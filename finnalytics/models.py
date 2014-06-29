# -*- coding: utf-8 -*-

'''

  models
  ~~~~~~

  :author: Sam Gammon <sam@momentum.io>
  :author: Ian Weisberger <ian@momentum.io>
  :author: David Rekow <david@momentum.io>
  :copyright: (c) momentum labs, 2014
  :license: The inspection, use, distribution, modification or implementation
            of this source code is governed by a private license - all rights
            are reserved by the Authors (collectively, "momentum labs") and held
            under relevant California and US Federal Copyright laws. For full
            details, see ``LICENSE.md`` at the root of this project. Continued
            inspection of this source code demands agreement with the included
            license and explicitly means acceptance to these terms.

'''

# stdlib
import uuid
import string
import random
import hashlib

# config
from config import config

# models
from base import model, Model
from canteen.util import struct


## Globals
private_length, public_length = 64, 16
default_token_length, invite_token_length = 12, 32
_key = lambda item: item.key if isinstance(item, Model) else item
salt = config.get('security', {}).get('salt') or unicode(uuid.uuid4())


class Permissions(struct.BidirectionalEnum):

  ''' Enumerates awardable permission levels between
      a :py:class:`User` and a :py:class:`Project`. '''

  VIEW = 0x0  # user can view a resource, but not modify or change perms
  EDIT = 0x1  # user can modify a resource, but not delete or change perms
  OWNER = 0x2  # user has full rights over an object and may change others' perms


_PERMISSIONS = frozenset((
  Permissions.VIEW,
  Permissions.EDIT,
  Permissions.OWNER
))


class User(Model):

  ''' Specifies a discrete user account, potentially
      tied to a domain. If a domain string is used,
      a ghost parent key prefixes the user key. '''

  name = basestring, {'required': True, 'indexed': True}
  email = basestring, {'required': True, 'indexed': True}
  domain = basestring, {'required': False, 'indexed': True}

  @classmethod
  def new(cls, name, email, domain=None, _save=True):

    '''  '''

    params = {
      'name': name,
      'email': email
    }

    # prepare domain and object
    if domain: params['domain'] = domain
    obj = cls(key=model.Key(cls, email, parent=(
      model.Key('Domain', domain)
    ) if domain else None), **params)

    if _save: obj.put()
    return obj


class Permission(Model):

  ''' Stores the highest specified permission between
      a :py:class:`User` and a :py:class:`Project`, as
      enumerated by :py:class:`Permissions`.

      Because the key ID is the user's email address
      and the parent key is the project, only one
      :py:class:`Permission` record may exist at a time
      between one :py:class:`User` and :py:class`Project`.
      Thus, the highest permission level for a user is
      expressed once for a given project. '''

  user = User, {'required': True}
  allow = bool, {'default': False}
  permission = int, {'choices': _PERMISSIONS}

  @classmethod
  def new(cls, user, permission, project, allow, _save=True):

    '''  '''

    if permission not in _PERMISSIONS:
      raise ValueError('Must pass a valid permission ID.')

    params = {
      'user': _key(user),
      'project': _key(project),
      'permission': permission,
      'allow': allow
    }

    obj = cls(key=model.Key(cls, user, parent=project), **params)
    if _save: obj.put()
    return obj


class Project(Model):

  ''' Specifies a user-created project that can receive
      data and display dashboards. Is potentially namespaced
      by a domain if the project is created in an enterprise
      context.

      A project has a string ``name`` that can be nice and
      human friendly (spaces/symbols OK).

      A project also has a string ``short_id`` that must be
      unique to the project, as it is used to build URLs.

      Permissions are enumerated in a repeated set of
      :py:class:`Permission` objects. An initial entry is
      added for the original project creator as ``OWNER``,
      and may not be removed if it is the only record. '''

  name = basestring, {'required': True}
  creator = User, {'required': True, 'indexed': True}
  domain = basestring, {'required': False, 'indexed': True}
  short_id = basestring, {'required': True, 'indexed': True}
  permissions = Permission, {'repeated': True, 'indexed': True}

  @classmethod
  def new(cls,
          name,
          short_id,
          creator,
          domain=None,
          permissions=None,
          _verify=True,
          _save=True):

    '''  '''

    if _verify:
      # try to fetch short-id, make sure it's not taken
      project_id = model.Key(cls, short_id, parent=(
        model.Key('Domain', domain)
      ) if domain else None)
      if project_id.get(): raise ValueError('Project name isn\'t available!')

    # calculate params
    params = {
      'name': name,
      'short_id': short_id,
      'creator': _key(creator)
    }

    # optional params
    if domain: params['domain'] = domain
    if permissions: params['permissions'] = permissions

    obj = cls(key=project_id, **params)
    if _save: obj.put()
    return obj


class APIKey(Model):

  ''' An API key expresses a pseudo-PKI-style key with a
      private (random) unshared value and a public value
      partially derived from the private value.

      An API key is bound to a project, and that's the
      key parent as well. Keys can be invalidated by
      setting the ``valid`` property to ``False``. '''

  project = Project, {'required': True, 'indexed': True}
  public = basestring, {'required': True, 'indexed': True}
  private = basestring, {'required': True, 'indexed': True}
  valid = bool, {'default': True, 'indexed': True}

  @classmethod
  def new(cls, project, _save):

    '''  '''

    # generate private
    keyhash, keycontent = Token.generate(
      project,
      length=private_length,
      hash=hashlib.md5
    )

    # generate public
    pubhash, pubcontent = Token.generate(
      project + keyhash,
      length=public_length,
      hash=hashlib.md5
    )

    # make APIkey object
    obj = cls(
      key=model.Key(cls, pubhash, parent=_key(project)),
      public=pubcontent,
      private=keycontent
    )

    if _save: obj.put()
    return obj


class Session(Model):

  ''' Model that specifies a client's session, as generated
      on the server-side and stapled for use by the JS
      frontend. The session ID is used in realtime and
      async (XHR-style) API calls.

      When the ``user`` property of a :py:class:`Session` is
      filled with a value, it is assumed that the session *is*
      authenticated with a valid user. '''

  user = User, {'required': False}
  session_id = basestring, {'required': True}


class Token(Model):

  ''' Specifies an opaque token (stored in ``content``) used
      in various tasks around the app, mostly for project
      invite emails. '''

  used = bool, {'default': False}
  expiry = int, {'indexed': True}
  creator = User, {'required': True}
  content = basestring, {'required': True}

  @classmethod
  def new(cls, parent, length=default_token_length, _save=True, **kwargs):

    '''  '''

    hash, content = cls.generate(length=default_token_length, hash=hashlib.md5)
    obj = cls(key=model.Key(cls, hash, parent=parent), content=content, **kwargs)
    if _save: obj.put()
    return obj

  @staticmethod
  def generate(cls, seed=None, uuid=False, length=default_token_length, hash=None):

    '''  '''

    if uuid: return uuid.uuid4()
    token = ''.join(filter(lambda _: _, (
      seed or None,
      reduce(lambda token, _: (token or '') + random.choice(string.hexdigits), xrange(0, length)),
      salt or uuid.uuid4()
    )))

    return (hash(token).hexdigest(), token) if hash else token


class Invite(Model):

  ''' Invitation model from a user to another user to
      view/edit/be an owner of a :py:class:`Project`.
      Once accepted, a corresponding record for a
      :py:class:`Permission` is created. '''

  invitee = User, {'indexed': True, 'required': True}
  invitor = User, {'indexed': True, 'required': True}
  token = Token, {'indexed': True, 'required': True}
  project = Project, {'indexed': True, 'required': True}

  @classmethod
  def new(cls, user, project):

    '''  '''

    params = {
      'user': _key(user),
      'project': _key(project),
      'token': _key(Token.new(parent=_key(project), length=invite_token_length))
    }

    return cls(key=model.Key(cls, _key(user).id, parent=_key(project)), **params)


class Event(Model):

  ''' Model specifying an analytics event that has been
      submitted to a ``collection`` for a given
      :py:class:`Project`. '''

  ip = basestring, {'required': True}
  agent = basestring, {'required': True}
  collection = basestring, {'required': True}
  project = Project, {'required': True}
  session = Session, {'required': False}
  data = dict

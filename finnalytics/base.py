# -*- coding: utf-8 -*-

'''

  base
  ~~~~

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
import datetime

# canteen
from canteen import rpc, model
from canteen.rpc import premote as proto


##### !!! Base Model !!! #####
class BaseModel(model.Model):

  ''' base model class '''

  __adapter__ = 'InMemoryAdapter' if __debug__ else 'RedisAdapter'

  # timestamps
  modified = datetime.datetime, {'auto_now': True}
  created = datetime.datetime, {'auto_now_add': True}

  @classmethod
  def factory(cls, parent=None, id=None, **kwargs):

    '''  '''

    # figure out key ID and parent
    id, parent = (
      parent if (not id or (isinstance(basestring, parent) and not parent)) else id,
      parent if not isinstance(parent, basestring) else None
    )

    # inject ID if we have one
    if hasattr(cls, 'id'): kwargs['id'] = id

    # factory object
    return cls(key=model.Key(cls, id, parent=parent), **kwargs)

Model = BaseModel


##### !!! Base Service !!! #####

## +=+ Auth Exceptions +=+ ##
class Unauthorized(proto.ApplicationError):

  ''' raised when authentication credentials
      aren't properly authorized to run a given
      method. '''


class AuthenticationRequired(proto.RequestError):

  ''' raised when authentication credentials
      are required, but were not provided at all. '''


## +=+ Base Service +=+ ##
class Service(rpc.Service):

  ''' base service class '''

  __credentials__ = None  # credentials pulled via `initialize`

  exceptions = rpc.Exceptions({
    # Base Exceptions
    'unauthorized': Unauthorized,
    'auth_required': AuthenticationRequired
  })

  @property
  def credentials(self):

    ''' property getter for request credentials '''

  def initialize(self, state):

    ''' initialize service transport state

        takes one of these:
        https://developers.google.com/appengine/docs/python/tools/protorpc/remote/requeststateclass

        or one of these if running over HTTP (likely):
        https://developers.google.com/appengine/docs/python/tools/protorpc/remote/httprequeststateclass '''

    # this is where we would interpret and mount authentication

  def enforce(self, request, level):

    ''' enforce authentication state interpreted
        by `Service.initialize`.

        :raises Unauthorized: if a method's credentials are not sufficiently privileged
        to complete the operation as-requested.

        :raises AuthenticationRequired: if a method requires authentication and no
        credentials are provided at all. '''

    # enforce authentication/authorization (mounted by `initialize`)

  @classmethod
  def protect(cls, *args):

    ''' class-level decorator to transparently apply auth protection of various levels
        to an otherwise-public service method. '''

    def _protected_method(cls):

      ''' wraps a protected method (``inner``) and attempts to validate
          previously-mounted credentials, by decorating the requested
          remote procedure with `Service.enforce`, which raises exceptions
          if auth requirements are not satisifed. '''

      def wrapped(self, request):

        ''' inner wrapped method that applies the proper dispatch and
            security enforcement flow. '''

      return wrapped
    return _protected_method

# bring up to module-level for syntactic sugar
public, protected = rpc.remote.public, Service.protect

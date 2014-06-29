# -*- coding: utf-8 -*-

'''

  project service
  ~~~~~~~~~~~~~~~

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

# app
import models

# service
from . import messages
from . import exceptions

# base
from base import rpc, Service
from base import public, protected


@public('project', version='v1')
class ProjectAPI(Service):

  '''  '''

  exceptions = rpc.Exceptions({
    'generic': exceptions.ProjectAPIException
  })

  @protected(messages.Projects)
  def list(self, request):

    '''  '''

    raise self.exceptions.generic('stubbed')

  @protected(models.Project, models.Result)
  def create(self, request):

    '''  '''

    raise self.exceptions.generic('stubbed')

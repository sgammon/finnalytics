# -*- coding: utf-8 -*-

'''

  write service
  ~~~~~~~~~~~~~

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

# service
from . import exceptions

# base
from finnalytics import models
from finnalytics.base import rpc, public, Service


@public('write', version='v0')
class WriteAPI(Service):

  '''  '''

  exceptions = rpc.Exceptions({
    'generic': exceptions.WriteAPIException
  })

  @public(models.Event, models.Result)
  def event(self, request):

    '''  '''

    raise self.exceptions.generic('stubbed')

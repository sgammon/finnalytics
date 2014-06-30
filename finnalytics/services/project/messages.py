# -*- coding: utf-8 -*-

'''

  project service messages
  ~~~~~~~~~~~~~~~~~~~~~~~~

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

# canteen
from canteen import model


class Projects(model.Model):

  ''' Contains a set of projects returned
      from an API request. '''

  count = int, {'default': 0}
  offset = int, {'default': 0}
  data = models.Project, {'repeated': True}
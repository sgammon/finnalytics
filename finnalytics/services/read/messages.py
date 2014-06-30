# -*- coding: utf-8 -*-

'''

  read service messages
  ~~~~~~~~~~~~~~~~~~~~~

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

# canteen
from canteen import model

# app
from finnalytics import models


class Projects(model.Model):

  ''' Contains a set of projects returned
      from an API request. '''

  count = int, {'default': 0}
  offset = int, {'default': 0}
  data = models.Project, {'repeated': True}


class Metrics(model.Model):

  ''' Contains a set of metrics that exist,
      returned from an API request. '''

  class Metric(model.Model):

    ''' Individual ``metric``, which is a
        dimension or logical point that
        may contain a number, usually
        bound by a timewindow. '''

    name = basestring, {'required': True}
    aggregate = bool, {'default': True}

  count = int, {'default': 0}
  offset = int, {'default': 0}
  data = Metric, {'repeated': True}


class Stats(model.Model):

  ''' Filled-out (metric data) returned
      from an API request. '''

  class Stat(model.Model):

    ''' Contains a single discrete point of
        data, which is where a :py:class:`Metric`
        and real life cross paths. '''

    value = float, {'default': 0.0}
    window = int, {'default': 86400}
    metric = Metrics.Metric, {'required': True}

  count = int, {'default': 0}
  start = int, {'default': 0}
  offset = int, {'default': 0}
  data = Stat, {'repeated': True}


class Query(model.Model):

  ''' A full dataset query (in GQL), with
      a pointer to a resultset (someday.) '''

  source = basestring, {'required': True}

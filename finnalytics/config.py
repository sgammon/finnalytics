# -*- coding: utf-8 -*-

'''

  finnalytics: configuration
  ~~~~~~~~~~~~~~~~~~~~~~~~~~

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

import canteen, os, hashlib
from canteen.util import config as cfg


app, root = (
  os.path.abspath(os.path.dirname(__file__)),
  os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
)

config = cfg.Config(app={

  'name': 'finnalytics',

  # Main app settings
  'debug': __debug__,

  # Dev tools
  'dev': {

    'profiler': {
      'enable': False
    }

  },

  # Runtime config
  'runtime': 'werkzeug',

  # App paths
  'paths': {

    'assets': os.path.join(app, 'assets'),
    'favicon': os.path.join(app, 'assets', 'img', 'favicon.ico'),

    'templates': {
      'source': os.path.join(app, 'templates', 'source'),
      'compiled': 'finnalytics.templates.compiled'
    }

  }

}, config={

  ##### ===== General Settings ===== #####

  # Gevent Config
  'gevent': {

    'engine': 'wsgi'  # `pywsgi`, `wsgi`, or `stream`

  },

  # HTTP semantics
  'http': {

    # HTTP session settings
    'sessions': {

      'engine': 'cookies',

      'cookies': {
        'key': 'finnalytics',
        'domain': None,
        'path': '/',
        'secure': False,  # only secure in production
        'http_only': True,
        'max_age': 3600,
        'mode': 'json'
      }

    },

    # Default headers to add
    'headers': {
      'X-DNS-Prefetch-Control': 'on'
    }

  },

  ##### ===== Framework APIs ===== #####

  ### == Cache API == ###
  'CacheAPI': {
    'debug': __debug__,
  },

  ### === Model API === ###
  'ModelAPI': {
    'debug': __debug__,
  },

  ### === Session API === ###
  'SessionAPI': {
    'enable': True,

    'debug': __debug__,

    'always_establish': True,

    'salt': 'vcklckxvnliNP@J!@)U@!)&)@(Udoijpoj2-19',
    'secret': 'jvn80Y)!*U)@(U@)(Jdij029jlcknv083y1f',
    'algorithm': hashlib.sha1
  },

  ### === Template API === ###
  'TemplateAPI': {
    'debug': __debug__,

    'force_compiled': False,

    'haml': {
      'debug': __debug__,
      'mode': 'compact'
    },

    'syntax': {
      'variable': ('{{', '}}'),
      'block': ('{%', '%}'),
      'comment': ('{#', '#}')
    },

    'jinja2': {

      'autoescape': True,

      'extensions': [
        'jinja2.ext.autoescape',
        'jinja2.ext.with_',
      ],

    }
  },

  ##### ===== Database APIs ===== #####
  'RedisAdapter': {
    'debug': True,

    'servers': {

      'default': 'local',

      # Redis Instances
      'local': {'host': '127.0.0.1', 'port': 6379}
    }
  },

}, assets={

  ##### ===== Assets ===== #####

  # Asset API config
  'config': {

    # main settings
    'minified': False,
    'cdn_prefix': ['//'],
    'serving_mode': 'cdn' if not __debug__ else 'local',

  },

  # Asset registry
  'assets': {

    'style': {

      'sample': {

        # sample app CSS
        'app': {'version': 'v1', 'minified': False}

      }

    },

    'scripts': {

    },

    'fonts': {

    }

  }


})

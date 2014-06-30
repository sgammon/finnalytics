#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ = '''

  development toolchain
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

__version__ = (0, 0, 1)
__author__ = "momentum labs, ltd"


# stdlib
import os, sys, subprocess, time, StringIO

project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'lib'))
sys.path.insert(0, os.path.join(project_root, 'lib/canteen'))
sys.path.insert(0, os.path.join(project_root, 'finnalytics'))
sys.path.insert(0, os.path.join(project_root, 'finnalytics/lib'))

# finnalytics
import finnalytics, canteen
from finnalytics import config
from finnalytics import logic
from finnalytics import pages
from finnalytics import services

# preload all the things
from finnalytics.logic import *
from finnalytics.pages import *
from finnalytics.config import *
from finnalytics.services import *

# canteen util
from canteen.util import cli, debug


## Globals
logging = debug.Logger(name='finna')
UWSGI_BASE_ARGS, UWSGI_PROD_ARGS = [
  "--pcre-jit",
  "--vacuum",
  "--py-autoreload",
  "--pidfile=/tmp/finnalytics.pid",
  "--wsgi=finnalytics.dispatch:application",
  "--shared-import=finnalytics",
  "--shared-import=werkzeug",
  "--shared-import=canteen",
  "--shared-import=jinja2",
], [
  "--optimize",
  "--uwsgi=127.0.0.1:3000"
]


class Finnalytics(cli.Tool):

  ''' Minimal toolchain for managing and developing a
      canteen-based web application. '''

  arguments = (
    ('--debug', '-d', {'action': 'store_true', 'help': 'run in debug mode'}),
    ('--quiet', '-q', {'action': 'store_true', 'help': 'suppress most output'}),
    ('--verbose', '-v', {'action': 'count', 'help': 'output a lot of useful info'}),
    ('--version', '-V', {'action': 'version', 'help': 'print version and exit', 'version': 'webtool %s' % '.'.join(map(unicode, __version__))})
  )

  ## == Bound Commands == ##
  class Run(cli.Tool):

    ''' Runs the local devserver. '''

    arguments = (
      ('--ip', '-i', {'type': str, 'help': 'address to bind to'}),
      ('--port', '-p', {'type': int, 'help': 'port to bind to'}),
      ('--production', '-p', {'action': 'store_true', 'help': 'simulate production'}),
      ('--no-nginx', '-nn', {'action': 'store_true', 'help': 'don\'t startup nginx when simulating production'}),
      ('--no-haproxy', '-nh', {'action': 'store_true', 'help': 'don\'t startup haproxy when simulating production'})
    )

    def execute(arguments):

      ''' Execute the ``finna run`` tool, given a set of arguments packaged
          as a :py:class:`argparse.Namespace`.

          :param arguments: Product of the ``parser.parse_args()`` call,
          dispatched by ``apptools`` or manually.

          :returns: Python value ``True`` or ``False`` depending on the
          result of the call. ``Falsy`` return values will be passed to
          :py:meth:`sys.exit` and converted into Unix-style return codes. '''

      if production:
        raise ValueError('production simulation isn\'t supported for local yet')

      canteen.run(finnalytics, **{
        'port': arguments.port or 9001,
        'interface': arguments.ip or '127.0.0.1',
        'config': config or {}
      })


  class Shell(cli.Tool):

    ''' Runs a local or simulated production shell. '''

    arguments = (
      ('--production', '-p', {'action': 'store_true', 'help': 'simulate production'}),
    )

    def execute(arguments):

      ''' Execute the ``finna shell`` tool, given a set of arguments packaged
          as a :py:class:`argparse.Namespace`.

          :param arguments: Product of the ``parser.parse_args()`` call,
          dispatched by ``canteen`` or manually.

          :returns: Python value ``True`` or ``False`` depending on the
          result of the call. ``Falsy`` return values will be passed to
          :py:meth:`sys.exit` and converted into Unix-style return codes. '''

      # assemble uWSGI arguments
      uwsgi_args = [

        # uwsgi path
        os.path.join(project_root, 'bin', 'uwsgi'),

        # base interactive flags
        "--socket=/tmp/finnalytics.sock",
        "--pyshell"

      ] + UWSGI_BASE_ARGS + (UWSGI_PROD_ARGS if arguments.production else [])

      try:
        # spawn uWSGI
        shell = subprocess.Popen(uwsgi_args,
          stdin=sys.stdin,
          stdout=sys.stdout,
          stderr=sys.stderr
        )

        returncode = shell.wait()

      except KeyboardInterrupt:
        shell.terminate()
        time.sleep(1)  # sleep a second to let console shut up
      sys.stdin, sys.stdout, sys.stderr = (StringIO.StringIO() for x in (0, 1, 2))


  class Build(cli.Tool):

    ''' Builds local sources. '''

    arguments = (
      ('--gzip', {'action': 'store_true', 'help': 'pre-gzip assets'}),
      ('--sass', {'action': 'store_true', 'help': 'collect/compile SASS'}),
      ('--scss', {'action': 'store_true', 'help': 'collect/compile SCSS'}),
      ('--less', {'action': 'store_true', 'help': 'collect/compile LESS'}),
      ('--coffee', {'action': 'store_true', 'help': 'collect/compile CoffeeScript'}),
      ('--closure', {'action': 'store_true', 'help': 'preprocess JS with closure compiler'}),
      ('--templates', {'action': 'store_true', 'help': 'compile and optimize jinja2 templates'})
    )

    def execute(arguments):

      ''' Execute the ``web build`` tool, given a set of arguments
          packaged as a :py:class:`argparse.Namespace`.

          :param arguments: Product of the ``parser.parse_args()``
          call, dispatched by ``apptools`` or manually.

          :returns: Python value ``True`` or ``False`` depending on
          the result of the call. ``Falsy`` return values will be
          passed to :py:meth:`sys.exit` and converted into Unix-style
          return codes. '''

      if arguments.templates:

        logging.info('Compiling app templates...')

        from scripts import compile_templates

        # delete existing templates first, if any
        logging.info('Cleaning existing template path...')
        module_root = os.path.join(project_root, "finnalytics", "templates")

        clean_command = "rm -fr %s" % os.path.join(module_root, "compiled", "*")
        if config.get('debug', False):
          logging.debug('Executing command: "%s".' % clean_command)
        os.system(clean_command)

        # run the template compiler
        try:
          result = compile_templates.run()
        except:
          logging.error('An exception was encountered while compiling templates.')
          raise
        else:
          logging.info('Templates compiled successfully.')


  class Deploy(cli.Tool):

    ''' Deploys code to prod/staging. '''

    arguments = (
      ('env', {'choices': ('sandbox', 'staging', 'production'), 'help': 'environment to deploy to'}),
      ('dc', {'choices': ('dal', 'sj'), 'help': 'datacenter to deploy to (defaults to both)'}),
      ('--assets', {'action': 'store_true', 'help': 'only deploy static assets'}),
      ('--notest', {'action': 'store_true', 'help': 'don\'t run tests before deploying (DANGEROUS!)'})
    )

    def execute(arguments):

      ''' Execute the ``web deploy`` tool, given a set of arguments
          packaged as a :py:class:`argparse.Namespace`.

          :param arguments: Product of the ``parser.parse_args()``
          call, dispatched by ``apptools`` or manually.

          :returns: Python value ``True`` or ``False`` depending on
          the result of the call. ``Falsy`` return values will be
          passed to :py:meth:`sys.exit` and converted into Unix-style
          return codes. '''

      import pdb; pdb.set_trace()


if __name__ == '__main__':
  Finnalytics(autorun=True)  # initialize and run :)

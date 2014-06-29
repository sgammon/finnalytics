# -*- coding: utf-8 -*-

'''

  setup
  ~~~~~

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

# setuptools
import setuptools as tools, finnalytics


tools.setup(name="finnalytics",
            version='-'.join(['.'.join(map(unicode, finnalytics.__version__)), 'alpha']),
            description="Shhh.....",
            author="Sam Gammon",
            author_email="sam@momentum.io",
            url="https://github.com/sgammon/canteen",
            packages=[
              "finnalytics",
              "finnalytics.logic",
              "finnalytics.services",
              "finnalytics.services.read",
              "finnalytics.services.write",
              "finnalytics.services.security"
            ] + [
              "finnalytics_tests"
            ] if __debug__ else [],
            install_requires=(
              "canteen-0.2-alpha",
            ),
            dependency_links=(
              "git+git://github.com/sgammon/canteen.git#egg=canteen-0.2-alpha",
            ),
            tests_require=("nose",)
)

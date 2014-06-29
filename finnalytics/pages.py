# -*- coding: utf-8 -*-

'''

  pages
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

# stdlib
import pdb

# canteen
from canteen import url, Page
if __debug__: from canteen.model.adapter import inmemory


# homepage!
@url('home', u'/')
class Homepage(Page):

  '''  '''

  if __debug__:

    # bind metadata/datastore for introspection
    __metadata__, __datastore__, metadata, datastore = (
      inmemory._metadata,
      inmemory._datastore,
      property(lambda self: self.__metadata__),
      property(lambda self: self.__datastore__)
    )

  def GET(self):

    ''' handles HTTP GET '''

    # allow interactive breakpoints for inspection
    if __debug__ and self.request.args.get('debug'): pdb.set_trace()

    return self.render('home.haml', message='hi')

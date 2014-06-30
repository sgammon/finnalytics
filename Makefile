
#
#   finnalytics
#
#   :author: Sam Gammon <sam@momentum.io>
#   :author: Ian Weisberger <ian@momentum.io>
#   :author: David Rekow <david@momentum.io>
#   :copyright: (c) momentum labs, 2014
#   :license: This is private software code and all
#             rights to access, observe, run, compile
#             deploy, modify, put use to, or leverage
#             for commercial gain (and any other rights
#             not enumerated here as governed by
#             applicable law) are held and reserved
#             ad infinitum by momentum labs, inc. and
#             its employees, founders, and partners.
#


## Vars
HOST?=127.0.0.1
PORT?=9000
DEBUG?=1
USER?=`whoami`
SANDBOX_GIT?=$(USER)@sandbox
CANTEEN_BRANCH?=master
SCRATCHSPACE=.develop
BREW=openssl python haproxy redis nginx pypy uwsgi

## Flags
TEST_FLAGS ?= --verbose --with-coverage --cover-package=finnalytics --cover-package=finnalytics_tests


all: develop
	@which zsh || echo "We noticed you're using bash or something. Execute 'source bin/activate' to go begin."
	@echo "~~ im finna count some shit ~~"
	@which zsh && zsh -c "source bin/activate" -i

test: build
	@bin/nosetests $(TEST_FLAGS) canteen_tests finnalytics_tests

build: .Python canteen dependencies npm env
	@echo "Built finnalytics."

develop: build
	@echo "Updating source dependencies..."

canteen: $(PWD)/lib/python2.7/site-packages/canteen.pth
	@echo "Cloning as user $(USER)..."
	@git clone https://github.com/momentum/canteen.git $(PWD)/lib/canteen -b $(CANTEEN_BRANCH)

package: develop
	@echo "Making buildroot..."
	@mkdir -p dist/ build/

	@echo "Building source package..."
	@bin/python setup.py sdist

	@echo "Building eggs..."
	@bin/python setup.py bdist_egg bdist_dumb

	@echo "Distributions build."

clean:
	@echo "Cleaning buildspace..."
	@rm -fr build/

	@echo "Cleaning egginfo..."
	@rm -fr finnalytics.egg-info

	@echo "Cleaning object files..."
	@find . -name "*.pyc" -delete
	@find . -name "*.pyo" -delete
	@find . -name "*.report.txt" -delete

distclean: clean
	@echo "Cleaning env..."
	@rm -fr .Python lib include

	@echo "Resetting codebase..."
	@git reset --hard

	@echo "Cleaning codebase..."
	@git clean -xdf

dependencies: $(PWD)/lib/closure/compiler.jar
	@# install pip dependencies
	@bin/pip install colorlog
	@bin/pip install -r requirements.txt

.Python:
	@# install pip/virtualenv if we have to
	@which pip || sudo easy_install pip
	@which virtualenv || pip install virtualenv

	@which brew && brew install $(BREW) 2> /dev/null

	@# make virtualenv and install stuffs
	@virtualenv .

	@# symlink environment
	@ln -s $(PWD)/scripts/finna.py $(PWD)/bin/finna
	@chmod +x $(PWD)/bin/finna

npm: $(PWD)/node_modules
$(PWD)/node_modules:
	@echo "Installing NPM dependencies..."
	@-npm install

env: $(PWD)/$(SCRATCHSPACE)
$(PWD)/.develop: $(PWD)/node_modules
	@echo "Making develop scratchspace..."
	@-mkdir -p $(SCRATCHSPACE)/ $(SCRATCHSPACE)/maps/finnalytics/assets/{coffee,style,less,sass,js}
	@-chmod 777 $(SCRATCHSPACE) -R

	@echo "Initializing frontend..."
	@-ln -s node_modules/gulp/bin/gulp ./bin/gulp
	@-bin/gulp

$(PWD)/lib/closure/compiler.jar:
	@echo "Downloading Closure Compiler..."
	@-wget http://dl.google.com/closure-compiler/compiler-latest.zip
	@-mkdir -p $(PWD)/lib/closure

	@echo "Extracting Closure Compiler..."
	@-unzip compiler-latest.zip -d $(PWD)/lib/closure
	@-mv compiler-latest.zip $(PWD)/lib/closure
	@-rm -f compiler-latest.zip

	@-mkdir -p $(PWD)/lib/closure/build;
	@-mv $(PWD)/lib/closure/compiler.jar $(PWD)/lib/closure/build/compiler.jar;

$(PWD)/lib/python2.7/site-packages/canteen.pth:
	@echo "$(PWD)/lib/canteen" > lib/python2.7/site-packages/canteen.pth

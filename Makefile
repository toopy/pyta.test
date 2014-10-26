
DRIVER ?= "phantomjs"
HOST   ?= "www.github.com"
TEST   ?= "pyta_test"

install:
	pip install -r requirements.pip

it:
	py.test -s --splinter-webdriver ${DRIVER} --host ${HOST} ${TEST}

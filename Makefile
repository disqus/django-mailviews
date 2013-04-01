STATIC_DIRECTORY = mailviews/static/mailviews

LESSC = ./node_modules/.bin/lessc
JQUERY = $(STATIC_DIRECTORY)/javascript/jquery.js


$(LESSC):
	npm install .

bootstrap: $(LESSC)
	git submodule update --init
	$(LESSC) vendor/bootstrap/less/bootstrap.less > $(STATIC_DIRECTORY)/css/bootstrap.css
	cp vendor/bootstrap/js/bootstrap-*.js $(STATIC_DIRECTORY)/javascript

$(JQUERY):
	curl http://code.jquery.com/jquery-1.8.3.js > $(JQUERY)

static: bootstrap $(JQUERY)


develop: static
	python setup.py develop

lint:
	pip install --use-mirrors flake8
	flake8 ./mailviews

clean:
	find . -name *.pyc -delete

test: clean
	python setup.py test

test-matrix: clean
	which tox >/dev/null || pip install --use-mirrors tox
	tox

test-server: develop
	python mailviews/tests/manage.py runserver

publish: static
	git tag $$(python setup.py --version)
	git push && git push --tags
	python setup.py sdist upload


.PHONY: bootstrap static develop lint clean test test-matrix test-server publish

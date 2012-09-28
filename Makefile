lint:
	pip install --use-mirrors flake8
	flake8 ./mailviews

clean:
	find . -name *.pyc -delete

test: clean
	python setup.py test

publish: lint tests
	git tag $$(python setup.py --version)
	git push --tags
	python setup.py sdist upload -r disqus

.PHONY: clean lint test publish

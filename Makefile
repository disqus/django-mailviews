lint:
	pip install --use-mirrors flake8
	flake8 ./mailview

clean:
	find . -name *.pyc -delete

test: clean
	python setup.py test

.PHONY: clean lint test

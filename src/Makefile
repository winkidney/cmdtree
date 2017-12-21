PYPI = https://pypi.python.org/pypi
default:
	@grep '^[^#[:space:]].*:' Makefile
mk-dist:
	python setup.py bdist sdist bdist_wheel upload -r $(PYPI)

clean:
	rm -fr ./dist ./build ./cmdtree.egg-info ./.cache

test:
	py.test tests --cov=cmdtree --cov-report=term-missing cmdtree

develop:
	python setup.py develop

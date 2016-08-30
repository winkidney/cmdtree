PYPI = https://pypi.python.org/pypi
default:
	@grep '^[^#[:space:]].*:' Makefile
mk-dist:
	python setup.py bdist sdist bdist_wheel upload -r $(PYPI)

clean:
	rm -fr ./dist ./build ./cmdtree.egg-info ./.cache

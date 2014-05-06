
.PHONY: clean

clean:
	-rm -rf build/ temp/ MANIFEST dist/ src/*.egg-info src/radical/ensemblemd/htbac/VERSION pylint.out *.egg
	find . -name \*.pyc -exec rm -f {} \;
	find . -name \*.egg-info -exec rm -rf {} \;

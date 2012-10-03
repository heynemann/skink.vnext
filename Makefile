test:
	@nosetests --with-yanc -s --with-coverage --cover-erase --cover-inclusive --cover-package=skink tests/

ci-test:
	@nosetests -s --with-coverage --cover-erase --cover-inclusive --cover-package=skink tests/

deps:
	@pip install -r python_requirements.txt

pep8:
	@find . -name '*.py' | xargs autopep8 -i

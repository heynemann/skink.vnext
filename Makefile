test:
	@nosetests -s --with-coverage --cover-erase --cover-inclusive --cover-package=skink tests/

deps:
	@pip install -r python_requirements.txt

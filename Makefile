test:
	@nosetests -s --with-coverage --cover-erase --cover-inclusive --cover-package=skink

deps:
	pip install -r python_requirements.txt

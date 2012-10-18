test:
	@nosetests -vv --pdb --pdb-failures --with-yanc -s --with-coverage --cover-erase --cover-inclusive --cover-package=skink tests/

kill-watch:
	@-ps aux | egrep 'grunt watch' | egrep -v egrep | awk ' { print $$2 }' | xargs kill -9

watch: kill-watch
	@./node_modules/.bin/grunt watch &

dev:
	@./node_modules/.bin/grunt dev

compile:
	@./node_modules/.bin/grunt compile

web: dev watch
	@PYTHONPATH=$(PYTHONPATH):. python skink/web/server.py -d -vv

ci-test:
	@nosetests -s --with-coverage --cover-erase --cover-inclusive --cover-package=skink tests/

kill_redis:
	@ps aux | awk '(/redis-server/ && $$0 !~ /awk/){ system("kill -9 "$$2) }'

redis: kill_redis
	@mkdir -p /tmp/skink/db
	@redis-server redis.conf &

setup deps:
	@command -v node >/dev/null 2>&1 || { echo >&2 "Node.js must be installed and accessible to develop skink. Please visit http://nodejs.org/ for more info."; exit 1; }
	@command -v npm >/dev/null 2>&1 || { echo >&2 "Node.js Package Manager (NPM) must be installed and accessible to develop skink. Please visit https://npmjs.org/ for more info."; exit 1; }
	@command -v bundle >/dev/null 2>&1 || { echo >&2 "Bundler must be installed and accessible to develop skink. Please visit http://gembundler.com/ for more info."; exit 1; }
	@bundle install
	@cat node_requirements.txt | xargs npm install
	@pip install -r python_requirements.txt
	@cp -rf ./node_modules/node-ffi/compiled/0.6/ ./node_modules/node-ffi/compiled/0.6.12/ #bizarre hack for node ffi

pep8:
	@find . -name '*.py' | xargs autopep8 -i

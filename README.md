![skink ci](https://raw.github.com/heynemann/skink.vnext/master/gh/skink-logo.png) 

[![Build Status](https://secure.travis-ci.org/heynemann/skink.vnext.png)](http://travis-ci.org/heynemann/skink.vnext)

# Introduction

Skink is a continuous integration server that uses virtualization to run the app being built.

By using virtualization, Skink allows users to run builds against a clean environment with
their apps running every time.

The idea is borrowed from the incredibly smart [travis CI](http://travis.ci) service.
If you just need to build an open source project hosted in github, travis is the way to go.
Skink repository is built using travis.

# Installing

Installing Skink is very simple, provided you have the necessary requirements:

* Python 2.6 or greater;
* VirtualBox latest version (considering you are using VirtualBox Provider);
* Redis (or any other persisting mechanism you choose).

After having setup these requirements, just install it using pip:

``pip install skink``

# Running Skink

Skink is divided in three major components:

* Web Interface;
* Build Workers;
* Repository Monitoring (optional).

The "communication bus" between these three parts is the persistence mechanism (Redis for instance).

## The Web Interface

Skink's web interface provides the users with realtime information about 
what's happening with their builds, as well as allowing users to manage projects, builds and workers.

Running the web interface using port 8888 is as simple as:

``skink-web -p 8888 --redis-host="localhost" --redis-port=3128``

## Build Workers

The build workers pull jobs out of Redis and create the proper VMs to
run the jobs, as well as run the jobs in said VMs.

The workers use a VM Provider, which is a class that complies to [[Skink's Provider Specification]].

After selecting your provider, just run as many workers as you feel are needed using:

``skink-worker --provider="skink.providers.VirtualBoxProvider" --redis-host="localhost" --redis-port=3128``

It's worth noting that each worker will spawn one VM.

## Repository Monitoring

A continuous integration server should be able to react to changes in 
the repositories as fast as possible.

Towards that goal, Skink provides an endpoint at ``http://<skink server>/<project name>/build ``
which will put a build job to the specified project in the build queue.

The first worker that gets the job will build the project. This mechanism works pretty well
if your git server supports hooks and if your skink server is accessible to the git server.

Since we know not all scenarios allow that, Skink allows users to specify a repository monitor
that keeps checking repositories for new commits.

Given the most common scenario is polling repositories for changes, Skink comes with a bundled
PollingMonitor that will keep polling the registered repositories for anything new and triggering a new
build in the event of a change.

Running a Repository Monitor is as simple as:

``skink-monitor --monitor="skink.monitors.PollingMonitor" --interval=60 --redis-host="localhost" --redis-port=3128``

This will poll all repositories every minute and report to redis if any of them needs building.

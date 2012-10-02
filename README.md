![skink ci](https://raw.github.com/heynemann/skink.vnext/master/gh/skink-logo.png) 

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

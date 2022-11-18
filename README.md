# Background
While trying to get async-redis to work I ran into issues while writing unit tests for it.
This code for this git repo boils down the code to it's most basic parts.

# Prerequisites
1. This assumes you have python 3.9 installed on your machine. If you don't then simply edit setup_venv.sh and give it a different python version.
2. This assumes you have the virtualenv package installed (via brew).

# How to build
1. Open a terminal window
2. Run the command `./setup_venv.sh`
3. Run the command `source venv/bin/activate`

# How to run all the tests
1. First build the code (see steps above)
2. Run the command `make unit-tests`

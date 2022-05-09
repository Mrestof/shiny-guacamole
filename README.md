# Shiny ~~like a guacamole~~ `IEC 60870-5-104` protocol emulator
Listen for incoming packets. Based on info about sender and data in package response accordingly.

## DevOps
### Run environment
- The project is developed and tested on GNU/Linux system under Arch distribution.
- Python 3.8.13 is used for executing `.py` scripts.
### Execution process
1. run the `server.py` with an appropriate python interpreter
2. the process:
   1. waits for a new connection
   2. logs everything in stdout
   3. exits when the connection is closed

## TODO
### global:
- [x] make working prototype
  - [x] fix behaviour
  - [ ] test the fix
- [ ] cover the whole code with exceptions
- [ ] replace print with varying levels of logging
### server:
- [ ] cover the code with exceptions
- [ ] set the socket timeouts by hand
- [ ] add command line parameters
  - [ ] name of the config to load
  - [ ] number of entire code cycle repeats
### test-client:
- [ ] cover the code with exceptions
- [ ] expand the test
  - [ ] test to connect with forbidden address
  - [ ] test to overtime the connection
- [ ] add command line parameters
  - [ ] list of tests to accomplish
- [ ] add command line prompt to execute tests in interactive way
### configs:
- [x] refactor the storage method of configs
- [x] ensure the passed configs are in correct form
- [x] change `data_rows` values format

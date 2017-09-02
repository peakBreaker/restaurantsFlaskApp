# Restaurants Webapplication

A sample dynamically driven webapplication project using the python flask framework and sqlalchemy.

## Getting started

Instructions on getting a local copy of the project running for development and testing purposes.

### Prerequists

- Vagrant
- VirtualBox

### Installing

1. Clone this repository `$ git clone https://github.com/Andurshurrdurr/SwissTournament_SQL`
2. Open a terminal and cd into the cloned repository
3. Get the VM running with Vagrant `$ vagrant up` - This may take a while
4. The VM should now be running, SSH into it `$ vagrant ssh`
5. Once you are running a shell in the vm, cd to the synced folder `$ cd /vagrant`
6. For OAuth2.0 to work with facebook and/or google, move the client secrets to root of this synced folder. The keys can be downloaded through google and facebooks developer portals, see oauth tokens further down. The google client secrets should be named 'client_secrets.json', and the facebook client secrets should be named 'fb_client_secrets.json'.
7. (Optional) Seed the database: `$ python seedMenus.py`
8. Run the application: `$ python run.py`

#### OAuth tokens:

Create a new project and credentials (google) or facebook login (facebook)
[Facebook](https://developers.facebook.com/docs/facebook-login)
[Google](https://developers.google.com/)
[I found this helpful for google oauth](https://support.google.com/googleapi/answer/6158857?hl=en)

Follow instructions given by the providers

## Deploying

I have a running [AWS EC2](http://restaurants.peakbreaker.com) instance serving this application

You may deploy your fork of this app aswell on a VPS by using my [serverConfig](https://github.com/peakBreaker/serverSetups) configuration management ansible-playbook scripts to automatically configure a server and deploy the app.

## License

The MIT License (MIT)

Copyright (c) 2017 Anders Hurum

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

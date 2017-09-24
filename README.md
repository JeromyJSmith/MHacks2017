# MHacks2017

Michigan Hackathon with Austin Klisch and Austin Meyer

* https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04
* https://tecadmin.net/install-python-3-6-ubuntu-linuxmint/  
* To setup AWS instance (Need to build python version from source):
- install gcc, make, zlib1g-dev
- $ sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
- sudo wget http://www.python.org/ftp/python/3.6.2/Python-3.6.2.tgz
- extract it
- Instruction can be found in README.rst, but to install:
  - sudo ./configure
  - sudo make
  - (optional) sudo make test
  - sudo make install
  - export PATH=$PATH:/usr/local/bin/python3
  - Make venv with 3.6.2 and requirements.txt
- Install and setup docker


* To run Docker container on local machine through ngrok for development,  
   in ./run-build map <ngrok port/flask app port> to 80 ( -p port:80), then ngrok  
   will correctly tunnel

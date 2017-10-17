# Project 1

## Bayesian Network Scoring
This project is a competition to find Bayesian network structures that best fit some given data.

### Scoring: Cooper&Herskovits, 1992
The scoring function is callibrated using the original Bayesian Structure Scoring paper, from which first published the
equations in the Decision Under Uncertainty book (2.80).  The paper provides example input data and values for
two Bayesian networks.
The test class is: graphotest.py
The input file: cooperh.csv

#### Docker on Mac

To run a Docker container, you:

- create a new (or start an existing) Docker virtual machine
- switch your environment to your new VM
- use the docker client to create, load, and manage containers

If not already done, create the machine:
``
docker-machine create
``

Start the daemon:

``
docker-machine start default
``

Confirm the daemon is running:
``
docker-machine ls
``

Connect to the machine:
``
eval "$(docker-machine env default)"
``

Any docker exposed ports are available on the virtual machine's IP address.  Get the host IP:
``
docker-machine ip default
``


Reference: https://docs.docker.com/machine/get-started/#create-a-machine

#### Brew on Mac

Homebrew is a package manager designed for installing UNIX tools.

Install xCode:
``
xcode-select --install
``

Install Homebrew:
``
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
``

Confirm the installs worked:
``
brew doctor
``

Install test environment for Jenkins:
``
brew install bats
``

Reference: https://www.howtogeek.com/211541/homebrew-for-os-x-easily-installs-desktop-apps-and-terminal-utilities/

### All

Go to the build foldeR:
``
cd Image-Docker--Build/Docker--Jenkins/
``

Build the Jenkins image:
``
docker build --file Dockerfile --tag jenkins/jenkins .
``

Test the Jenkins setup:
``
git clone https://github.com/jenkinsci/docker.git
bats docker/tests
``

Run Jenkins, providing it a volume:
``
mkdir jenkins_home
docker run --publish 8080:8080 --publish 50000:50000 --volume jenkins_home:/var/jenkins_home jenkins/jenkins:lts
``

Log on to Jenkins, on the virtual machine at teh published port, for instance:
``
http://192.168.99.100:8080
``

Unlock Jenkins, logging into the container ID, pasting the admin passoword in the Jenkins webpage:
``
docker ps
docker exec --interactive --tty 48fa37c3fb9e bash
cat /var/jenkins_home/secrets/initialAdminPassword
``

Then create select the desired plugins and user name/password:

Reference: https://github.com/jenkinsci/docker

## Repo: building and running





# Fullstack-Udacity: Tournament Results

## Requirements
- python 2.7.10
- vagrant: https://www.vagrantup.com/downloads.html
- virtualBox: https://www.virtualbox.org/wiki/Downloads

### Setup

1.Download all the requirement files and install them first
2.Navigate to folder project4/vagrant
3.Input the following command in your terminal to set up virtual machine
  ```bash
    vagrant up
  ```
4.Input the following command to connect to virtual machine
  ```bash
    vagrant ssh
  ```
4.Navigate to /vagrant/tournament
5.run tournament_test.py to check the testing result
ps: tournament.sql is database schema definition file
    tournament.py is self-developed database api file
    tournament_test.py is unit testing file
    
### Feature
```
1. Avoiding Rematching Mechanism
```

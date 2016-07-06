# Fullstack-Udacity

## Requirements
- python 2.7.10


## Project1 : Movie Trailer Website

### Setup

Download folder "project1", then using commande line to direct to this directory.
Then runing the following command, the page will open automaticly

```bash
$ python entertainment_center.py
```

## Project2 : Build a Portfolio Site

### Setup

1.Download folder "project2", just render index.html in browser.

## Project3 : Multi User Blog

### Setup

1.Download folder "project3". User Googgle App Engine to lauch it.

2.The public accessible link is: https://youyue-g.appspot.com/blog

### Feature

```
1.Fully functional secure acccount management(including login,register,logout feature)
2.Fully functional blog management(including create,edit,delete,view posts feature)
3.Comment and like feature
```

## Project4 : Tournament Results

### Special Requirement:

```
vagrant: https://www.vagrantup.com/downloads.html
virtualBox: https://www.virtualbox.org/wiki/Downloads
```

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
## Project5 : Item Catalog

### Special Requirements
- vagrant: https://www.vagrantup.com/downloads.html
- virtualBox: https://www.virtualbox.org/wiki/Downloads

### Setup

1.Download all the requirement files and install them first
2.Navigate to folder project5/vagrant
3.Input the following command in your terminal to set up virtual machine
  ```bash
    vagrant up
  ```
4.Input the following command to connect to virtual machine
  ```bash
    vagrant ssh
  ```
4.Navigate to /vagrant/catalog
5.run application.py
6.Go to browser and open localhost:5000. You will see the website result.
    
### Feature
```
1. JSON API EndPoints : '/country/JSON'and '/country/<int:country_id>/football_club/JSON'
2. CRUD based on database with ORM
3. Authentication & Authorization with Edit,Delete and Create Function
4. Third Party OAuth2 Login : Google_Plus
```

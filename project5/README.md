# Fullstack-Udacity: Item Catalog

## Requirements
- python 2.7.10
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

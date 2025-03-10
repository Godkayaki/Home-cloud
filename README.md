# Home-Cloud

## Requirements
- Python3.x or more: https://www.python.org/downloads/
- Flask==2.2.3
- Flask_WTF==1.1.1
- Werkzeug==2.2.3
- WTForms==3.0.1


## What is this
A custom-made home cloud storage application build with Python and flask.

## To-do list
- [x] Show current directory
- [x] Add the option to change the root where the cloud is reading.
- [ ] Add the option to download specific content.
  - [x] Option to download ALL content.
  - [ ] Make it so the download otion only applies for the files in the current directory.
- [ ] Better looking GUI.
  - [x] Fix long-name fitting for files/folders.
  - [x] Add folder icon.
  - [x] Add thumbnails.
  - [x] Add bootstrap.
  - [ ] Make it more stylish in general.
- [x] Dockerize application.

## Run it with docker
Although not recommendable, since currently the path being read is from where the application is running, it's setted up so you can run it with docker;
```
docker build -t flask-home-cloud . 
docker run -p 5000:5000 flask-home-cloud
```
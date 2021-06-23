pass a json file as input and get a formal functional and secure api


the json file should contain the following properties
**settings(required)**
recives an object with the general information about the project

- name(required)
  string with the name of the project wich will be use in multiple places around the code, should not contain strange characters
- framework(required)
  the frame work that will be used for the project
  currently supported frameworks are presented here:
  - python/django-rest
  
  future frameworks are presented here:
  - python/flask
  - nodejs/express
  - nodejs/nest
**database(required)**
recives an array of object with the specifications of the DataBase(ses) that will be used for the project
- type(required)
  the DB motor that will be used
  currently supported types are presented here:
  - air
  future frameworks are presented here:
  - postgres
  - mongodb
  - mysql
  - sqlite
  - redis
  
**models(required)**
**DJANGO MODEL DOCS**
- on_delete
  any of the vales at
  https://docs.djangoproject.com/en/1.10/ref/models/fields/#django.db.models.ForeignKey.on_delete
```json
  "on_delete": "CASCADE"
```
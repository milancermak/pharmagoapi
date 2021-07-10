# pharmagoapi
PharmaGO Django APP API

#### Database configuration ####

Local setup uses postgres as database. You have to be sure it is
installed.

```
#!shell
sudo apt-get install postgresql
```

create pharmago user (password: pharmago)

```
#!shell
sudo -u postgres createuser -P pharmago
```

Allow user to create databases (used by test suite):
```
#!shell
sudo -u postgres psql -c 'alter role pharmago with createdb;'
```

create bsurance partners databases

```
#!shell
sudo -u postgres bash -c "createdb pharmago"
```

#### Create tables in database ####

```
#!shell
python manage.py migrate
```


### Bitnami dependency locations

bitnami@ip-172-26-3-232:/opt/bitnami/python/lib/python3.8/site-packages$ 
sudo pip install -r /opt/bitnami/projects/pharmagoapi/requirements.txt -t .
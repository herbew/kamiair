#|==============================================================================
#|          D E P L O Y M E N T   G U I D A N C E with Ubuntu 22.04
#|==============================================================================

sudo apt-get install build-essential checkinstall python3 python3-pip python3-dev python3-setuptools
sudo apt-get install libncursesw5-dev libssl-dev libpq-dev \
    tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev

1.1. INSTALL DATABASE POSTGRES 10
--------------------------------------------------------------------------------
sudo wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -sc)-pgdg main" > /etc/apt/sources.list.d/PostgreSQL.list'

sudo apt update
sudo apt-get install postgresql-10

sudo -u postgres psql -c "CREATE USER ukamiair WITH ENCRYPTED PASSWORD 'PwDkamiairSatu1Dua3';"
sudo -u postgres psql -c "CREATE DATABASE db_kamiair;"

sudo -u postgres psql db_kamiair -c "GRANT ALL ON ALL TABLES IN SCHEMA public to ukamiair;"
sudo -u postgres psql db_kamiair -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA public to ukamiair;"
sudo -u postgres psql db_kamiair -c "GRANT ALL ON ALL FUNCTIONS IN SCHEMA public to ukamiair;"

IF need drop db
sudo -u postgres psql -c "DROP DATABASE db_kamiair;"


2.1. SYSTEM DJANGO ENVIRONMENT
-------------------------------------------------------------------------------

sudo apt install language-pack-id
sudo dpkg-reconfigure locales

sudo apt install -y python3-venv 
sudo apt install pip

python3 -m pip install --user pipenv

git clone  https://github.com/herbew/kamiair.git


IF PRODUCTION
--
ln -s /root/kamiair /opt/kamiair
cd /opt/

python3 -m venv envkamiair

source envkamiair/bin/activate


sudo apt install dos2unix -y 
cd kamiair

dos2unix utilities/install_os_dependencies.sh
dos2unix utilities/install_python_dependencies.sh
sudo ./utilities/install_os_dependencies.sh install

source envkamiair/bin/activate
cd kamiair

sudo -H pip3 install virtualenv
./utilities/install_python_dependencies.sh


TEST
--
assume directory /home/herbew/

source envkamiair/bin/activate
cd kamiair/tests/
pytest -s

OR

cd kamiair/tests/
/home/herbew/envkamiair/bin/pytest -s

SHELL
--
assume the directoris /home/herbew
/home/herbew/envkamiair/bin/python3 kamiair/manage.py shell

CREATE Super Admin
--
from kamiair.apps.masters.models.users import User
user = User(username='herbew')
user.name = "Heribertus Rustyawan"
user.email = "herbew@gmail.com"
user.set_password("password")
user.is_active = True
user.save()

UPDATE AS admin
--
user.roles = '00000'
user.save()




RUN
--
assume the directoris /home/herbew
/home/herbew/envkamiair/bin/python3 run.py

 * Serving Flask app 'run'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://192.168.0.155:8080
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 105-089-458


3. SETUP GUNICORN
--------------------------------------------------------------------------------
pip install -r requirements/production.txt

gunicorn --bind 0.0.0.0:8080 wsgi:app

[2023-06-26 03:28:13 +0000] [1595] [INFO] Starting gunicorn 20.1.0
[2023-06-26 03:28:13 +0000] [1595] [INFO] Listening at: http://127.0.0.1:8000 (1595)
[2023-06-26 03:28:13 +0000] [1595] [INFO] Using worker: sync
[2023-06-26 03:28:13 +0000] [1596] [INFO] Booting worker with pid: 1596


sudo vi /etc/systemd/system/gunicorn.service

# Assume the user 'herbew'
# Assume the project directory '/home/herbew/kamiair'
# Assume the environment project directory '/home/herbew/envkamiair/bin'

-------------------------------------------------------------------------------
[Unit]
Description=Gunicorn instance to serve kamiair
After=network.target

[Service]
User=herbew
Group=www-data
WorkingDirectory=/home/herbew/kamiair
Environment="PATH=/home/herbew/envkamiair/bin"
ExecStart=/home/herbew/envkamiair/bin/gunicorn --access-logfile - --workers 3 --bind unix:flask.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
-------------------------------------------------------------------------------

sudo systemctl start gunicorn

# Generate sock 'unix:flask.sock' or beed changed and activated the workers
sudo systemctl enable gunicorn	

Created symlink /etc/systemd/system/multi-user.target.wants/gunicorn.service → /etc/systemd/system/gunicorn.service.

sudo systemctl status gunicorn

--
● gunicorn.service - Gunicorn instance to serve kamiair
     Loaded: loaded (/etc/systemd/system/gunicorn.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2023-06-26 03:55:07 UTC; 45s ago
   Main PID: 1776 (gunicorn)
      Tasks: 4 (limit: 1012)
     Memory: 60.0M
        CPU: 273ms
     CGroup: /system.slice/gunicorn.service
             ├─1776 /home/herbew/envkamiair/bin/python3 /home/herbew/envkamiair/bin/gunicorn --access-logfile - --workers 3 --bind unix:flask.sock -m>
             ├─1777 /home/herbew/envkamiair/bin/python3 /home/herbew/envkamiair/bin/gunicorn --access-logfile - --workers 3 --bind unix:flask.sock -m>
             ├─1778 /home/herbew/envkamiair/bin/python3 /home/herbew/envkamiair/bin/gunicorn --access-logfile - --workers 3 --bind unix:flask.sock -m>
             └─1779 /home/herbew/envkamiair/bin/python3 /home/herbew/envkamiair/bin/gunicorn --access-logfile - --workers 3 --bind unix:flask.sock -m>

Jun 26 03:55:07 fub2204 systemd[1]: Started Gunicorn instance to serve kamiair.
Jun 26 03:55:07 fub2204 gunicorn[1776]: [2023-06-26 03:55:07 +0000] [1776] [INFO] Starting gunicorn 20.1.0
Jun 26 03:55:07 fub2204 gunicorn[1776]: [2023-06-26 03:55:07 +0000] [1776] [INFO] Listening at: unix:flask.sock (1776)
Jun 26 03:55:07 fub2204 gunicorn[1776]: [2023-06-26 03:55:07 +0000] [1776] [INFO] Using worker: sync
Jun 26 03:55:07 fub2204 gunicorn[1777]: [2023-06-26 03:55:07 +0000] [1777] [INFO] Booting worker with pid: 1777
Jun 26 03:55:07 fub2204 gunicorn[1778]: [2023-06-26 03:55:07 +0000] [1778] [INFO] Booting worker with pid: 1778
Jun 26 03:55:07 fub2204 gunicorn[1779]: [2023-06-26 03:55:07 +0000] [1779] [INFO] Booting worker with pid: 1779
--

ps ax |grep py

--
648 ?        Ss     0:00 /usr/bin/python3 /usr/bin/networkd-dispatcher --run-startup-triggers
708 ?        Ssl    0:00 /usr/bin/python3 /usr/share/unattended-upgrades/unattended-upgrade-shutdown --wait-for-signal
1776 ?        Ss     0:00 /home/herbew/envkamiair/bin/python3 /home/herbew/envkamiair/bin/gunicorn --access-logfile - --workers 3 --bind unix:flask.sock -m 007 wsgi:app
1777 ?        S      0:00 /home/herbew/envkamiair/bin/python3 /home/herbew/envkamiair/bin/gunicorn --access-logfile - --workers 3 --bind unix:flask.sock -m 007 wsgi:app
1778 ?        S      0:00 /home/herbew/envkamiair/bin/python3 /home/herbew/envkamiair/bin/gunicorn --access-logfile - --workers 3 --bind unix:flask.sock -m 007 wsgi:app
1779 ?        S      0:00 /home/herbew/envkamiair/bin/python3 /home/herbew/envkamiair/bin/gunicorn --access-logfile - --workers 3 --bind unix:flask.sock -m 007 wsgi:app
1859 pts/0    S+     0:00 grep --color=auto py
--
	
	
4. SETUP NGINX
--

sudo apt install nginx

sudo cp -f /home/herbew/kamiair/configs/nginx/local-nginx.conf /etc/nginx/sites-available/kamiair
sudo ln -s /etc/nginx/sites-available/kamiair /etc/nginx/sites-enabled

sudo nginx -t

--
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
--

sudo service nginx configtest

sudo systemctl enable nginx
sudo systemctl start nginx
sudo systemctl restart nginx
sudo systemctl daemon-reload
sudo systemctl status nginx


sudo systemctl restart gunicorn
sudo systemctl restart nginx

IF ANY error
--
2023/06/26 04:47:43 [notice] 2779#2779: using inherited sockets from "6;7;"
2023/06/26 04:55:20 [crit] 3205#3205: *2 connect() to unix:/home/herbew/kamiair/flask.sock failed (13: Permission denied) while connecting to upstream, client: 192.168.0.186, server: localhost, request: "GET / HTTP/1.1", upstream: "http://unix:/home/herbew/kamiair/flask.sock:/", host: "192.168.0.155:8080"

with sock files:
--
srwxrwx---  1 herbew www-data    0 Jun 26 05:02 flask.sock


assume account is 'herbew'

sudo vi /etc/nginx/nginx.conf
--
#user www-data;
user herbew;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;
...

5. FLASK CONFIGURATION
--
# Assume the project directory '/home/herbew/kamiair'
cp -f /home/herbew/kamiair/default.env /home/herbew/kamiair/.env


6. BABEL TRANSLATIONS SETUP & COMPILE
--
- https://flask-babelplus.readthedocs.io/en/latest/
- messages/babel.cfg
  -----------------------------------------------------------------------
  1. pybabel extract -F babel.cfg -o messages.pot .
  This, collect all babel in script as master messages.pot
  
  2. pybabel init -i messages.pot -d translations -l id
  Copy the message.pot to translations/id/LC_MESSAGES/messages.po
  
  3. Update the translations/de/LC_MESSAGES/messages.po as language id
  translate word, senteces, to Bahasa.
  
  4. pybabel compile -d translations
  
  5. Update master messages.pot
  pybabel update -i messages.pot -d translations
  -----------------------------------------------------------------------
  
  


7. REDIS
--
https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-22-04
sudo apt install redis-server


sudo systemctl enable redis-server
sudo systemctl start redis
sudo systemctl restart redis
sudo systemctl daemon-reload
sudo systemctl status redis



8. RQWORKER
--
sudo vi /etc/systemd/system/rqworker.service

# Assume the user 'herbew'
# Assume the project directory '/home/herbew/kamiair'
# Assume the environment project directory '/home/herbew/envkamiair/bin'

-------------------------------------------------------------------------------
[Unit]
Description=RQ2 Worker instance to serve kamiair
After=network.target

[Service]
User=herbew
Group=www-data
WorkingDirectory=/home/herbew/kamiair
Environment="PATH=/home/herbew/envkamiair/bin"
ExecStart=/home/herbew/envkamiair/bin/python3 manage.py rqworker --low=low --simple=simple --critical=critical
StandardOutput=append:/tmp/kamiair_rqworker.log
StandardError=append:/tmp/kamiair_rqworker_error.log

[Install]
WantedBy=multi-user.target
-------------------------------------------------------------------------------
sudo systemctl daemon-reload
sudo systemctl start rqworker
sudo systemctl enable rqworker	
sudo systemctl status rqworker


9.SUPERUSER
--
cd message
/home/herbew/envkamiair/bin/python3 manage.py shell

from kamiair.apps.masters.models.users import User
from kamiair.apps.crawlers.models.users import UserCrawler

u = User()
u.username="herbew"
u.password_portal("#!herbew!!23")
u.email="herbew.3l@gmail.com"
u.save()

u.set_password("password")
u.save()

uc = UserCrawler()
uc.user = u
uc.is_authorized = False
uc.save()











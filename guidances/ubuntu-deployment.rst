#|==============================================================================
#|          D E P L O Y M E N T   G U I D A N C E with Ubuntu 22.04
#|==============================================================================

sudo apt-get install build-essential checkinstall python3 python3-pip python3-dev python3-setuptools
sudo apt-get install libncursesw5-dev libssl-dev libpq-dev \
    tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev

1.1. INSTALL DATABASE POSTGRES 
--------------------------------------------------------------------------------
sudo apt update
sudo apt install postgresql postgresql-contrib

sudo -u postgres psql -c "CREATE USER ukamiair WITH ENCRYPTED PASSWORD 'PwDkamiairSatu1Dua3';"
sudo -u postgres psql -c "CREATE DATABASE db_kamiair;"


sudo -u postgres psql db_kamiair -c "GRANT ALL PRIVILEGES ON DATABASE db_kamiair TO ukamiair;"
sudo -u postgres psql db_kamiair -c "GRANT ALL ON SCHEMA public TO ukamiair;"
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

CLONE & COPY .env
--
git clone  https://github.com/herbew/kamiair.git
cd kamiair
cp env_default.env .env



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


MAKEMIGRATIONS & MIGRATE
--
source envkamiair/bin/activate
cd kamiair/

python3 manage.py makemigrations users
python3 manage.py makemigrations masters

python3 manage.py migrate sites
python3 manage.py migrate users
python3 manage.py migrate masters

python3 manage.py migrate

COLLECT STATIC FOLDER
--
source envkamiair/bin/activate
cd kamiair/

python3 manage.py collectstatic


LOAD DATA
--
python3 manage.py loaddata 001_users_user
python3 manage.py loaddata 002_account_emailaddress

python3 manage.py loaddata 003_masters_airlines



SUPER USER if needed 
--
source envkamiair/bin/activate
cd kamiair/

python manage.py createsuperuser
admin
password







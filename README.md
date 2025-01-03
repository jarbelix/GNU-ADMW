# What is GNU-ADMW

GNU-ADMW is an Active Directory Management Web in a GNU GENERAL PUBLIC LICENSE

# Introduction

This project is a Web Interface for Active Directory made using **Django** (https://www.djangoproject.com/) and **ms_active_directory** (https://ms-active-directory.readthedocs.io/) focusing on ease of use and simplicity provide by **Bootstrap** (https://getbootstrap.com/)

It's using the connecting user's credentials to connect to the directory and allow a variety of operations.

The goal is to be able to do most common directory operations directly through this web interface rather than have to rely on command tools or Windows interfaces.

It's compatible with both **Windows Active Directory** and **Samba4** domain controllers.

If you don't know how to install samba4 see https://wiki.tiozaodolinux.com/Guide-for-Linux/Active-Directory-With-Samba-4

# History

This project started in december 2024 with objetive of simplify the management of Users, Groups, Lists, Organizatinal Units

In my job we have the RH area with demands to NOC area create new Users, reset password Users, etc

The main objetive is RH area make yours needs without NOC area dependencies

# Install and run

```sh
# Download clone project
git clone https://github.com/jarbelix/GNU-ADMW.git
cd GNU-ADMW

# Create virtualenvironment
python -m venv .venv
. .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Setup Environment

Copy the env.example file to .env and udpate the settings to match your environment.

```sh
cp env.example .env
```

## Initial testing

### Config .env

```sh
python test-config-env.py
```

### Connection to Active Directory

```sh
python test-active-directory.py
```
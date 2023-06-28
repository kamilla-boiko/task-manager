# Task Manager

Django project for managing and handle all possible problems during product development in team

## Installation

Python3 must be already installed

```shell
git clone https://github.com/kamilla-boiko/task-manager.git
cd task-manager
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver  # starts Django Server
```

Use the following command to load prepared data from fixture:

`python manage.py loaddata dashboard_db_data.json`

## Environment variables

This project uses environment variables to store sensitive or configurable data.
The variables are stored in a file named .env, which should be created in the
project's root directory.
Please follow the instructions below to set up the environment variables for your local development.

### .env file

Create a file named .env in the root directory of the project and add the following variables
with their corresponding values:

```SECRET_KEY=your_secret_key_here```

Replace your_secret_key_here with the actual values for your environment variables.

* Note: Make sure to keep the .env file secure and do not commit it to the repository.

### .env_sample file

A file named .env_sample is included in the repository as a template for setting up the .env file.
It contains the names of the environment variables without their values.
You can use it as a reference when creating your own .env file.

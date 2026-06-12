# Dotster

A lightweight platform for deploying and managing Docker applications on Kubernetes.

## Features

- Deploy applications using Docker image URLs
- Configure minimum and maximum replicas
- Auto-generate Kubernetes deployment configurations
- Rebuild existing deployments
- Clone applications
- Update deployment settings
- Delete deployments
- User-specific application management

## Tech Stack

- Python
- Django
- Kubernetes
- Docker
- SQLite (default Django database)

## Application Configuration

Each application stores:

- Application name
- Description
- Docker image URL
- Port
- Minimum replicas
- Maximum replicas
- Current running instances

## Setup

```bash
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

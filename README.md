# Reservation System Development Environment 🚀

![Docker](https://img.shields.io/badge/Docker-required-blue?logo=docker)
![Docker Compose](https://img.shields.io/badge/Docker_Compose-required-blue?logo=docker)
![Status](https://img.shields.io/badge/Status-Development-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

This development environment configures all the services needed to work on the cloud resource reservation system, including:
- 🖥️ React Frontend (reservation-fe)
- 🔌 Backend (reservation-be)
- 🔑 Keycloak for authentication
- 🗄️ PostgreSQL for databases

## Requirements ⚙️

- 🐳 Docker
- 🔄 Docker Compose

## Project Structure 📂

```
project-root/
├── docker-compose.yml           # Docker Compose configuration
├── init-multiple-postgres-dbs.sh # Database initialization script
├── keycloak/
│   └── import/
│       └── resource-management-realm.json # Keycloak realm configuration
├── reservation-fe/              # Frontend source code
└── reservation-be/              # Backend source code
```

## Getting Started 🚦

### Setup Instructions 📝

1. Make sure the `reservation-fe` and `reservation-be` folders contain the respective source code
2. Make the database initialization script executable:
   ```bash
   chmod +x init-multiple-postgres-dbs.sh
   ```
3. Modify your hosts file to redirect "backend" and "keycloak" to your local machine:
   - For Linux/macOS:
     ```bash
     sudo nano /etc/hosts
     ```
     Add these lines:
     ```
     127.0.0.1 backend
     127.0.0.1 keycloak
     ```
     Save the file (Ctrl+O, then Enter) and exit (Ctrl+X)
     
   - For Windows:
     - Open Notepad as Administrator
     - Open the file `C:\Windows\System32\drivers\etc\hosts`
     - Add these lines:
       ```
       127.0.0.1 backend
       127.0.0.1 keycloak
       ```
     - Save the file
     
4. Start the development environment:
   ```bash
   docker-compose up -d
   ```
5. The services will be available at the following addresses:
   - 🌐 Frontend: http://localhost:3000
   - 🔌 Backend API: http://localhost:8080/api
   - 🔑 Keycloak: http://localhost:8180
   - 🗄️ PostgreSQL Database: localhost:5432

After starting the containers with Docker Compose and ensuring all services are running properly, you can access the application using a bootstrap admin account:

- 🔗 **URL:** http://localhost:3000
- 👤 **Username:** admin
- 🔒 **Password:** password
  
## Demo Access 🌟

A demo version of the application is available at:
- 🔗 **URL:** https://204.216.215.139/
- 👤 **Username:** admin
- 🔒 **Password:** password

## Access Credentials 🔐

### Keycloak Admin Console
- 🌐 URL: http://localhost:8180/admin
- 👤 Username: admin
- 🔒 Password: admin

### Default Users
1. Administrator:
   - 👤 Username: admin
   - 🔒 Password: password
   - 📧 Email: mario.rossi@example.com
   - 🎭 Roles: admin, user

## Configuration ⚙️

The frontend is configured to automatically connect to the backend and Keycloak with the following settings:
- 🔌 Backend API: http://localhost:8080/api
- 🔑 Keycloak: http://localhost:8180
- 🏰 Realm: resource-management
- 🆔 Client ID: resource-management-app

## Kubernetes Deployment with Helm ☸️

A Helm chart is available for deploying this application on Kubernetes. You can find the chart and instructions in the following repository:

- [reservation-helm-chart](https://github.com/giovannimirarchi420/reservation-helm-chart)

## Troubleshooting ⚠️

### Permission errors
If you encounter permission errors when starting the containers:
```bash
sudo chown -R $USER:$USER reservation-fe reservation-be keycloak
chmod -R 755 reservation-fe reservation-be keycloak
```

### Cleaning the environment
To stop and remove all containers, networks, and volumes:
```bash
docker-compose down -v
```

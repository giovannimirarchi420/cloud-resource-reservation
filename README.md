# Reservation System Development Environment

Questo ambiente di sviluppo configura tutti i servizi necessari per lavorare sul sistema di prenotazione risorse cloud, inclusi:
- Frontend React (reservation-fe)
- Backend (reservation-be)
- Keycloak per l'autenticazione
- PostgreSQL per i database

## Requisiti

- Docker
- Docker Compose

## Struttura del progetto

```
project-root/
├── docker-compose.yml           # Configurazione Docker Compose
├── init-multiple-postgres-dbs.sh # Script inizializzazione database
├── keycloak/
│   └── import/
│       └── resource-management-realm.json # Configurazione realm Keycloak
├── reservation-fe/              # Codice sorgente frontend
└── reservation-be/              # Codice sorgente backend
```

## Istruzioni per l'avvio

1. Assicurati che le cartelle `reservation-fe` e `reservation-be` contengano il codice sorgente rispettivo
2. Rendi eseguibile lo script di inizializzazione del database:
   ```bash
   chmod +x init-multiple-postgres-dbs.sh
   ```
3. Avvia l'ambiente di sviluppo:
   ```bash
   docker-compose up -d
   ```
4. I servizi saranno disponibili ai seguenti indirizzi:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8080/api
   - Keycloak: http://localhost:8180
   - Database PostgreSQL: localhost:5432

## Credenziali di accesso

### Keycloak Admin Console
- URL: http://localhost:8180/admin
- Username: admin
- Password: admin

### Utenti predefiniti
1. Amministratore:
   - Username: admin
   - Password: password
   - Email: mario.rossi@example.com
   - Ruoli: admin, user

2. Utente standard:
   - Username: user
   - Password: password
   - Email: luigi.bianchi@example.com
   - Ruoli: user

## Configurazione

Il frontend è configurato per connettersi automaticamente al backend e a Keycloak con le seguenti impostazioni:
- API Backend: http://localhost:8080/api
- Keycloak: http://localhost:8180
- Realm: resource-management
- Client ID: resource-management-app

## Risoluzione problemi

### Backend non disponibile
Se il backend non si avvia correttamente, potrebbe essere necessario modificare il comando di avvio nel `docker-compose.yml` in base alla struttura effettiva del progetto backend:

Per un progetto Maven:
```yaml
command: sh -c "./mvnw spring-boot:run -Dspring-boot.run.profiles=dev"
```

Per un progetto Gradle:
```yaml
command: sh -c "./gradlew bootRun --args='--spring.profiles.active=dev'"
```

### Errori di permessi
Se riscontri errori di permessi durante l'avvio dei container:
```bash
sudo chown -R $USER:$USER reservation-fe reservation-be keycloak
chmod -R 755 reservation-fe reservation-be keycloak
```

### Pulizia ambiente
Per fermare e rimuovere tutti i container, le reti e i volumi:
```bash
docker-compose down -v
```

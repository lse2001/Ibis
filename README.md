# Ibis Odoo Sales Order Notification Service

## Overview

This project is a lightweight Python integration service that connects to an Odoo ERP sandbox instance through XML-RPC, retrieves qualifying confirmed sales orders, generates consolidated Part Summaries from related order line data, and sends Gmail notifications for newly discovered orders.

The service continuously polls the Odoo instance every 60 seconds and prevents duplicate notifications by tracking previously processed orders in a local JSON state file.

---

# Features

- Authenticates against an Odoo sandbox instance using XML-RPC
- Retrieves confirmed sales orders from the last 48 hours
- Filters orders that contain customer PO numbers
- Retrieves and processes associated `sale.order.line` records
- Generates consolidated Part Summaries
- Sends Gmail notifications for newly confirmed orders
- Prevents duplicate email notifications across polling cycles
- Dockerized deployment using Docker Compose
- Environment-variable based credential management

---

# Environment & Security

This project follows the required deployment/security standards:

- Dockerized using `Dockerfile` and `docker-compose.yml`
- Credentials are stored securely in a `.env` file
- No Odoo or Gmail credentials are hardcoded
- Runtime logs are available through:

```bash
docker compose logs -f
```

---

# Odoo Relational Data Handling

Odoo stores sales order data across two related models:

- `sale.order`
- `sale.order.line`

A single `sale.order` can contain multiple `sale.order.line` records representing individual quoted products/components.

Example:

```text
SO1002
├── 2x Thermal Bracket
└── 1x Composite Panel
```

The service retrieves all associated order line records for each qualifying sales order and consolidates them into a single readable Part Summary.

Additionally, imported CSV sandbox/demo data may produce duplicate sales order records where each imported row contains only one quoted component. To handle both structures consistently, the application normalizes orders by grouping records using:

- internal sales order reference
- customer PO number

This allows the service to generate one consolidated Part Summary regardless of how the Odoo data was imported.

---

# Project Structure

```text
.
├── app/
│   ├── config.py
│   ├── emailer.py
│   ├── main.py
│   └── odoo_client.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── .gitignore
└── README.md
```

---

# Setup

## 1. Clone Repository

```bash
git clone <repository-url>
cd <repository-name>
```

---

## 2. Create .env File

Create a `.env` file in the project root:

```env
ODOO_URL=https://your-odoo-instance-url
ODOO_DB=your_database_name
ODOO_USERNAME=your_odoo_username
ODOO_PASSWORD=your_odoo_api_key

GMAIL_SENDER=your_email@gmail.com
GMAIL_APP_PASSWORD=your_gmail_app_password
GMAIL_RECIPIENT=test_recipient@gmail.com
```

---

# Docker Deployment

# Docker Deployment

## Build Container

```bash
docker compose build
```

Builds the Docker image using the project's Dockerfile.

---

## Run Service

Background mode:

```bash
docker compose up -d
```

Starts the polling service in detached/background mode.

---

## View Logs

```bash
docker compose logs -f
```

Streams live application logs, including:
- Odoo authentication status
- matching sales orders
- Gmail notification activity
- polling cycle status
- processing errors

---

## Check Running Containers

```bash
docker compose ps
```

Displays the current status of running containers.

---

## Restart Service

```bash
docker compose restart
```

Restarts the running polling service container.

---

## Stop Service

```bash
docker compose down
```

Stops and removes the running containers.

---

## Rebuild Container After Code Changes

```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

Rebuilds the image from scratch after modifying application code or Docker configuration files.

---

## Execute Commands Inside Container

```bash
docker compose exec ibis-app bash
```

Opens an interactive shell inside the running container for debugging and inspection.

Example:

```bash
cat processed_orders.json
```

---

# Notification Workflow

The service polls the Odoo sandbox every 60 seconds.

For each qualifying confirmed order:

1. Retrieve associated order lines
2. Generate consolidated Part Summary
3. Check local JSON state tracking
4. Send Gmail notification if order has not already been processed
5. Record processed order key to prevent duplicate notifications

Processed orders are tracked using:

```text
Order Reference + Customer PO Number
```

Example:

```text
SO1002|PO-77102
```

---

# Dependencies

```text
python-dotenv
```
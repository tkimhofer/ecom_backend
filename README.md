[![Docker Compose CI](https://github.com/tkimhofer/ecom_backend/actions/workflows/main.yml/badge.svg)](https://github.com/tkimhofer/ecom_backend/actions/workflows/main.yml)

# Scalable Cloud E-commerce Backend and Data Warehouse Integration

Backend API for e-commerce operations, with Docker Compose for Local Development.

Built with FastAPI and asynchronous Python, this backend handles requests efficiently while using minimal resources. It’s containerized with Docker for easy deployment and scaling in cloud environments.

The system stores transactional data in an operational database designed for quick and reliable order processing. It also connects to data warehouse platforms like Google Cloud BigQuery to support reporting and business insights.

The design focuses on simplicity and flexibility to meet core e-commerce backend needs.

## Key Features

- User authentication and token-based authorization
- High concurrency support leveraging asynchronous Python with FastAPI for efficient request handling
- Containerized deployment (Docker) enabling easy scaling and cloud-native operations
- Order ingestion, validation, and retrieval, with data staged in operational databases
- ETL workflows scheduled to transfer data into layered data warehouse systems (e.g., Google Cloud DWH)
- Webhook authentication to securely communicate with external services
- Planned expansions for integration with fulfillment and other 3rd-party services


## Tech Stack & Architecture

- FastAPI for asynchronous Python backend
- SQLAlchemy for database ORM and transaction management
- Containerization and scalable deployment
- OAuth2 / JWT for secure authentication and authorization
- Postgresql for raw order data storage and processing
- Scheduled ETL processing for data warehouse integration (e.g. BigQuery / Google Cloud Platform)
- Designed with microservices readiness / enabling components to be developed, deployed, and scaled independently
- Utilizes OOP encapsulation to promote modularity and maintainability



## Installation & Setup

1. Clone the repository:
git clone https://github.com/tkimhofer/ecom_backend.git
```bash
cd ecom_backend
```

2. Set up a Python virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure environment variables for DB connection strings, secret keys, etc.


4. Run the application locally with Docker Compose (development mode):
```bash
docker-compose up --build
```

5. To stop the services
```bash
docker-compose down
```


## Usage

- API accessible at http://localhost:8000

- Swagger doc: http://localhost:8000/docs

## API Endpoints Overview

- POST /token — User login, returns JWT token
- GET /me — Fetch info of current authenticated user
- GET /health — API health check endpoint
- POST /raw-orders — Ingest raw order data asynchronously
- GET /raw-orders/{uid} — Retrieve raw order details by ID


## Project Status

This project is in early development and gradually maturing.

## Contribution

Contributions, feature requests, and feedback are welcome. Feel free to open issues or pull requests.

## Contact

tkimhofer@gmail.com

GitHub: https://github.com/tkimhofer/ecom_backend

## License

MIT License — see LICENSE file.



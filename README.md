# E-commerce Backend

Backend API for e-commerce operations, built to handle high concurrency and scalable workloads. Designed to receive API requests from frontend clients, process order data, and integrate seamlessly with operational databases and data warehouses.

## Key Features

- User authentication and token-based authorization

- High concurrency support leveraging asynchronous Python with FastAPI for efficient request handling

- Containerized deployment (Docker) enabling easy scaling and cloud-native operations

- Order ingestion, validation, and retrieval, with data staged in operational databases

- ETL workflows scheduled to transfer data into layered data warehouse systems (e.g., Google Cloud DWH)

- Webhook authentication to securely communicate with external services

- Planned expansions for integration with fulfillment and other 3rd-party services


Tech Stack & Architecture

- FastAPI for a modern, fast asynchronous Python backend

- SQLAlchemy for database ORM and transaction management

- Docker for containerization and scalable deployment

- OAuth2 / JWT for secure authentication and authorization

- Operational DB (e.g., PostgreSQL) for raw order data storage and processing

- Data Warehouse (e.g., Google Cloud BigQuery) for analytics and BI workflows

- Designed with microservices readiness and API-first principles



## Installation & Setup

1. Clone the repository:
git clone https://github.com/tkimhofer/ecom_backend.git
cd ecom_backend

2. Set up a Python virtual environment and install dependencies:
python3 -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirements.txt

3. Configure environment variables for DB connection strings, secret keys, etc.

4. Run the application locally (development mode):
uvicorn main:app --reload

4. For containerized deployment:
docker build -t ecom_backend .
docker run -p 8000:8000 ecom_backend

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

This project is currently in early development / early maturity. Features and integrations are actively evolving, including enhancements to support fulfillment services and advanced data workflows.

## Contribution

Contributions, feature requests, and feedback are welcome. Feel free to open issues or pull requests.

## Contact

Torben Kimhofer — tkimhofer@gmail.com

GitHub: https://github.com/tkimhofer/ecom_backend

## License

MIT License — see LICENSE file.



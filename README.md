# Finance Tracker Backend

A robust backend service for tracking financial transactions and managing personal finances.

## 📋 Overview

This project provides a RESTful API for the Finance Tracker application, allowing users to track their expenses, income, and financial goals.

## 🛠️ Technologies

- Python
- Django and Django REST Framework
- Docker
- PostgreSQL
- Swagger/OpenAPI for documentation

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- Docker
- Docker Compose

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/tkach-v/finance-tracker-be.git
cd finance-tracker-be
```

### 2. Configure Environment Variables

Create a `.env` file in the project root directory:

### 3. Launch the Application

Start the service using Docker Compose:

```bash
docker-compose up
```

The API will be available at: http://localhost:8000

## 📚 API Documentation

When running in development mode, API documentation is available at:

- Swagger UI: http://localhost:8000/docs/
- ReDoc: http://localhost:8000/docs/redoc/

## 💻 Development

### Code Quality Tools

This project uses:
- Ruff for linting
- Black for code formatting
- isort for import sorting

These are configured as pre-commit hooks to ensure code quality.

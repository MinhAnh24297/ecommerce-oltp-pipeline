# Project 03: E-commerce OLTP Synthetic Data Pipeline

## Project Objective
The goal of this project is to build a robust Python-based data engineering pipeline that generates **relationally consistent synthetic data** for an E-commerce OLTP (Online Transaction Processing) system and loads it into a **PostgreSQL** database.

## Project Structure
This project follows the **Poetry src-layout** convention:

```text
project3_poetry/
├── src/
│   └── project3_poetry/    # Core Package
│       ├── config.py       # DB Configuration parser
│       ├── connect.py      # Connection establishment logic
│       ├── insert.py       # Main script for data insertion
│       └── create_tables.py# Table schema definitions
├── tests/                  # Unit tests
├── pyproject.toml          # Dependencies & metadata
├── poetry.lock             # Frozen dependency versions
└── README.md
```

## Prerequisites
- Python 3.10+
- Poetry
- PostgreSQL

## Setup & Installation
### 1. Initialize the Environment:
Run this in the root directory to build your virtual environment:
```text
poetry install
```
### 2. Configure Database:
Ensure your **database.ini** file is in the root directory with the following format:
```text
[postgresql]
host=localhost
database=e_commerce
user=your_user
password=your_password
```

## Usage
To run the scripts within the isolated Poetry environment, use the following commands:
### 1.To create the tables:
```text
poetry run python src/project3_poetry/create_tables.py
```
### 2. To insert synthetic data (using Faker):
```text
poetry run python src/project3_poetry/insert.py
```

## Key Dependencies
- psycopg2: PostgreSQL adapter for Python.
- Faker: For generating realistic test data (names, dates, brands).
# Data Commons: FastAPI Backend

## Overview

Data Commons is a web application using a fastAPI backend.

## Features

- **Authentication**: Users can log in and log out. Unauthorized access to specific routes is prevented.
- **Dataset Management**: Manage datasets with options to view all datasets or a single dataset.
- **Patient Management**: View and manage patient information.
- **Project Management**: View all projects or a single project, with a dashboard overview.
- **Responsive Design**: The application is designed to be responsive, providing a good user experience across different devices.


## Project Structure
```plaintext
REDMANE_fastapi/
├── app/
│   │   ├── __init__.py             # Initializes the API package
│   │   └── routes.py               # Defines API endpoints
│   ├── schemas/
│   │   ├── __init__.py             # Initializes the schemas package
│   │   └── schemas.py              # Defines Pydantic models for data validation
│   └── main.py                     # Entry point for the FastAPI application
├── data/
│   ├── REDMANE_fastapi_public_data/
│   │   ├── readmedatabase.sql      # PostgreSQL to set up database
│   ├── sample_data/                # Sample datasets and scripts for testing
│   │   ├── clear_patients_and_samples.sh  # Script to clear sample data
│   │   ├── import_onj_patients.py  # Script to import ONJ patients
│   │   ├── import_onj_samples.py   # Script to import ONJ samples
│   │   ├── import_rmh_patients.py  # Script to import RMH patients
│   │   ├── redcap_onj.csv          # Sample ONJ patient data
│   │   ├── redcap_onj_samples.csv  # Sample ONJ sample data
│   │   └── redcap_rmh.csv          # Sample RMH patient data
│   └── sample_files/               # Sample files for raw data tracking
│       └── tracker/                # Folder for tracking scripts and raw data
│           ├── scrnaseq/raw/       # scRNA-seq raw data files
│           │   └── random_file_2.fastq   # Example FASTQ file
│           └── westn/raw/          # WES raw data files
│               ├── *.fastq         # Example FASTQ files for testing
│               ├── create_counts_file_big.py  # Script for processing large count files
│               ├── create_counts_file_size.py # Script for calculating file size
│               ├── create_fastq_size.py       # Script for FASTQ size processing
│               └── file_report.py  # Script for generating file reports
├── data_redmane.db                 # SQLite database file
├── LICENSE                         # Project license
├── README.md                       # Project documentation
├── .gitignore                      # Git ignore file
└── .DS_Store
```

## Installation

### Database Creation

1. Make sure you have installed PostgreSql on your device
2. Login in to your own account in psql shell
3. In psql interface type:
   ````bash
   CREATE DATABASE readmedatabase;
   CREATE USER username WITH PASSWORD 'password';
   GRANT ALL PRIVILEGES ON DATABASE mydatabase TO username;
   GRANT ALL ON SCHEMA public TO username;
   ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO username;
   ````
   
   

### Setup Instructions

1. **Create a python virtual environment:**

   ```bash
   python3 -m venv env
   ```

2. **Install Libraries:**

   Using npm:
   ```bash
   pip install fastapi uvicorn psycopg2
   ```

3. **Run server:**

   Connect to venv
   ```bash
   source env/bin/activate
   ```

   ```bash
   uvicorn app.main:app --reload --port 8888
   ```
=======
https://github.com/WEHI-ResearchComputing/REDMANE_nuxt


# Public data

Go to [REDMAME_fastapi_public_data](https://github.com/WEHI-ResearchComputing/REDMANE_fastapi_public_data)


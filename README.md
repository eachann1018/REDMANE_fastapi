# Data Commons: FastAPI Backend

## Overview

Data Commons is a web application using a fastAPI backend.

## Features

- **Authentication**: Users can log in and log out. Unauthorized access to specific routes is prevented.
- **Dataset Management**: Manage datasets with options to view all datasets or a single dataset.
- **Patient Management**: View and manage patient information.
- **Project Management**: View all projects or a single project, with a dashboard overview.
- **Responsive Design**: The application is designed to be responsive, providing a good user experience across different devices.

## Installation

### Setup Instructions

1. **Create a python virtual environment:**

   ```bash
   python3 -m venv env
   ```

2. **Install Libraries:**

   Using npm:
   ```bash
   pip install fastapi uvicorn
   ```

3. **Run server:**

   Using npm:
   ```bash
   uvicorn app.main:app --reload --port 8888
   ```

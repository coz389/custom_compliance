# Custom Compliance

## Project Description

The **Custom Compliance** project is designed to streamline and bring transparency to port operations, specifically focusing on **customs clearance, document verification, and cargo inspection**.

Currently, port authorities and shippers often face a lack of clarity regarding the real-time status of shipments—whether they have cleared customs or if cargo verification is complete. Additionally, there is no centralized system to track the availability of various customs offices, leading to confusion about which offices are busy or free.

This project provides a comprehensive dashboard for shippers to track their shipment status before loading and allows port authorities to manage office workloads and verification processes efficiently.

## Features

- **Role-Based Access Control (RBAC):** Separate permissions and views for Port Authorities, Shippers, and Custom Officers [Conversation History].
- **Real-time Shipment Tracking:** Transparency in cargo and document verification status.
- **Office Management:** Visibility into the workload and availability (Free/Busy) of customs offices.
- **Audit Logging:** Recording all critical actions for compliance and tracking [Conversation History].
- **Soft Delete:** Data integrity maintenance by using soft delete flags instead of hard deletes.

## Tech Stack

- **Backend:** Python 3.11 [Conversation History]
- **Framework:** Django with Django REST Framework (DRF)
- **Authentication:** JWT (JSON Web Tokens) [Conversation History]
- **Database:** PostgreSQL (Recommended) or SQLite

## Installation and Setup

Follow these steps to set up the project locally:

### Step 1: Create a Virtual Environment

Isolate your project dependencies by creating a virtual environment using Python 3.11.

```bash
python -m venv venv
```


### Step 2: Activate The Virtual Environment

Activate the environment to start using the isolated Python interpreter.

- **Windows:**
    ```bash
    .\venv\Scripts\activate
    ```
- **Unix/macOS:**
    ```bash
    source venv/bin/activate
    ```

### Step 3: Install All Packages

Install all necessary libraries and dependencies from the `requirement.txt` file.

```bash
pip install -r requirement.txt
```

### Step 4: Setup your Database

Configure your database connection settings in the `settings.py` file located in the core project directory. Ensure your database server is running.

### Step 5: Navigate to Your Core Project Directory

Move into the directory where the `manage.py` file is located.

```bash
cd your_project_name
```

### Step 6: Run Database Migration Files

Apply migrations to sync your database schema with the Django models.

```bash
python manage.py migrate
```

### Step 7: Run Data Seeder

Populate the database with essential initial data (roles, modules, actions, etc.) using the custom seeder command.

```bash
python manage.py seed_data
```

## Running the Project

To start the development server, run:

```bash
python manage.py runserver
```


# ElectroMap

## Overview
ElectroMap is a system designed to manage and monitor electricity consumption and distribution efficiently in electricity substations. This documentation provides a detailed guide on setting up and running the project on your local machine.

## Prerequisites
Ensure you have the following installed on your system before proceeding:
- Python (>=3.8)
- Git
- pip
- Virtual environment module (venv)

## Setup Instructions

### 1. Clone the Repository
To get started, clone the project repository from GitHub:
```bash
git clone https://github.com/janisadhi/Electricity-load.git
cd Electricity-load
```

### 2. Setting Up the Virtual Environment
Create and activate a virtual environment to manage dependencies separately.

#### For Unix/Linux/macOS:
```bash
python -m venv myvenv
source myvenv/bin/activate
```
#### For Windows:
```bash
python -m venv myvenv
myvenv\Scripts\activate.bat
```

### 3. Install Dependencies and Run the Server
Navigate to the `electro_map` directory and install the required dependencies.
```bash
cd electro_map
pip install -r requirements.txt
```
Run the Django development server:
```bash
python manage.py runserver
```

### 4. Setting Up Data Processing Service
Open a new terminal and navigate back to the project root:
```bash
cd Electricity-load
```
Create and activate another virtual environment:
```bash
python -m venv myvenv
source myvenv/bin/activate
```
#### For Windows:
```bash
myvenv\Scripts\activate.bat
```
Navigate to the `data` directory and install dependencies:
```bash
cd data
pip install -r requirements.txt
```
Start the data processing application:
```bash
python app.py
```

### 5. Accessing the Application
Once both the Django server and the data processing service are running, open your browser and navigate to:
```
https://<your-ip>:8000
```

## Project Structure
```
Electricity-load/
│-- electro_map/         # Django project files
│-- data/                # Data processing scripts
│-- myvenv/              # Virtual environment (generated during setup)
│-- requirements.txt     # Dependencies list
│-- manage.py            # Django project manager
│-- README.md            # Documentation
```





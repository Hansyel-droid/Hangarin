#  Hangarin: To-Do Manager
A clean, functional Django task management system built for Midterm project requirements.

##  Quick Start
Follow these steps to run the project locally:

1. **Setup Environment**
   ```bash
   python -m venv venv
   # Activate (Windows): venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate

python manage.py seed_data      # Optional: Add sample data

python manage.py createsuperuser # For Admin access

python manage.py runserver

Visit: http://127.0.0.1:8000/
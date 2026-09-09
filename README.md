# Blood Donation Platform

**Live Site:** [https://blood-donation-gray.vercel.app/](https://blood-donation-gray.vercel.app/)

A Django‑based blood donation system deployed on Vercel. It connects donors and recipients through a user-friendly interface with templates for donation requests, donor information, and more.

---

##  Features

- Responsive pages such as **Home**, **About**, **Contact**, **Donate**, **News**, and **Required**.
- User interface built with Django templates.
- Django apps: 
  - `blood` — core settings, URLs, views.
  - `panel` — handling models, admin, and business logic.
- Tailored for deployment on Vercel via `vercel_wsgi.py`.
- Database migrations integrated (likely using SQLite or a production-ready DB).
  
---

##  Project Structure

blood/ ← Django project
├── init.py
├── asgi.py
├── settings.py
├── urls.py
├── views.py
└── wsgi.py

panel/ ← Django app
├── init.py
├── admin.py
├── apps.py
├── models.py
├── views.py
├── tests.py
└── migrations/

templates/ ← HTML templates
└── .html files (home, donate, about, etc.)

manage.py ← Django management script
requirements.txt ← Python dependencies
runtime.txt ← Python version for deployment
vercel_wsgi.py ← Vercel deployment entry point

yaml
Copy
Edit

---

##  Getting Started

### Prerequisites

- Python 3.12
- `virtualenv` or `venv`
- Access to a database (SQLite in development, or configure production DB)

### Installation & Setup

```bash
git clone https://github.com/devHashim111/blood-donation-management-system
cd blood-donation-management-system
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Configuration
Set environment variables (e.g., in .env file):

env
Copy
Edit

DATABASE_URL=your_database_connection_url
Apply migrations:

bash
Copy
Edit
python manage.py migrate
Create a superuser (optional but useful):

bash
Copy
Edit
python manage.py createsuperuser
Run the development server:

bash
Copy
Edit
python manage.py runserver
Deployment
This project is configured for deployment on Vercel using vercel_wsgi.py. To deploy:

Push your code to GitHub.

In Vercel dashboard, import the repository.

Set necessary environment variables in Vercel settings.

Deploy — Vercel uses vercel_wsgi.py as the Django entry point.

Templates Overview
home.html — Landing page with overview.

about.html — Information about the platform.

contact.html — Contact form or details.

donate.html — Form or page to submit a donation request.

news.html — Updates or news feed.

required.html — List of requirements (maybe needed blood types or resource lists).

base.html — Base template for consistent layout and navigation.

Contributing
Contributions are welcome! If you’d like to help:

Fork the repository.

Create a feature branch: git checkout -b feature-name.

Commit changes and push.

Open a Pull Request with details of your updates.

License & Notes
Ensure no sensitive data (like secrets or .env) is committed.

Feel free to add documentation for custom business logic or features.

yaml
Copy
Edit




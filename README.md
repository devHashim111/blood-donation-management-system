# Blood Donation Platform

**Live Site:** https://blood-donation-gray.vercel.app/

A Django-based blood donation management system designed to connect blood donors with people in need. The platform provides a simple, user-friendly, template-based web interface for submitting blood requests, registering ready donors, publishing donation-related news, and handling contact enquiries.

## Features

* Responsive pages including **Home**, **About**, **Contact**, **Donate**, **News**, and **Required**.
* Server-rendered UI built with **Django Templates**.
* Blood request management with blood group, hospital, location, disease, contact information, urgency, and resolution status.
* Ready donor registration with personal information, blood group, contact details, and donation preferences.
* Blood-group-based donor and request matching workflow.
* Support for urgent donation requests and blood-bank donation preferences.
* Pick-and-drop service information for blood requests.
* Donation-related news and announcements using **TinyMCE**.
* Contact form for visitor enquiries and messages.
* Django admin support for managing application data.
* Automated model tests using Django's testing framework.
* Deployment configuration for **Vercel**.

## Application Structure

The project is organized into a Django project, a core application, and a template-based frontend.

```text
blood-donation-management-system/
│
├── blood/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
│
├── panel/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   └── migrations/
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── about.html
│   ├── contact.html
│   ├── donate.html
│   ├── news.html
│   └── required.html
│
├── manage.py
├── requirements.txt
├── runtime.txt
└── vercel_wsgi.py
```

### Django Project

The `blood` package contains the main Django configuration, URL routing, WSGI/ASGI configuration, and project-level views.

### Panel Application

The `panel` application contains the primary application logic, database models, administration configuration, migrations, views, and tests.

### Templates

The `templates` directory contains the server-rendered frontend pages and shared layout components.

## Data Models

The system currently includes the following core models.

### BloodRequest

Stores blood requirements submitted for patients or emergencies.

It includes:

* Blood group
* Location
* Disease or medical requirement
* Time limit
* Hospital
* Attendant name
* Contact information
* Pick-and-drop service status
* Request resolution status
* Creation timestamp

### ReadyDonors

Stores information about people willing to donate blood.

It includes:

* Name and address
* Age
* Gender
* Weight
* Disease information
* Blood group
* Phone number
* Email
* Donation preference
* Registration timestamp

Donors can indicate whether they are available for an urgent request or prefer donating through a blood bank.

### News

Provides a content-management layer for publishing blood donation-related news and announcements.

The `detail` field supports rich HTML content through TinyMCE.

### Contact

Stores messages submitted through the website, including the visitor's name, email address, and message.

## Donation Workflow

The core workflow of the system is centered around connecting blood requests with available donors.

```text
                    Visitor
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
   Submit Blood Request       Register as Donor
          │                         │
          ▼                         ▼
    BloodRequest               ReadyDonors
          │                         │
          └────────────┬────────────┘
                       │
                       ▼
              Blood Group Matching
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
        Matching Donor      No Match Found
              │
              ▼
       Donation Coordination
              │
              ▼
        Request Resolved
```

A blood request contains the information required to identify an appropriate donor, while the ready-donor records provide the available donor pool.

Requests can be tracked using their `is_solved` status, while the `time_limit` field allows urgent or time-sensitive requirements to be identified.

## Technology Stack

| Technology            | Purpose                        |
| --------------------- | ------------------------------ |
| Python                | Application language           |
| Django                | Web framework                  |
| Django Templates      | Server-rendered frontend       |
| Django ORM            | Database access and modeling   |
| SQLite                | Local development database     |
| TinyMCE               | Rich-text news/content editing |
| Django Admin          | Data administration            |
| Django Test Framework | Automated testing              |
| Vercel                | Deployment                     |

## Requirements

* Python 3.12
* `pip`
* `venv` or another Python virtual environment
* SQLite for local development
* Git

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/devHashim111/blood-donation-management-system.git
cd blood-donation-management-system
```

### 2. Create a Virtual Environment

Linux/macOS:

```bash
python3.12 -m venv venv
source venv/bin/activate
```

Windows:

```powershell
py -3.12 -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create an Administrator

```bash
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at:

```text
http://127.0.0.1:8000/
```

## Testing

The project includes model and workflow tests covering the core blood donation functionality.

Run the complete test suite with:

```bash
python manage.py test
```

Or test the `panel` application specifically:

```bash
python manage.py test panel
```

The tests cover areas such as:

* Blood request creation and validation
* Blood group choices
* Ready donor creation and validation
* Donor filtering by blood group
* Request resolution
* Time-limit handling
* Optional donor information
* Timestamp behavior
* Donor/request matching workflows
* Model persistence and retrieval

## Django Admin

The Django admin interface can be used to manage application records.

After creating a superuser, start the development server and open:

```text
http://127.0.0.1:8000/admin/
```

From the admin interface, administrators can manage the application's registered models and content.

## Templates

The frontend is built using Django's server-side template system.

Typical pages include:

| Template        | Purpose                                         |
| --------------- | ----------------------------------------------- |
| `base.html`     | Shared layout, navigation, and common structure |
| `home.html`     | Landing page                                    |
| `about.html`    | Information about the platform                  |
| `contact.html`  | Contact form/information                        |
| `donate.html`   | Donor or donation-related form                  |
| `news.html`     | Donation-related news and announcements         |
| `required.html` | Blood requirements and requests                 |

## Deployment

The project includes Vercel deployment configuration through `vercel_wsgi.py`.

A typical deployment workflow is:

```text
GitHub Repository
       │
       ▼
     Vercel
       │
       ▼
 Django Application
       │
       ├── Templates
       ├── Views
       └── Database
```

### Deploying to Vercel

1. Push the project to GitHub.
2. Import the repository into Vercel.
3. Configure the required environment variables.
4. Deploy the project using the repository's Vercel configuration.

For production deployments, database configuration and media/static-file handling should be configured according to the hosting environment.

## Environment Variables

Local development can use a `.env` file for configuration that should not be committed to source control.

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=True
```

Never commit actual secrets, credentials, or private configuration values to GitHub.

## Project Goals

This project demonstrates practical Django development through a real-world use case rather than a simple CRUD example.

Its main goals are to provide:

* A complete server-rendered Django workflow
* Practical relational data modeling
* Form-driven user interaction
* Blood request and donor management
* Blood-group matching logic
* Administrative data management
* Automated testing
* Production-oriented deployment configuration

## Future Improvements

Potential future enhancements include:

* User accounts and donor authentication
* Advanced blood-group compatibility matching
* Automated donor notifications
* SMS and email notifications
* Hospital accounts and dashboards
* Donation history
* Donor eligibility tracking
* Geographic donor matching
* Appointment scheduling
* Blood inventory management
* Improved analytics and reporting
* More advanced search and filtering
* Production database integration

## Contributing

Contributions are welcome.

```bash
git checkout -b feature-name
```

Make your changes, test them, commit them, and push the branch:

```bash
git add .
git commit -m "Add feature"
git push origin feature-name
```

Then open a Pull Request with a clear description of the changes.

## Security

Do not commit:

* `.env` files
* Secret keys
* Database credentials
* Production credentials
* Private deployment configuration

For production use, configure `DEBUG=False`, secure secret management, HTTPS, appropriate host configuration, and a production-ready database and static/media storage solution.

## License

This project is open source. Add the license used by the repository here.

For example:

```text
MIT License
```

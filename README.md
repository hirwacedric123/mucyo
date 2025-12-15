# Student Translator MVP

A Django web application that translates student documents between English, French, Arabic, Swahili, and Kinyarwanda using OpenAI GPT-4.

## Features

* Upload PDF and DOCX files
* Automatic language detection
* Translation between 5 languages
* Download translated documents as PDF
* Modern, responsive UI

## Quick Start

### Prerequisites

1. Python 3.10 or higher
2. OpenAI API key from https://platform.openai.com/api-keys

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/hirwacedric123/mucyo.git
   cd mucyo
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

5. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Collect static files**:
   ```bash
   python manage.py collectstatic --noinput
   ```

7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

8. **Visit** http://127.0.0.1:8000

## Project Structure

```
Mucyo/
├── manage.py              # Django management script
├── mucyo/                 # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── translator/            # Main application
│   ├── views.py          # View logic
│   ├── urls.py           # App URLs
│   ├── templates/        # HTML templates
│   └── static/           # CSS and JavaScript
├── docs/                  # Documentation
│   ├── DEPLOYMENT_PYTHONANYWHERE.md
│   ├── DJANGO_MIGRATION.md
│   ├── FIXES.md
│   └── TROUBLESHOOTING.md
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in git)
└── README.md             # This file
```

## Supported File Types

* PDF (.pdf)
* Microsoft Word (.docx)

## Supported Languages

* English
* French
* Arabic
* Swahili
* Kinyarwanda

## Deployment

### PythonAnywhere

See [docs/DEPLOYMENT_PYTHONANYWHERE.md](docs/DEPLOYMENT_PYTHONANYWHERE.md) for detailed deployment instructions.

### Other Platforms

The application can be deployed to:
* Render
* Heroku
* Railway
* DigitalOcean
* AWS
* Any platform that supports Django

## Environment Variables

Required:
- `OPENAI_API_KEY`: Your OpenAI API key (required)

Optional:
- `SECRET_KEY`: Django secret key (generates default for development)
- `DEBUG`: Set to `False` in production

## Documentation

- [Deployment Guide](docs/DEPLOYMENT_PYTHONANYWHERE.md) - Deploy to PythonAnywhere
- [Migration Guide](docs/DJANGO_MIGRATION.md) - Flask to Django migration details
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and solutions
- [Fixes Applied](docs/FIXES.md) - List of fixes and improvements

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please check the [Troubleshooting Guide](docs/TROUBLESHOOTING.md) or open an issue on GitHub.

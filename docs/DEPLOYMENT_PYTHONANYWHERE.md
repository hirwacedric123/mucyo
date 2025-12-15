# Deploying to PythonAnywhere

This guide will help you deploy your Django Student Translator app to PythonAnywhere.

## Prerequisites

1. A PythonAnywhere account (free tier available at https://www.pythonanywhere.com)
2. Your OpenAI API key
3. Your code pushed to GitHub (already done)

## Step 1: Create a PythonAnywhere Account

1. Go to https://www.pythonanywhere.com
2. Sign up for a free account (or use existing account)
3. Verify your email if required

## Step 2: Clone Your Repository

1. Open a **Bash console** in PythonAnywhere
2. Navigate to your home directory:
   ```bash
   cd ~
   ```
3. Clone your repository:
   ```bash
   git clone https://github.com/hirwacedric123/mucyo.git
   cd mucyo
   ```

## Step 3: Set Up Virtual Environment

**IMPORTANT**: The virtual environment must be created in the **project root** (same directory as `manage.py`), NOT inside the `mucyo/` folder.

### If You Created venv in the Wrong Location

If you accidentally created `venv` inside the `mucyo/` folder (where `settings.py` is), follow these steps:

1. **Navigate to project root**:
   ```bash
   cd ~/mucyo
   # Verify you're in the right place - you should see manage.py here
   ls -la
   ```

2. **Remove the incorrectly placed venv**:
   ```bash
   # Remove venv from mucyo/ folder (wrong location)
   rm -rf mucyo/venv
   
   # Also remove any venv in project root if you want to start fresh
   rm -rf venv
   ```

3. **Create venv in the correct location** (project root):
   ```bash
   python3.10 -m venv venv
   # or python3.11 -m venv venv (depending on available version)
   ```

4. **Verify the location is correct**:
   ```bash
   ls -la
   # You should see: manage.py, mucyo/, translator/, venv/ (at same level)
   # NOT: mucyo/venv/
   ```

### Normal Setup (If Starting Fresh)

1. **Navigate to project root**:
   ```bash
   cd ~/mucyo
   ```

2. **Create virtual environment**:
   ```bash
   python3.10 -m venv venv
   # or python3.11 -m venv venv (depending on available version)
   ```

3. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate
   ```

4. **Upgrade pip**:
   ```bash
   pip install --upgrade pip
   ```

5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Step 4: Set Up Database

1. Run migrations:

   ```bash
   python manage.py migrate
   ```
2. Create a superuser (optional, for admin access):

   ```bash
   python manage.py createsuperuser
   ```

## Step 5: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

## Step 6: Configure Environment Variables

1. Create a `.env` file in your project directory:

   ```bash
   cd ~/mucyo
   nano .env
   ```
2. Add your environment variables:

   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   SECRET_KEY=your-django-secret-key-here
   DEBUG=False
   ```
3. Generate a Django secret key (run in Python console):

   ```python
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```
4. Save the file (Ctrl+X, then Y, then Enter)

## Step 7: Update Settings for Production

Edit `mucyo/settings.py` and ensure:

1. **ALLOWED_HOSTS** includes your PythonAnywhere domain:

   ```python
   ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']
   ```
2. **DEBUG** is set to False (or use environment variable)

## Step 8: Create a Web App

1. Go to the **Web** tab in PythonAnywhere dashboard
2. Click **Add a new web app**
3. Choose **Manual configuration** (not "Django")
4. Select Python version (3.10 or 3.11)
5. Click **Next** and then **Finish**

## Step 9: Configure WSGI File

1. In the **Web** tab, click on the WSGI configuration file link
2. Delete all the default code
3. Replace with:

```python
import os
import sys

# Add your project directory to the Python path
path = '/home/yourusername/mucyo'
if path not in sys.path:
    sys.path.insert(0, path)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'mucyo.settings'

# Activate virtual environment (in project root, NOT in mucyo/venv/)
activate_this = '/home/yourusername/mucyo/venv/bin/activate_this.py'
if os.path.exists(activate_this):
    exec(open(activate_this).read(), {'__file__': activate_this})
else:
    # Alternative method if activate_this.py doesn't exist
    venv_path = '/home/yourusername/mucyo/venv'
    if os.path.exists(venv_path):
        sys.path.insert(0, os.path.join(venv_path, 'lib', 'python3.10', 'site-packages'))
        # or python3.11 depending on your Python version

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Important**: 
- Replace `yourusername` with your actual PythonAnywhere username!
- The venv path should be `/home/yourusername/mucyo/venv` (project root), NOT `/home/yourusername/mucyo/mucyo/venv`

## Step 10: Configure Static Files

1. In the **Web** tab, scroll down to **Static files**
2. Add a new mapping:

   - **URL**: `/static/`
   - **Directory**: `/home/yourusername/mucyo/staticfiles`
3. Add another mapping for media files (if needed):

   - **URL**: `/media/`
   - **Directory**: `/home/yourusername/mucyo/media`

## Step 11: Create Required Directories

In Bash console:

```bash
cd ~/mucyo
mkdir -p uploads translations media staticfiles
```

## Step 12: Reload Web App

1. Go back to the **Web** tab
2. Click the green **Reload** button
3. Your app should now be live at: `https://yourusername.pythonanywhere.com`

## Step 13: Test Your Application

1. Visit your site: `https://yourusername.pythonanywhere.com`
2. Try uploading a document and translating it
3. Check the **Error log** in the Web tab if something doesn't work

## Troubleshooting

### Common Issues:

1. **500 Internal Server Error**:

   - Check the Error log in the Web tab
   - Verify `.env` file exists and has correct API key
   - Check that `ALLOWED_HOSTS` includes your domain
2. **Static files not loading**:

   - Run `python manage.py collectstatic --noinput` again
   - Verify static files mapping in Web tab
   - Check that `STATIC_ROOT` path is correct
3. **Module not found errors**:

   - Ensure virtual environment is activated in WSGI file
   - Verify all dependencies are installed: `pip install -r requirements.txt`
4. **Database errors**:

   - Run migrations: `python manage.py migrate`
   - Check database permissions
5. **API key not working**:

   - Verify `.env` file is in the project root
   - Check that `python-dotenv` is installed
   - Restart web app after adding/changing `.env`

### Viewing Logs:

- **Error log**: Web tab → Error log
- **Server log**: Web tab → Server log
- **Console output**: Use Bash console

## Updating Your App

When you push changes to GitHub:

1. In Bash console:

   ```bash
   cd ~/mucyo
   git pull origin main
   ```
2. If requirements changed:

   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. If database changes:

   ```bash
   python manage.py migrate
   ```
4. If static files changed:

   ```bash
   python manage.py collectstatic --noinput
   ```
5. Reload web app in the Web tab

## Security Notes

- Never commit `.env` file to git (already in `.gitignore`)
- Use `DEBUG=False` in production
- Set a strong `SECRET_KEY`
- Keep your OpenAI API key secure
- Regularly update dependencies

## Free Tier Limitations

- Limited CPU time per day
- Limited outbound internet access
- App sleeps after inactivity (wakes on first request)
- Limited storage space

For production use, consider upgrading to a paid plan.

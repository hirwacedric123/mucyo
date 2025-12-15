# Troubleshooting 500 Server Error

## Quick Fixes

### 1. Enable DEBUG Mode
Make sure DEBUG is set to True in your environment or settings:
```bash
export DEBUG=True
# or in settings.py, it should default to True now
```

### 2. Check the Actual Error
With DEBUG=True, Django will show you the actual error. Look at the terminal output or browser for the full traceback.

### 3. Common Issues and Solutions

#### Issue: Template Not Found
**Solution**: Verify template directory structure:
```
translator/
  templates/
    translator/
      index.html
      success.html
```

#### Issue: Static Files Not Found
**Solution**: In development, Django serves static files automatically if DEBUG=True.
If you see 404s for static files, run:
```bash
python manage.py collectstatic --noinput
```

#### Issue: Import Errors
**Solution**: Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

#### Issue: Database Not Migrated
**Solution**: Run migrations:
```bash
python manage.py migrate
```

### 4. Check Server Logs
Look at your terminal where `python manage.py runserver` is running. The actual error will be printed there.

### 5. Test Individual Components

Test if Django is working:
```bash
python manage.py shell
>>> from django.conf import settings
>>> settings.DEBUG
>>> from translator import views
```

Test template rendering:
```bash
python manage.py shell
>>> from django.template.loader import get_template
>>> template = get_template('translator/index.html')
>>> template.render({'languages': {'english': 'English'}})
```

## Most Likely Causes

1. **Missing dependencies** - Run `pip install -r requirements.txt`
2. **Template path issue** - Check that templates are in `translator/templates/translator/`
3. **Static files issue** - Make sure DEBUG=True for development
4. **Import error** - Check that all packages in views.py are installed
5. **Database issue** - Run `python manage.py migrate`

## Get Detailed Error

To see the full error, make sure:
1. DEBUG=True in settings
2. Check terminal output when you visit the page
3. The browser will show a detailed error page with DEBUG=True


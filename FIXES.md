# Fixes Applied

## Issues Fixed

### 1. Staticfiles Directory Warning
- **Problem**: Django was warning about missing `/staticfiles/` directory
- **Fix**: 
  - Updated `settings.py` to create the directory automatically
  - Changed WhiteNoise storage to only be used in production (not in DEBUG mode)
  - Updated `urls.py` to conditionally serve static files

### 2. Development vs Production Settings
- **Problem**: WhiteNoise's `CompressedManifestStaticFilesStorage` requires running `collectstatic` first
- **Fix**: Use default Django static file storage in development mode

## How to Run

1. **Activate virtual environment**:
   ```bash
   source venv/bin/activate
   ```

2. **Install dependencies** (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Collect static files** (optional for development, required for production):
   ```bash
   python manage.py collectstatic --noinput
   ```

5. **Run development server**:
   ```bash
   python manage.py runserver
   ```

## Troubleshooting 500 Errors

If you're still getting 500 errors:

1. **Check Django logs**: Look at the terminal output for the actual error message
2. **Enable DEBUG mode**: Make sure `DEBUG=True` in your environment or settings
3. **Check template paths**: Ensure templates are in `translator/templates/translator/`
4. **Check static files**: Run `python manage.py collectstatic` if needed
5. **Check database**: Run `python manage.py migrate` to ensure database is set up

## Environment Variables

Make sure to set these environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key (required for translation)
- `SECRET_KEY`: Django secret key (for production)
- `DEBUG`: Set to `True` for development, `False` for production


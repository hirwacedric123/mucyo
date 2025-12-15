# Fix Virtual Environment Location on PythonAnywhere

## Quick Fix Commands

Run these commands in your PythonAnywhere Bash console:

### Step 1: Navigate to Project Root
```bash
cd ~/mucyo
# Verify you're in the right place
ls -la
# You should see: manage.py, mucyo/, translator/, etc.
```

### Step 2: Remove Incorrectly Placed venv

**If venv is inside mucyo/ folder (WRONG location):**
```bash
# Check if it exists
ls -la mucyo/venv 2>/dev/null && echo "Found venv in wrong location"

# Remove it
rm -rf mucyo/venv
```

**Also remove any existing venv in project root (if you want fresh start):**
```bash
rm -rf venv
```

### Step 3: Create venv in Correct Location

```bash
# Create venv in project root (same level as manage.py)
python3.10 -m venv venv
# OR if Python 3.11 is available:
# python3.11 -m venv venv
```

### Step 4: Verify Correct Location

```bash
# Check the structure
ls -la
# Should show: manage.py, mucyo/, translator/, venv/ (all at same level)

# Verify venv is NOT inside mucyo/
ls mucyo/venv 2>/dev/null && echo "ERROR: venv still in wrong place!" || echo "✓ venv is in correct location"
```

### Step 5: Activate and Install

```bash
# Activate venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Step 6: Update WSGI File

Make sure your WSGI file points to the correct venv path:
- **Correct**: `/home/edutranslate/mucyo/venv/bin/activate_this.py`
- **Wrong**: `/home/edutranslate/mucyo/mucyo/venv/bin/activate_this.py`

## Correct Project Structure

```
~/mucyo/                    ← Project root (where manage.py is)
├── manage.py
├── venv/                   ← Virtual environment (CORRECT location)
│   ├── bin/
│   ├── lib/
│   └── ...
├── mucyo/                  ← Django project folder
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── translator/             ← Django app
│   ├── views.py
│   └── ...
├── requirements.txt
└── .env
```

## Common Mistakes

❌ **Wrong**: `~/mucyo/mucyo/venv/` (inside Django project folder)  
✅ **Correct**: `~/mucyo/venv/` (in project root)

## After Fixing

1. Reload your web app in PythonAnywhere dashboard
2. Check error logs if issues persist
3. Verify all paths in WSGI file are correct


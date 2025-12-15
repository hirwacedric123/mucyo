#!/usr/bin/env python
"""
Quick test script to check Django setup
"""
import os
import sys
import django

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mucyo.settings')

try:
    django.setup()
    print("✓ Django setup successful")
    
    from django.conf import settings
    print(f"✓ DEBUG mode: {settings.DEBUG}")
    print(f"✓ Installed apps: {len(settings.INSTALLED_APPS)} apps")
    
    from django.template.loader import get_template
    try:
        template = get_template('translator/index.html')
        print("✓ Template 'translator/index.html' found")
    except Exception as e:
        print(f"✗ Template error: {e}")
    
    from translator import views
    print("✓ Translator views imported successfully")
    
    print("\n✓ All checks passed!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


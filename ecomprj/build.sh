#!/usr/bin/env bash
# exit on error
set -o errexit

echo "====== Starting build process ======"

echo "====== Installing dependencies ======"
pip install --upgrade pip
pip install -r requirements.txt

echo "====== Compiling translation files ======"
python -c "
from babel.messages.mofile import write_mo
from babel.messages.pofile import read_po
import os

langs = ['en', 'kk', 'ru']
for lang in langs:
    po_path = f'locale/{lang}/LC_MESSAGES/django.po'
    mo_path = f'locale/{lang}/LC_MESSAGES/django.mo'
    if os.path.exists(po_path):
        with open(po_path, 'r', encoding='utf-8') as po_file:
            catalog = read_po(po_file)
        with open(mo_path, 'wb') as mo_file:
            write_mo(mo_file, catalog)
        print(f'Compiled {po_path} -> {mo_path}')
print('Translation files compiled successfully!')
"

echo "====== Collecting static files ======"
python manage.py collectstatic --no-input

echo "====== Running migrations ======"
python manage.py migrate --no-input

echo "====== Build completed successfully ======"

# E-commerce Store

A full-stack e-commerce web application built with Django, developed as part of the CodeAlpha Full Stack Development Internship.

## Features
- Product catalog organized by categories (Groceries, Clothing, Home Decor, Electronics, Footwear, Personal Care)
- Product listing and detail pages with images
- Shopping cart (add, remove, view items and totals)
- User registration, login, and logout
- Checkout and order processing
- Order history for logged-in users
- Admin panel for managing products, categories, and orders

## Tech Stack
- **Backend:** Django (Python)
- **Frontend:** HTML, CSS
- **Database:** SQLite

## How to Run Locally
1. Clone the repository
2. Create and activate a virtual environment
3. Install Django: `pip install django`
4. Run migrations: `python manage.py migrate`
5. Create a superuser: `python manage.py createsuperuser`
6. Start the server: `python manage.py runserver`
7. Visit `http://127.0.0.1:8000/`
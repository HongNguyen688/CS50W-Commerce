# CS50W Commerce – Django Auction Site

A full-stack e-commerce auction web application built as part of Harvard CS50’s Web Programming with Python and JavaScript.

This project allows users to create auction listings, place bids, comment, manage watchlists, and close auctions with authenticated user accounts.

## Live Demo
[My website] (https://hongnguyen688.pythonanywhere.com/)

## Features

- User authentication (register, login, logout)

- Create and manage auction listings

- Category-based browsing

- Bidding system

- Close auctions and declare winners

- Comment system

- Watchlist functionality

- Responsive UI with Bootstrap

- Deployed on PythonAnywhere

## Tech Stack

1. Frontend: HTML, CSS, Bootstrap
   
2. Backend: Django 4.2

3. Database: SQLite

4. Deployment: PythonAnywhere

## Project Structure

1. **auctions**: Main application.        
2. **commerce**: Project settings        
3. **staticfiles**       
4. **manage.py**
5. **requirements.txt**
6. **db.sqlite3**

## Local Development Setup
1. Clone the repository
git clone https://github.com/HongNguyen688/CS50W-Commerce.git
cd CS50W-Commerce

2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate

3. Install dependencies
pip3 install --upgrade pip
pip3 install -r requirements.txt

4. Apply migrations
python3 manage.py makemigrations
python3 manage.py migrate

5. Run the development server
python3 manage.py runserver


### Open your browser at:
👉 http://127.0.0.1:8000/


👤 Author

**Hong Nguyen**
GitHub: https://github.com/HongNguyen688

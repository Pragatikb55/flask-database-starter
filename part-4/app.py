"""
Part 4: REST API with Flask
===========================
Build a JSON API for database operations (used by frontend apps, mobile apps, etc.)

What You'll Learn:
- REST API concepts (GET, POST, PUT, DELETE)
- JSON responses with jsonify
- API error handling
- Status codes
- Testing APIs with curl or Postman

Prerequisites: Complete part-3 (SQLAlchemy)
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Author, Book

app = Flask(__name__)
app.secret_key = "secret-key"

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ======================= HTML UI =======================

@app.route('/')
def index():
    authors = Author.query.all()
    books = Book.query.all()

    edit_author_id = request.args.get('edit_author')
    edit_book_id = request.args.get('edit_book')

    edit_author = Author.query.get(edit_author_id) if edit_author_id else None
    edit_book = Book.query.get(edit_book_id) if edit_book_id else None

    return render_template(
        'index.html',
        authors=authors,
        books=books,
        edit_author=edit_author,
        edit_book=edit_book
    )

# ================= AUTHOR CRUD =================

@app.route('/add-author', methods=['POST'])
def add_author():
    name = request.form['name']
    bio = request.form.get('bio')
    city = request.form.get('city')

    new_author = Author(name=name, bio=bio, city=city)
    db.session.add(new_author)
    db.session.commit()
    flash("Author added successfully!")
    return redirect(url_for('index'))

@app.route('/update-author/<int:id>', methods=['POST'])
def update_author(id):
    author = Author.query.get_or_404(id)
    author.name = request.form['name']
    author.bio = request.form.get('bio')
    author.city = request.form.get('city')
    db.session.commit()
    flash("Author updated successfully!")
    return redirect(url_for('index'))

@app.route('/delete-author/<int:id>')
def delete_author(id):
    author = Author.query.get_or_404(id)
    db.session.delete(author)
    db.session.commit()
    flash("Author deleted successfully!")
    return redirect(url_for('index'))

# ================= BOOK CRUD =================

@app.route('/add-book', methods=['POST'])
def add_book():
    title = request.form['title']
    isbn = request.form['isbn']
    author_id = int(request.form['author_id'])

    new_book = Book(title=title, isbn=isbn, author_id=author_id)
    db.session.add(new_book)
    db.session.commit()
    flash("Book added successfully!")
    return redirect(url_for('index'))

@app.route('/update-book/<int:id>', methods=['POST'])
def update_book(id):
    book = Book.query.get_or_404(id)
    book.title = request.form['title']
    book.isbn = request.form['isbn']
    book.author_id = int(request.form['author_id'])
    db.session.commit()
    flash("Book updated successfully!")
    return redirect(url_for('index'))

@app.route('/delete-book/<int:id>')
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash("Book deleted successfully!")
    return redirect(url_for('index'))

# ================= REST APIs =================

@app.route('/api/books')
def api_books():
    books = Book.query.all()
    return jsonify([
        {
            "id": b.id,
            "title": b.title,
            "isbn": b.isbn,
            "author": b.author.name
        } for b in books
    ])

@app.route('/api/add-book', methods=['POST'])
def api_add_book():
    data = request.get_json()
    new_book = Book(title=data['title'], isbn=data['isbn'], author_id=data['author_id'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"success": True})

# ================= PAGINATION =================

@app.route('/api/books-with-pagination')
def api_books_paginated():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    pagination = Book.query.paginate(page=page, per_page=per_page)
    return jsonify({
        "total": pagination.total,
        "pages": pagination.pages,
        "books": [
            {"id": b.id, "title": b.title, "isbn": b.isbn, "author": b.author.name}
            for b in pagination.items
        ]
    })

# ================= SORTING =================

@app.route('/api/books-with-sorting')
def api_books_sorting():
    sort = request.args.get('sort', 'title')
    order = request.args.get('order', 'asc')

    column = getattr(Book, sort, Book.title)
    books = Book.query.order_by(column.desc() if order == 'desc' else column.asc()).all()

    return jsonify([
        {"id": b.id, "title": b.title, "isbn": b.isbn, "author": b.author.name}
        for b in books
    ])

# ================= RUN =================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)



# =============================================================================
# REST API CONCEPTS:
# =============================================================================
#
# HTTP Method | CRUD      | Typical Use
# ------------|-----------|---------------------------
# GET         | Read      | Retrieve data
# POST        | Create    | Create new resource
# PUT         | Update    | Update entire resource
# PATCH       | Update    | Update partial resource
# DELETE      | Delete    | Remove resource
#
# =============================================================================
# HTTP STATUS CODES:
# =============================================================================
#
# Code | Meaning
# -----|------------------
# 200  | OK (Success)
# 201  | Created
# 400  | Bad Request (client error)
# 404  | Not Found
# 500  | Internal Server Error
#
# =============================================================================
# KEY FUNCTIONS:
# =============================================================================
#
# jsonify()           - Convert Python dict to JSON response
# request.get_json()  - Get JSON data from request body
# request.args.get()  - Get query parameters (?key=value)
#
# =============================================================================


# =============================================================================
# EXERCISE:
# =============================================================================
#
# 1. Create new class say "Author" with fields id, name, bio, city with its table. 
# Write all CRUD api routes for it similar to Book class.
# Additionally try to link Book and Author class such that each book has one author and one author can have multiple books.

# 1. Create 2 simple frontend using JavaScript fetch()
# This is a bigger exercise. Create a frontend in HTML and JS that uses all api routes and displays data dynamically, along with create/edit/delete functionality.
# Since the API is through n through accessible on the computer/server, you don't need to use render_template from flask, instead, 
# you can directly use ipaddress:portnumber/apiroute from any where. So your HTML JS code can be anywhere on computer (not necessarily in flask)  

# 3. Add pagination: `/api/books?page=1&per_page=10` 
# Hint - the sqlalchemy provides paginate method. 
# OPTIONAL - For ease of understanding, create a new api say /api/books-with-pagination which takes page number and number of books per page

# 4. Add sorting: `/api/books?sort=title&order=desc`
# OPTIONAL - For ease of understanding, create a new api say /api/books-with-sorting
#
# =============================================================================
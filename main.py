from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///book-collections.db"
app.config['SQLALCHEMY-TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


    def __repr__(self):
        return f'<Book {self.title}>'

db.create_all()



@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template("index.html", add_book=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_books = Book(title=request.form["title"], author=request.form["author"], rating=request.form["rating"])
        db.session.add(new_books)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")

@app.route("/edit", methods=["GET","POST"])
def edit():
    if request.method == "POST":
        book_id = request.form["id"]
        book_to_update = Book.query.get(book_id)
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_select = Book.query.get(book_id)
    return render_template("edit.html", book=book_select)

@app.route("/delete")
def delete():
    book_id = request.args.get('id')
    book_select = Book.query.get(book_id)
    db.session.delete(book_select)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    print("Git Testing")
    app.run(debug=True)


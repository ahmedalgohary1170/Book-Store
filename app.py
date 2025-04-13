from flask import Flask , render_template , request,redirect , url_for
import os
from models import db , Book, Author, Review

app = Flask(__name__)

BASE_DIR =os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR,'book.db')}"


db.init_app(app)


with app.app_context():
    db.create_all()



@app.route('/')
def index():
    books= Book.query.all()
    return render_template('index.html',books=books)




@app.route('/add-book',methods=['GET','POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author_name = request.form['author_name']
        author = Author.query.filter_by(name=author_name).first()
        if not author:
            author = Author(name=author_name)
            db.session.add(author)
            db.session.commit()
        book = Book(title=title, author_id=author.id)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_book.html')


@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit_book(id):
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        title = request.form['title']
        author_name = request.form['author_name']
        author = Author.query.filter_by(name=author_name).first()
        if not author:
            author = Author(name=author_name)
            db.session.add(author)
            db.session.commit()
        book.author_id = author.id
        book.title = title
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_book.html',book=book)



@app.route('/delete/<int:id>')
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/books/<int:id>')

def book_detail(id):
    book = Book.query.get_or_404(id)
    return render_template('book_detail.html', book=book)


if __name__ =='__main__':
    app.run(debug=True)
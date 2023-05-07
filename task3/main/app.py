from flask import Flask,render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import MySQLdb

app = Flask(__name__)

# MySQL Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456789'
app.config['MYSQL_DB'] = 'library_users'
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'

#-------------------------------------------Indexes----------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE name = %s', (name,))
        user = cur.fetchone()
        if name and check_password_hash(user[2], password):
            session.clear()
            session['user_id'] = user[0]
            session['user_role'] = user[3]
            flash('Logged in successfully!', 'success')
            if user[3] == 'librarian':
                return redirect('/library')
            elif user[3] == 'User':
                return redirect('/user')
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

# Users Index

@app.route('/new_user')
def User():
    cur = mysql.connection.cursor()
    cur.execute('Select * from users')
    data = cur.fetchall()

    return render_template('user.html', users = data)

# Books Index

@app.route('/book')
def Book():
    cur = mysql.connection.cursor()
    cur.execute('Select * from books')
    data = cur.fetchall()

    return render_template('new_books.html', books = data)

#------------------------------------------Roles---------------------------------------------------------------
@app.route("/default")
def defautl():
    cur = mysql.connection.cursor()
    cur.execute("SELECT books.id, books.title, books.author, loans.state FROM books LEFT JOIN loans ON books.id = loans.id_books")
    data = cur.fetchall()
    return render_template("loans_default.html", books = data)

@app.route('/library')
def library():
    cur = mysql.connection.cursor()
    cur.execute("SELECT books.id, books.title, books.author, loans.state, loans.due_date, loans.borrower FROM books LEFT JOIN loans ON books.id = loans.id_books")
    data = cur.fetchall()
    return render_template('loans_library.html', books=data)

@app.route('/user')
def user():
    cur = mysql.connection.cursor()
    cur.execute("SELECT books.id, books.title, books.author, loans.state, loans.due_date FROM books LEFT JOIN loans ON books.id = loans.id_books")
    data = cur.fetchall()
    id_users = session['user_id']
    return render_template('loans_user.html', books=data, id_users=id_users)

#--------------------------------------------Reserver books---------------------------------------------------------------

@app.route("/reserve_book/<int:id_books>/<int:id_users>", methods=['POST'])
def reserve_book(id_books, id_users):
    print(id_users)
    print(id_books)
    
    due_date = datetime.date.today() + datetime.timedelta(days=14)
    cur = mysql.connection.cursor()
    borrower= None
    cur.execute('SELECT name FROM users WHERE id= %s',(id_users, ))
    borrower = cur.fetchone()[0]

    cur.execute("INSERT INTO loans (id_users, id_books, state, borrower, due_date) VALUES (%s, %s, %s, %s, %s)",
                (id_users, id_books, 'reserved', borrower, due_date.strftime('%Y-%m-%d')))
    mysql.connection.commit()
    
    flash('Book reserved successfully', 'success')
    return redirect(url_for('user'))

#---------------------------------------------overdue reserve--------------------------------------------------------------

def check_overdue_loans():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id_books, id_users, due_date FROM loans WHERE state='reserved' AND due_date <= NOW()")
    overdue_loans = cur.fetchall()
    for loan in overdue_loans:
        id_book = loan[0]
        id_user = loan[1]
        cur.execute("UPDATE loans SET state='available', date=NULL WHERE id_books=%s AND id_users=%s", (id_book, id_user))
        mysql.connection.commit()

#--------------------------------------------Delete Loans------------------------------------------------------------------

@app.route("/del_loans/<int:id_books>", methods =["POST"])
def del_loans(id_books):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM loans WHERE id_books = %s', (id_books, ))
    mysql.connection.commit()
    flash('Book Unreserved successfully')
    return redirect(url_for('library'))

#----------------------------------------------------------------------Users-----------------------------------------------

@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        password =request.form['password']
        hashed_password = generate_password_hash(password)
        role = request.form['role']
        cur = mysql.connection.cursor()
        try:
            cur.execute('INSERT INTO users (name,password,role) VALUES (%s, %s, %s)',
                        (name, hashed_password, role))
            mysql.connection.commit()
            flash('User Added successfully')
            return redirect(url_for('User'))
        except MySQLdb.IntegrityError as e:
            error_msg = str(e)
            if "Duplicate entry" in error_msg:
                flash("Error: User with that name already exists! ")
            else:
                flash("Error adding user")
            return redirect(url_for('User'))
    return redirect(url_for('User'))

@app.route('/edit_user/<string:id>')
def get_user(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE id = %s', (id,))
    data = cur.fetchall()
    return render_template('edit_user.html', user = data[0]) 

@app.route('/update_user/<string:id>', methods = ['POST'])
def update_user(id):
    if request.method == 'POST':
        name = request.form['name']
        password =request.form['password']
        role = request.form['role']
        cur = mysql.connection.cursor()

        # Obtain the encrypted password for the user selected
        cur.execute('SELECT password FROM users WHERE id = %s', (id,))
        result = cur.fetchone()
        hashed_password = result[0]

        # Desencrypt the password and verify if the new password matches the previous password
        if check_password_hash(hashed_password, password):
            flash('The new password should be different from the current one')
            return redirect(url_for('get_user', id=id))
        
        hashed_password = generate_password_hash(password)

        
        cur.execute('''
        UPDATE users
        SET name = %s,
            password = %s,
            role = %s
        WHERE id = %s
        ''', (name,hashed_password,role,id,))
        flash ('User Updated Successfully.')
        mysql.connection.commit()
        return redirect(url_for('User'))

@app.route('/del_user/<string:id>')
def del_user(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM users WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('User Deleted successfully')
    return redirect(url_for('User'))

#---------------------------------------Books---------------------------------------

@app.route('/add_book', methods=['POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author =request.form['author']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO books (title,author) VALUES (%s, %s)',
                    (title, author))
        mysql.connection.commit()
        flash('Book Added successfully')

    return redirect(url_for('Book'))

@app.route('/edit_book/<string:id>')
def get_book(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM books WHERE id = %s', (id,))
    data = cur.fetchall()
    return render_template('edit_book.html', book = data[0]) 

@app.route('/update_book/<string:id>', methods = ['POST'])
def update_book(id):
    if request.method == 'POST':
        title = request.form['title']
        author =request.form['author']
        cur = mysql.connection.cursor()
        cur.execute('''
        UPDATE books
        SET title = %s,
            author = %s
        WHERE id = %s
        ''', (title, author, id,))
        flash ('Book Updated Successfully.')
        mysql.connection.commit()
        return redirect(url_for('Book'))

@app.route('/del_book/<string:id>')
def del_book(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM books WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Book Deleted successfully')
    return redirect(url_for('Book'))


if __name__ =='__main__':
    app.run(port=3000, debug=True)

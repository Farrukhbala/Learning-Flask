from flask import Flask , render_template ,request , flash , redirect , url_for , session 
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from wtforms import Form , StringField , TextAreaField, PasswordField , validators
from functools import wraps
# from data import Articles

app = Flask(__name__)

# articles = Articles()

# Config MySQL
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "dm_master"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

# Init database
mysql = MySQL(app)

@app.route('/')
def home():
  return render_template('home.html')


class RegisterForm(Form):
    first_name = StringField('First Name' , [validators.Length(min=1 , max=50)])
    last_name = StringField('Last Name' , [validators.Length(min=1 , max=50)])
    username = StringField('Username' , [validators.Length(min=4 , max=25)])
    email = StringField('Email' , [validators.Length(min=6 , max=50)])
    password = PasswordField('Password' , [
        validators.DataRequired(),
        validators.EqualTo('confirm' , message = 'Password do not match')
        ])
    confirm = PasswordField('Confirm Password')


def is_logged_in(f):
  @wraps(f)
  def wrap(*args , **kwargs):
    if 'logged_in' in session:
      return f(*args , **kwargs)
    else:
      flash("Unauthorized Access! Please Login!" , 'danger')
      return redirect(url_for('login'))
  return wrap

@app.route('/articles')
def article():
  
  cur = mysql.connection.cursor()
  result = cur.execute('SELECT * FROM add_article')
  
  _articles = cur.fetchall()

  if result > 0:
    return render_template('articles.html' , _articles = _articles)
  else:
    msg = 'No Article Found!'
    return render_template('articles.html' , msg = msg)

@app.route('/article/<id>')
def articless(id):
  #creating cursor
  cur = mysql.connection.cursor()
  result = cur.execute('SELECT * FROM add_article WHERE id = %s' , [id])
  data_article = cur.fetchone()
  

  return render_template('blog_articles.html' , data_article = data_article)

@app.route('/register' , methods = ['GET' , 'POST'])
def register():

  form = RegisterForm(request.form)

  if request.method == 'POST' and form.validate():
    first_name = form.first_name.data
    last_name = form.last_name.data
    username = form.username.data
    eamil = form.email.data
    password = sha256_crypt.encrypt(str(form.password.data))


    cur = mysql.connection.cursor()

    cur.execute("INSERT into register(first_name , last_name , email , username , password) VALUES  (%s , %s , %s , %s , %s)" ,
    (first_name , last_name , eamil , username , password))

    mysql.connection.commit()

    cur.close()
    flash("You are now register , You can now login" , 'success')
    return redirect(url_for('login'))
  
  return render_template('register.html' , form = form)



@app.route('/login' , methods = ['GET' , 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password_candid = request.form['password']
  
    cur = mysql.connection.cursor()

    result = cur.execute('SELECT * FROM register WHERE username = %s' , [username])

    if result > 0:
      #GET PASSOWORD HASH
      data = cur.fetchone()
      password = data['password']

      if sha256_crypt.verify(password_candid , password):
        session['logged_in'] = True
        session['username'] = username

        flash("You are now logged in!" , 'success')
        return redirect(url_for('dashboard'))

      else:
        error = 'Invalid Password'
        return render_template('login.html' , error = error)
      cur.close()
    else:
      error = "Username not found Please Register Yourself"
      return render_template('login.html' , error = error)

  return render_template('login.html')


@app.route('/logout')
@is_logged_in
def logout():

  session.clear()
  flash("Thank You for USing Our Service! You Are Logged Out" , 'success')
  return render_template('logout.html')


@app.route('/dashboard')
@is_logged_in
def dashboard():
  
  cur = mysql.connection.cursor()
  result = cur.execute('SELECT * FROM add_article')
  
  _articles = cur.fetchall()

  if result > 0:


    return render_template('dashboard.html' , _articles = _articles)

  else:
    msg = 'No Article Found!'
    return render_template('dashboard.html' , msg = msg)




  return render_template('dashboard.html')


class add_article_form(Form):
    title = StringField('Title' , [validators.Length(min=4)])
    body = TextAreaField('Article Body' , [validators.Length(min = 30)])

@app.route('/add_article' , methods = ['GET' , 'POST'])
@is_logged_in
def add_article():
  form = add_article_form(request.form)

  if request.method == 'POST' and form.validate():
    title = form.title.data
    body = form.body.data


    
    cur = mysql.connection.cursor()

    

    cur.execute("INSERT into add_article( title , body , author) VALUES  (%s , %s , %s)" ,
    ( title , body , session['username']))
    mysql.connection.commit()

    cur.close()
    flash("Your Article has been Published Cograts!" , 'success')
    return redirect(url_for('article'))

  return render_template('add_articles.html' , form = form)


@app.route('/about')
def about():
  return render_template('aboutus.html')

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404




if __name__ == "__main__":
    app.secret_key = 'secret123'
    app.run(debug= True , port = 3000)
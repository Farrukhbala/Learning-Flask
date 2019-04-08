from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():

    return render_template('home.html')

@app.route('/puppy')
def puppy():

    return render_template('puppy.html')


@app.route('/services')
def service():

    return render_template('service.html')

@app.route('/login')
def login():

    email = request.args.get('email')
    password = request.args.get('password')
    return render_template('login.html', email = email , password = password)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/thank_you')
def thank_you():

    first = request.args.get('first')
    last = request.args.get('last')
    return render_template('thank_you.html', first = first , last = last)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html') , 404

if __name__ == "__main__":
    app.run(debug=True)





































# @app.route('/')
# def index():
#     some_variable = "Farrukh"
#     names = ['farrukh', 'usama', 'khan','jibran']

#     dictionary = {'name': 'farrukh' , 'father Name' : 'Munir Ahmed'} 
    
#     user = True

#     return render_template('index.html', some_variable = some_variable, names = names , dictionary = dictionary, user = user)

# @app.route('/information')
# def info():
#     return "<h1>Here is the Information Page</h1>"

# # dynamic routing


# @app.route('/dynamic/<name>')
# def dynamic(name):
#     return "<h1>Welcome to dynamic routing {}</h1>".format(name)


# @app.route('/puppy-latin/<name>')
# def puppy_latin(name):
#     if name[-1].lower() == 'y':
#         return "<h1>Welcome to dynamic routing {} </h1>".format(name[:-1] + 'iful')
#     else:
#         return "<h1>Welcome {}</h1>".format(name + 'y')


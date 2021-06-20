from flask import Flask, render_template, url_for
app = Flask(__name__)

bollards = [
    {
        "number": "1",
        "name": "Vitiau",
        "comment": "This is the first comment of the bollard. Please like, subscribe and share",
        "dateAdded": "date",
        "dateUpdated": "date"
    },
    {
        "number": "2",
        "name": "lol",
        "comment": "This is the second comment of the bollard. Please like, subscribe and share",
        "dateAdded": "date",
        "dateUpdated": "date"
    },
    {
        "number": "3",
        "name": "betty",
        "comment": "This is the third comment of the bollard. Please like, subscribe and share OMG",
        "dateAdded": "date",
        "dateUpdated": "date"
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html', title='Login')

@app.route('/list')
def list_bollards():
    return render_template('list.html', title='List', bollards=bollards)

@app.route('/manage')
def manage():
    return render_template('manage.html', title='Manage')

@app.route('/add')
def add():
    return render_template('manage.html', title='Add')

if __name__ == "__main__":
    app.run(debug=True)
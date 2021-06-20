from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/list')
def bollards():
    return render_template('bollards.html')

@app.route('/manage')
def manage():
    return render_template('manage.html')


if __name__ == "__main__":
    app.run(debug=True)
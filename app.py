from flask import Flask, render_template

app = Flask(__name__)


@app.route('/admin')
def dashboardpyth():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/profile')
def profile():
    return render_template('profile_admin.html')

@app.route('/welcomepage')
def welocome():
    return render_template('welcome_page.html')

@app.route('/rekomendasi')
def rekomendasi():
    return render_template('rekomendasi.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)

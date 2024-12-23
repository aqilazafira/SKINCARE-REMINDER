from flask import Flask, render_template

app = Flask(__name__)

# Data dummy untuk kategori skincare
skincare_data = {
    "kulit_kering": [
        {"gambar": "kering1.jpg", "merk": "Brand A", "jenis": "Cleanser"},
        {"gambar": "kering2.jpg", "merk": "Brand B", "jenis": "Toner"}
    ],
    "kulit_normal": [
        {"gambar": "normal1.jpg", "merk": "Brand C", "jenis": "Moisturizer"},
        {"gambar": "normal2.jpg", "merk": "Brand D", "jenis": "Serum"}
    ],
    "kulit_kombinasi": [
        {"gambar": "kombinasi1.jpg", "merk": "Brand E", "jenis": "Essence"},
        {"gambar": "kombinasi2.jpg", "merk": "Brand F", "jenis": "Sunscreen"}
    ],
    "kulit_berjerawat": [
        {"gambar": "berjerawat1.jpg", "merk": "Brand G", "jenis": "Acne Cleanser"},
        {"gambar": "berjerawat2.jpg", "merk": "Brand H", "jenis": "Spot Treatment"}
    ],
    "kulit_berminyak": [
        {"gambar": "berminyak1.jpg", "merk": "Brand I", "jenis": "Oil Cleanser"},
        {"gambar": "berminyak2.jpg", "merk": "Brand J", "jenis": "Mattifying Moisturizer"}
    ]
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/rekomendasi')
def rekomendasi():
    return render_template('rekomendasi.html')

@app.route('/kulit_kering')
def kulit_kering():
    data = skincare_data.get("kulit_kering", [])
    return render_template('kulit_kering.html', data=data)

@app.route('/kulit_normal')
def kulit_normal():
    data = skincare_data.get("kulit_normal", [])
    return render_template('kulit_normal.html', data=data)

@app.route('/kulit_kombinasi')
def kulit_kombinasi():
    data = skincare_data.get("kulit_kombinasi", [])
    return render_template('kulit_kombinasi.html', data=data)

@app.route('/kulit_berjerawat')
def kulit_berjerawat():
    data = skincare_data.get("kulit_berjerawat", [])
    return render_template('kulit_berjerawat.html', data=data)

@app.route('/kulit_berminyak')
def kulit_berminyak():
    return render_template('kulit_berminyak.html')

@app.route('/pengingat')
def pengingat():
    return render_template('pengingat.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/logout')
def logout():
    return 'TODO'

if __name__ == '__main__':
    app.run(debug=True)

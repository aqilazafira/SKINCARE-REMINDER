from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Route untuk halaman home
@app.route('/')
def home():
    return render_template('home.html')

# Route untuk halaman rekomendasi
@app.route('/rekomendasi', methods=['GET', 'POST'])
def rekomendasi():
    jenis_kulit = None
    if request.method == 'POST':
        jenis_kulit = request.form.get('jenis_kulit')
        # Tambahkan logika jika ingin menggunakan data jenis_kulit lebih lanjut
        return redirect(url_for('hasil_rekomendasi', jenis_kulit=jenis_kulit))
    return render_template('rekomendasi.html')

# Route untuk hasil rekomendasi
@app.route('/hasil_rekomendasi/<jenis_kulit>')
def hasil_rekomendasi(jenis_kulit):
    rekomendasi_produk = {
        'kering': 'Gunakan pelembap intensif dan serum hydrating.',
        'normal': 'Gunakan produk ringan seperti gel moisturizer.',
        'kombinasi': 'Gunakan pelembap ringan di zona T dan hydrating di area kering.',
        'berjerawat': 'Gunakan produk dengan kandungan salicylic acid dan non-komedogenik.',
        'berminyak': 'Gunakan produk berbasis gel dan bebas minyak.'
    }
    rekomendasi = rekomendasi_produk.get(jenis_kulit, 'Jenis kulit tidak ditemukan.')
    return render_template('hasil_rekomendasi.html', jenis_kulit=jenis_kulit, rekomendasi=rekomendasi)

if __name__ == '__main__':
    app.run(debug=True)

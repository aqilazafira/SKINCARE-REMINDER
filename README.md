## Setup Projek

```sh
// install dependencies
pip install -r requirements.txt

// inisialisasi database
flask init-db

// menjalankan aplikasi
python run.py

// aktifkan virtual environment
. .venv/Scripts/activate

//tes code coverage
python -m pytest --cov=app tests

//install pytest cov
pip install pytest-cov

//update requirements
pip freeze > ./requirements.txt
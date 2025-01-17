import io

from PIL import Image
from werkzeug.datastructures import FileStorage
from flask import url_for
from app import db
from app.models import Product, Recommendation, SkincareType

def create_test_image():
    img = Image.new('RGB', (100, 100), color = (73, 109, 137))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    return img_byte_arr

def test_product_creation(auth_client, init_db):
    file_storage = FileStorage(stream=create_test_image(), filename='test.jpg', content_type='image/jpeg')
    data = {
        'brand': 'Test Brand',
        'description': 'Test Description',
        'recommendations': 'Berminyak',
        'skincareTypes': 'Cleanser',
        'file': file_storage,
    }
    response = auth_client.post('/admin/rekomendasi', data=data, content_type='multipart/form-data', follow_redirects=True)

    assert response.status_code == 200
    product = Product.query.filter_by(brand='Test Brand').first()
    assert product is not None
    assert product.description == 'Test Description'

def test_product_update(auth_client, init_db):
    product = Product(brand='Old Brand', description='Old Description', image_url='old.jpg')
    db.session.add(product)
    db.session.commit()
    response = auth_client.put(f'/admin/rekomendasi/{product.id}', data=dict(
        brand='New Brand',
        description='New Description',
        recommendations='Kering',
        skincareTypes='Toner'
    ), follow_redirects=True)
    assert response.status_code == 200
    updated_product = Product.query.get(product.id)
    assert updated_product.brand == 'New Brand'
    assert updated_product.description == 'New Description'

def test_product_deletion(auth_client, init_db):
    product = Product(brand='Delete Brand', description='Delete Description', image_url='delete.jpg')
    db.session.add(product)
    db.session.commit()
    response = auth_client.delete(f'/admin/rekomendasi/{product.id}', follow_redirects=True)
    assert response.status_code == 200
    deleted_product = Product.query.get(product.id)
    assert deleted_product is None

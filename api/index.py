from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

connection = psycopg2.connect(
    dbname="pawpals",
    user="postgres",
    password="123456",
    host="localhost",
    cursor_factory=RealDictCursor
)

cloudinary.config(
    cloud_name="USERNAME",
    api_key="API KEY",
    api_secret="SECRET KEY"
)

@app.route('/')
def home():
    return 'Hello, Pawpals 4geeks!'

@app.route('/about')
def about():
    return 'About'

@app.route('/register-pets-users', methods=['POST'])
def register_pets_users():
    body = request.get_json()
    username = body.get('username')
    email = body.get('email')
    photo = 'https://static.scientificamerican.com/sciam/cache/file/E235EE4C-5D9A-44A3-9D0E30F0035C3151_source.jpg?w=1200'
    password = body.get('password')
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO pets_users (username, email, photo, password)
        VALUES (%s, %s, %s, %s)""", [username, email, photo, password]
    )
    connection.commit()
    cursor.close()
    return jsonify({"message": "Usuario mascota creado correctamente"}), 201

@app.route('/register-services-users', methods=['POST'])
def register_services_users():
    body = request.get_json()
    username = body.get('username')
    email = body.get('email')
    photo = 'https://assets.petco.com/petco/image/upload/f_auto,q_auto:best/vet-services-vetco-total-care-lifestyle-img-800x577'
    password = body.get('password')
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO services_users (username, email, photo, password)
        VALUES (%s, %s, %s, %s)""", [username, email, photo, password]
    )
    connection.commit()
    cursor.close()
    return jsonify({"message": "Usuario empresa creado correctamente"}), 201

@app.route('/login-pets-users', methods=['POST'])
def login_pets_users():
    body = request.get_json()
    email = body.get('email')
    password = body.get('password')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM pets_users WHERE email = %s", [email])
    result = cursor.fetchone()
    password_compare = result.get('password')
    if password == password_compare:
        return jsonify({"message": "Usuario autenticado correctamente"}), 200
    return jsonify({"message": "Credenciales invalidas"}), 401

@app.route('/login-services-users', methods=['POST'])
def login_services_users():
    body = request.get_json()
    email = body.get('email')
    password = body.get('password')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM services_users WHERE email = %s", [email])
    result = cursor.fetchone()
    password_compare = result.get('password')
    if password == password_compare:
        return jsonify({"message": "Usuario autenticado correctamente"}), 200
    return jsonify({"message": "Credenciales invalidas"}), 401

@app.route('/create-new-pets-posts', methods=['POST'])
def create_new_pets_posts():
    return "Create new pets posts"

@app.route('/create-new-services-posts', methods=['POST'])
def create_new_services_posts():
    return "Create new pets posts"

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    result = cloudinary.uploader.upload(file)
    return jsonify({"url": result['secure_url']})

app.run(host='0.0.0.0', port=3000, debug=True)
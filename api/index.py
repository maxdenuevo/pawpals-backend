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
    cloud_name="<cloud_name>",
    api_key="<api_key>",
    api_secret="<api_secret>"
)

@app.route('/')
def home():
    return 'Hello, Pawpals 4geeks!'

@app.route('/register-pets-users', methods=['POST'])
def register_pets_users():
    cursor = connection.cursor()
    try:
        body = request.get_json()
        username = body.get('username')
        email = body.get('email')
        photo = 'https://static.scientificamerican.com/sciam/cache/file/E235EE4C-5D9A-44A3-9D0E30F0035C3151_source.jpg?w=1200'
        password = body.get('password')
        cursor.execute("""
            INSERT INTO pets_users (username, email, photo, password)
            VALUES (%s, %s, %s, %s)""", [username, email, photo, password]
        )
        connection.commit()
        cursor.close()
        return jsonify({"message": "Usuario mascota creado correctamente"}), 201
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al crear usuario"}), 500
    finally:
        cursor.close()

@app.route('/register-services-users', methods=['POST'])
def register_services_users():
    cursor = connection.cursor()
    try:
        body = request.get_json()
        username = body.get('username')
        email = body.get('email')
        photo = 'https://assets.petco.com/petco/image/upload/f_auto,q_auto:best/vet-services-vetco-total-care-lifestyle-img-800x577'
        password = body.get('password')
        cursor.execute("""
            INSERT INTO services_users (username, email, photo, password)
            VALUES (%s, %s, %s, %s)""", [username, email, photo, password]
        )
        connection.commit()
        cursor.close()
        return jsonify({"message": "Usuario empresa creado correctamente"}), 201
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al crear usuario"}), 500
    finally:
        cursor.close()

@app.route('/login-pets-users', methods=['POST'])
def login_pets_users():
    cursor = connection.cursor()
    try:
        body = request.get_json()
        email = body.get('email')
        password = body.get('password')
        cursor.execute("SELECT * FROM pets_users WHERE email = %s", [email])
        result = cursor.fetchone()
        password_compare = result.get('password')
        if password == password_compare:
            return jsonify({"message": "Usuario autenticado correctamente"}), 200
        return jsonify({"message": "Credenciales invalidas"}), 401
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al autenticar usuario"}), 500
    finally:
        cursor.close()

@app.route('/login-services-users', methods=['POST'])
def login_services_users():
    cursor = connection.cursor()
    try:
        body = request.get_json()
        email = body.get('email')
        password = body.get('password')
        cursor.execute("SELECT * FROM services_users WHERE email = %s", [email])
        result = cursor.fetchone()
        password_compare = result.get('password')
        if password == password_compare:
            return jsonify({"message": "Usuario autenticado correctamente"}), 200
        return jsonify({"message": "Credenciales invalidas"}), 401
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al autenticar usuario"}), 500
    finally:
        cursor.close()

@app.route("/get-pets-posts", methods=["GET"])
def get_pets_posts():
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM pets_posts")
        results = cursor.fetchall()
        cursor.close()
        return jsonify({"posts": results})
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al obtener posts"}), 500
    finally:
        cursor.close()

@app.route("/get-services-posts", methods=["GET"])
def get_services_posts():
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM services_posts")
        results = cursor.fetchall()
        cursor.close()
        return jsonify({"posts": results})
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al obtener posts"}), 500
    finally:
        cursor.close()

@app.route('/get-pet-profile/<int:id_pet_user>')
def get_pet_profile(id_pet_user):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM pets_users WHERE id_pet_user = %s", [id_pet_user])
        result = cursor.fetchone()
        cursor.close()
        return jsonify({"profile": result})
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al obtener perfil"}), 500
    finally:
        cursor.close()

@app.route('/get-service-profile/<int:id_service_user>')
def get_service_profile(id_service_user):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM services_users WHERE id_service_user = %s", [id_service_user])
        result = cursor.fetchone()
        cursor.close()
        return jsonify({"profile": result})
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al obtener perfil"}), 500
    finally:
        cursor.close()

@app.route('/create-new-pets-posts', methods=['POST'])
def create_new_pets_posts():
    cursor = connection.cursor()
    try:
        data = request.form
        title = data.get('title')
        description = data.get('description')
        id_pet_user = int(data.get('id_pet_user'))
        photo = request.files['photo']
        result = cloudinary.uploader.upload(photo)
        photo_url = result['secure_url']
        cursor.execute("""
        INSERT INTO pets_posts (title, photo, description, id_pet_user)
        VALUES (%s, %s, %s, %s);
        """, [title, photo_url, description, id_pet_user]
        )
        connection.commit()
        cursor.close()
        return jsonify({"message": "Post creado correctamente"}), 201
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al crear post"}), 500
    finally:
        cursor.close()

@app.route('/create-new-services-posts', methods=['POST'])
def create_new_services_posts():
    cursor = connection.cursor()
    try:
        data = request.form
        title = data.get('title')
        description = data.get('description')
        id_service_user = int(data.get('id_service_user'))
        photo = request.files['photo']
        result = cloudinary.uploader.upload(photo)
        photo_url = result['secure_url']
        cursor.execute("""
        INSERT INTO services_posts (title, photo, description, id_service_user)
        VALUES (%s, %s, %s, %s);
        """, [title, photo_url, description, id_service_user]
        )
        connection.commit()
        cursor.close()
        return jsonify({"message": "Post creado correctamente"}), 201
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al crear post"}), 500
    finally:
        cursor.close()

@app.route('/create-new-comment-pets-posts', methods=['POST'])
def create_new_comment_pets_posts():
    cursor = connection.cursor()
    try:
        body = request.get_json()
        comment = body.get('comment')
        id_pet_post = body.get('id_pet_post')
        id_pet_user = body.get('id_pet_user')
        
        cursor.execute("""
            INSERT INTO pets_comments (comment, id_pet_post, id_pet_user) 
            VALUES (%s, %s,  %s);
        """, [comment, id_pet_post, id_pet_user]
        )
        connection.commit()
        cursor.close()
        return jsonify({"message": "Comentario creado correctamente"}), 201
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al crear comentario"}), 500
    finally:
        cursor.close()

@app.route('/create-new-comment-services-posts', methods=['POST'])
def create_new_comment_services_posts():
    cursor = connection.cursor()
    try:
        body = request.get_json()
        comment = body.get('comment')
        id_service_post = body.get('id_service_post')
        id_service_user = body.get('id_service_user')
        cursor.execute("""
            INSERT INTO services_comments (comment, id_service_post, id_service_user) 
            VALUES (%s, %s,  %s);
        """, [comment, id_service_post, id_service_user]
        )
        connection.commit()
        cursor.close()
        return jsonify({"message": "Comentario creado correctamente"}), 201
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al crear comentario"}), 500
    finally:
        cursor.close()

@app.route('/update-pet-profile/<int:id_pet_user>', methods=["PATCH"])
def update_pet_profile(id_pet_user):
    cursor = connection.cursor()
    try:
        photo = request.files['photo']
        result = cloudinary.uploader.upload(photo)
        photo_url = result['secure_url']
        cursor.execute("""
            UPDATE pets_users 
            SET photo = %s
            WHERE id_pet_user = %s;
        """, [photo_url, id_pet_user])
        connection.commit()
        cursor.close()
        return jsonify({"message": "Perfil actualizado correctamente"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al actualizar perfil"}), 500
    finally:
        cursor.close()

@app.route('/update-service-profile/<int:id_service_user>', methods=["PATCH"])
def update_services_profile(id_service_user):
    cursor = connection.cursor()
    try:
        photo = request.files['photo']
        result = cloudinary.uploader.upload(photo)
        photo_url = result['secure_url']
        cursor.execute("""
            UPDATE services_users 
            SET photo = %s
            WHERE id_service_user = %s;
        """, [photo_url, id_service_user])
        connection.commit()
        cursor.close()
        return jsonify({"message": "Perfil actualizado correctamente"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al actualizar perfil"}), 500
    finally:
        cursor.close()

@app.route('/search-pets-users', methods=["GET"])
def search_pets_users():
    cursor = connection.cursor()
    try:
        params = request.args
        username = params.get('username')
        cursor.execute(
            """
            SELECT * FROM pets_users WHERE username ILIKE %s
            """,
            ['%' + username + '%']
        )
        results = cursor.fetchall()
        cursor.close()
        return jsonify({"results": results}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al buscar usuarios"}), 500
    finally:
        cursor.close()

@app.route('/search-services-users', methods=["GET"])
def search_services_users():
    cursor = connection.cursor()
    try:
        params = request.args
        username = params.get('username')
        cursor.execute(
            """
            SELECT * FROM services_users WHERE username ILIKE %s
            """,
            ['%' + username + '%']
        )
        results = cursor.fetchall()
        cursor.close()
        return jsonify({"results": results}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al buscar usuarios"}), 500
    finally:
        cursor.close()

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        result = cloudinary.uploader.upload(file)
        return jsonify({"url": result['secure_url']})
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al subir imagen"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
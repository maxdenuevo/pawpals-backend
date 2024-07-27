-- Eliminar tablas (opcional)
DROP TABLE pets_posts;
DROP TABLE services_posts;
DROP TABLE pets_users;
DROP TABLE services_users;

-- Tabla de usuarios de mascotas
CREATE TABLE pets_users (
    id_pet_user SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE, 
    email VARCHAR(255) UNIQUE,
    photo TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    password VARCHAR(255)
);

-- Tabla de usuarios de servicios
CREATE TABLE services_users (
    id_service_user SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE, 
    email VARCHAR(255) UNIQUE,
    photo TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    password VARCHAR(255)
);

-- Tabla de publicaciones de mascotas
CREATE TABLE pets_posts (
    id_pet_post SERIAL PRIMARY KEY,
    title VARCHAR(255),
    photo TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_pet_user INT,
    CONSTRAINT fk_pets_posts_pets_users FOREIGN KEY (id_pet_user)
    REFERENCES pets_users (id_pet_user)
);

-- Tabla de publicaciones de servicios
CREATE TABLE services_posts (
    id_service_post SERIAL PRIMARY KEY,
    title VARCHAR(255),
    photo TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_service_user INT,
    CONSTRAINT fk_services_posts_services_users FOREIGN KEY (id_service_user)
    REFERENCES services_users (id_service_user)
);

-- Tabla de comentarios muchos a muchos entre usuarios pets y posts de pets
CREATE TABLE pets_comments (
    id_pet_comment SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    comment TEXT,
    id_pet_post INT,
    id_pet_user INT,
    CONSTRAINT fk_pets_comments_pets_posts FOREIGN KEY (id_pet_post)
    REFERENCES pets_posts (id_pet_post),
    CONSTRAINT fk_pets_comments_pets_users FOREIGN KEY (id_pet_user)
    REFERENCES pets_users (id_pet_user)
);

-- Tabla de comentarios muchos a muchos entre usuarios servicios y posts de servicios
CREATE TABLE services_comments (
    id_service_comment SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    comment TEXT,
    id_service_post INT,
    id_service_user INT,
    CONSTRAINT fk_services_comments_services_posts FOREIGN KEY (id_service_post)
    REFERENCES services_posts (id_service_post),
    CONSTRAINT fk_services_comments_services_users FOREIGN KEY (id_service_user)
    REFERENCES services_users (id_service_user)
);
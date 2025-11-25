import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()

db_password = os.getenv("DB_PASSWORD")

if db_password is None:
    raise RuntimeError(
        "DB_PASSWORD is not set. Please define it in your environment or .env file."
    )

db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": db_password,
    "database": os.getenv("DB_NAME", "busticketapp")
}

connection_pool = pooling.MySQLConnectionPool(
    pool_name="bus_booking_pool",
    pool_size=5,
    pool_reset_session=True,
    **db_config
)

def get_db_connection():
    return connection_pool.get_connection()

def init_database():
    """Initialize database schema"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS districts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dropping_points (
            id INT AUTO_INCREMENT PRIMARY KEY,
            district_id INT NOT NULL,
            name VARCHAR(100) NOT NULL,
            price INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (district_id) REFERENCES districts(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bus_providers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            contact_info TEXT,
            address TEXT,
            privacy_policy TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS provider_routes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            provider_id INT NOT NULL,
            district_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (provider_id) REFERENCES bus_providers(id),
            FOREIGN KEY (district_id) REFERENCES districts(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            booking_reference VARCHAR(20) NOT NULL UNIQUE,
            customer_name VARCHAR(100) NOT NULL,
            customer_phone VARCHAR(20) NOT NULL,
            from_district VARCHAR(100) NOT NULL,
            to_district VARCHAR(100) NOT NULL,
            dropping_point VARCHAR(100) NOT NULL,
            bus_provider VARCHAR(100) NOT NULL,
            travel_date DATE NOT NULL,
            fare INT NOT NULL,
            status VARCHAR(20) DEFAULT 'confirmed',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bus_documents (
            id INT AUTO_INCREMENT PRIMARY KEY,
            provider_name VARCHAR(100) NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

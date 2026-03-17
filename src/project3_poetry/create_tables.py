import psycopg2
from config import load_config

def create_tables():
    """Create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE brand (
            brand_id SERIAL PRIMARY KEY,
            brand_name VARCHAR(100) NOT NULL,
            country VARCHAR(50) NOT NULL,
            created_at TIMESTAMP NOT NULL
        )
        """,
        """
        CREATE TABLE category (
            category_id SERIAL PRIMARY KEY,
            category_name VARCHAR(100) NOT NULL,
            parent_category_id INT REFERENCES category (category_id) ,
            level SMALLINT NOT NULL,
            created_at TIMESTAMP NOT NULL
        )
        """,
        """
        CREATE TABLE seller (
            seller_id SERIAL PRIMARY KEY,
            seller_name VARCHAR(150) NOT NULL,
            join_date DATE NOT NULL,
            seller_type VARCHAR(50) NOT NULL,
            rating DECIMAL(2,1) NOT NULL,
            country VARCHAR(50) NOT NULL
        )
        """,
        """
        CREATE TABLE product (
            product_id SERIAL PRIMARY KEY,
            product_name VARCHAR(200) NOT NULL,
            category_id INT NOT NULL REFERENCES category (category_id),
            brand_id INT NOT NULL REFERENCES brand (brand_id),
            seller_id INT NOT NULL REFERENCES seller (seller_id),
            price DECIMAL(12,2) NOT NULL,
            discount_price DECIMAL(12,2) NOT NULL,
            stock_qty INT NOT NULL,
            rating FLOAT NOT NULL,
            created_at TIMESTAMP NOT NULL,
            is_active BOOLEAN NOT NULL
        )
        """,
        """
        CREATE TABLE orders (
            order_id SERIAL PRIMARY KEY,
            order_date TIMESTAMP NOT NULL,
            seller_id INT NOT NULL REFERENCES seller (seller_id),
            status VARCHAR(20) NOT NULL,
            total_amount DECIMAL(12,2) NOT NULL,
            created_at TIMESTAMP NOT NULL
        )
        """,
        """
        CREATE TABLE order_item (
            order_item_id SERIAL PRIMARY KEY,
            order_id INT NOT NULL REFERENCES orders (order_id),
            product_id INT NOT NULL REFERENCES product (product_id),
            quantity INT NOT NULL,
            unit_price DECIMAL(12,2) NOT NULL,
            subtotal DECIMAL(12,2) NOT NULL
        )
        """,
        """
        CREATE TABLE promotions (
            promotion_id SERIAL PRIMARY KEY,
            promotion_name VARCHAR(100) NOT NULL,
            promotion_type VARCHAR(50) NOT NULL,
            discount_type VARCHAR(20) NOT NULL,
            discount_value NUMERIC(10,2) NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL
        )
        """,
        """
        CREATE TABLE promotion_products (
            promo_product_id SERIAL PRIMARY KEY,
            promotion_id INT NOT NULL REFERENCES promotions (promotion_id),
            product_id INT NOT NULL REFERENCES product (product_id),
            created_at TIMESTAMP NOT NULL
        )
        """,
    )
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                #execute the CREATE TABLE statement
                for command in commands:
                    cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__ == '__main__':
    create_tables()
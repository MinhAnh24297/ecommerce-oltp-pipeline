import psycopg2
from config import load_config
import random
from datetime import datetime, timedelta
from faker import Faker

faker = Faker()

ORDER_COUNT = 2500000

def insert_orders(cur, conn):
    #fetch valid seller_ids and their products to ensure relational consistency
    cur.execute("SELECT seller_id, product_id, price, discount_price FROM product")
    product_data = cur.fetchall() #list of (seller_id, product_id, price, discount_price)

    #organize products by seller for faster look up
    seller_to_product = dict()
    for seller_id, product_id, price, discount_price in product_data:
        price = float(price)
        discount_price = float(discount_price)
        if seller_id not in seller_to_product:
            seller_to_product[seller_id] = []
        seller_to_product[seller_id].append((product_id, price, discount_price))

    seller_ids = list(seller_to_product.keys())

    #status distribution probability
    status_type = ["PLACED", "PAID", "SHIPPED", "DELIVERED", "CANCELLED", "RETURNED"]
    weights = [5, 4, 11, 70, 7, 3]

    order_batch = []
    order_item_batch = []
    batch_size = 10000 # batching for performance

    for i in range(ORDER_COUNT):
        order_id = i + 1
        order_date = faker.date_time_between(start_date=datetime(2025, 8, 1), end_date=datetime(2025, 10, 31))
        seller_id = random.choice(seller_ids)
        status = random.choices(status_type, weights)[0]
        created_at = order_date + timedelta(days=random.randint(1, 3))
        #generate 3-4 items per order
        num_items = random.randint(3,4)
        total_amount = 0
        for _ in range(num_items):
            #ensure products belong to the same seller
            product_id, price, discount_price = random.choice(seller_to_product[seller_id])
            quantity = random.randint(1, 5)
            unit_price = random.choice([price, discount_price])
            subtotal = round(quantity * unit_price, 2)
            total_amount += subtotal

            order_item_batch.append((order_id, product_id, quantity, unit_price, subtotal))

        order_batch.append((order_id, order_date, seller_id, status, round(total_amount, 2), created_at))

        #execute batch insert
        if len(order_batch) >= batch_size:
            cur.executemany(
                """
                INSERT INTO \"orders\" (order_id, order_date, seller_id, status, total_amount, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                """, order_batch
            )
            cur.executemany(
                """
                INSERT INTO "order_item" (order_id, product_id, quantity, unit_price, subtotal)
                VALUES (%s, %s, %s, %s, %s)
                """, order_item_batch
            )
            conn.commit()
            print(f"Done inserting {i+1} order")
            order_batch, order_item_batch = [], []

def seed_data():
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                insert_orders(cur, conn)
                print("Generation completed")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == "__main__":
    seed_data()



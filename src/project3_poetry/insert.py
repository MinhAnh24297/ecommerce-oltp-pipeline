import psycopg2
from config import load_config
import random
from datetime import timedelta
from faker import Faker

faker = Faker()

BRAND_COUNT = 20
SELLER_COUNT = 25
PRODUCT_COUNT = 2000
PROMOTION_COUNT = 10
PROMOTION_PRODUCT_COUNT = 100


def insert_brands(cur):
    # insert new row into the brand table & return the inserted brand_ids
    brand_ids = []
    for _ in range(BRAND_COUNT):
        brand_id = None
        cur.execute(
            """
            INSERT INTO brand (brand_name, country, created_at)
            VALUES (%s, %s, %s)
            RETURNING brand_id
            """,
            (
                faker.company(),
                faker.country(),
                faker.date_time_this_decade(),
            ),
        )
        # get the generated id back
        rows = cur.fetchone()
        if rows:
            brand_id = rows[0]
        brand_ids.append(brand_id)
    return brand_ids

def insert_categories(cur):
    category_ids = []
    parent_category = ["Electronics", "Fashion", "Beauty", "Home"]
    child_category = ["Phones", "Laptop", "Men Clothing", "Women Clothing", "Skincare", "Makeup", "Kitchen"]
    #parent categories
    parent_category_ids = []
    for category in parent_category:
        parent_category_id = None
        cur.execute(
            """
            INSERT INTO category (category_name, parent_category_id, level, created_at)
            VALUES (%s, %s, %s, %s)
            RETURNING category_id
            """,
            (
                category,
                None,
                1,
                faker.date_time_this_year()
            ),
        )
        #get the generated id back
        rows = cur.fetchone()
        if rows:
            parent_category_id = rows[0]
        parent_category_ids.append(parent_category_id)
        category_ids.append(parent_category_id)

    #child category
    for category in child_category:
        child_category_id = None
        cur.execute(
            """
            INSERT INTO category (category_name, parent_category_id, level, created_at)
            VALUES (%s, %s, %s, %s)
            RETURNING category_id
            """,
            (
                category,
                random.choice(parent_category_ids),
                2,
                faker.date_time_this_year()
            )
        )
        #get the generated id back
        rows = cur.fetchone()
        if rows:
            child_category_id = rows[0]
        category_ids.append(child_category_id)

    return category_ids

def insert_sellers(cur):
    seller_ids = []
    seller_types = ["Individual", "Business", "Official", "Marketplace"]
    for _ in range(SELLER_COUNT):
        seller_id = None
        cur.execute(
            """
            INSERT INTO seller (seller_name, join_date, seller_type, rating, country)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING seller_id
            """,
            (
                faker.company(),
                faker.date_between(start_date="-4y", end_date="today"),
                random.choice(seller_types),
                round(random.uniform(3,5), 1),
                "Vietnam",
            ),
        )
        #get the generated id back
        rows = cur.fetchone()
        if rows:
            seller_id = rows[0]
        seller_ids.append(seller_id)

    return seller_ids

def insert_products(cur, category_ids, brand_ids, seller_ids):
    product_ids = []
    for _ in range(PRODUCT_COUNT):
        product_id = None
        price = random.uniform(100000, 50000000)
        discount_price = price * random.uniform(0.7, 1.0)
        cur.execute(
            """
            INSERT INTO product (product_name, category_id, brand_id, seller_id, price, discount_price, stock_qty, rating, created_at, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING product_id
            """,
            (
                faker.catch_phrase(),
                random.choice(category_ids),
                random.choice(brand_ids),
                random.choice(seller_ids),
                price,
                discount_price,
                random.randint(0, 500),
                round(random.uniform(3,5), 1),
                faker.date_time_between(start_date="-3y", end_date="now"),
                random.choice([True, False])
            )
        )
        #get the generated id back
        rows = cur.fetchone()
        if rows:
            product_id = rows[0]
        product_ids.append(product_id)

    return product_ids

def insert_promotions(cur):
    promotion_ids = []
    promotion_types = ["Flash Sale", "Campaign", "Seasonal", "Voucher"]
    discount_types = ["percentage", "fixed amount"]
    for i in range(PROMOTION_COUNT):
        promotion_id = None
        discount_type = random.choice(discount_types)
        discount_value = round(random.uniform(5, 80), 2) if discount_type == "percentage" else round(random.uniform(50000, 1000000), 2)
        start_date = faker.date_between(start_date="-6mo", end_date="today")
        end_date = start_date + timedelta(days=random.randint(30, 50))
        cur.execute(
            """
            INSERT INTO promotions (promotion_name, promotion_type, discount_type, discount_value, start_date, end_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING promotion_id
            """,
            (
                f"Promotion {i + 1}",
                random.choice(promotion_types),
                discount_type,
                discount_value,
                start_date,
                end_date
            )
        )
        #get the generated id back
        rows = cur.fetchone()
        if rows:
            promotion_id = rows[0]
        promotion_ids.append(promotion_id)

    return promotion_ids

def insert_promotion_products(cur, promotion_ids, product_ids):
    used_pairs = set()
    while len(used_pairs) < PROMOTION_PRODUCT_COUNT:
        promotion_id = random.choice(promotion_ids)
        product_id = random.choice(product_ids)
        pair = (promotion_id, product_id)

        if pair in used_pairs:
            continue
        used_pairs.add(pair)
        cur.execute(
            """
            INSERT INTO promotion_products (promotion_id, product_id, created_at)
            VALUES (%s, %s, %s)
            """,
            (
                promotion_id,
                product_id,
                faker.date_time_this_year()
             )
        )

def seed_data():
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                #execute the INSERT statement
                brand_ids = insert_brands(cur)
                category_ids = insert_categories(cur)
                seller_ids = insert_sellers(cur)
                product_ids = insert_products(cur, category_ids, brand_ids, seller_ids)
                promotion_ids = insert_promotions(cur)
                insert_promotion_products(cur, promotion_ids, product_ids)

                #commit the changes to the database
                conn.commit()
                print("fake data inserted successfully")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == "__main__":
    seed_data()



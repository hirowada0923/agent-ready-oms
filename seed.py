from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.models import Product, Customer

def seed_data():
    # テーブル作成
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 商品データの投入
        if db.query(Product).count() == 0:
            products = [
                Product(name="MacBook Pro 14", price=248000, stock_quantity=10),
                Product(name="iPhone 15 Pro", price=159800, stock_quantity=20),
                Product(name="AirPods Pro", price=39800, stock_quantity=50),
            ]
            db.add_all(products)
            print("Products added.")

        # 顧客データの投入
        if db.query(Customer).count() == 0:
            customers = [
                Customer(name="山田 太郎", address="東京都渋谷区...", contact="090-0000-0000"),
                Customer(name="株式会社テック", address="大阪府大阪市...", contact="info@tech-corp.com"),
            ]
            db.add_all(customers)
            print("Customers added.")

        db.commit()
        print("Seed completed successfully.")
    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()

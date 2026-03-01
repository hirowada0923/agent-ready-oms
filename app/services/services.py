from sqlalchemy.orm import Session
from app.models.models import Customer, Product, Order, OrderItem
import uuid

class MasterService:
    @staticmethod
    def get_products(db: Session):
        return db.query(Product).all()

    @staticmethod
    def create_product(db: Session, name: str, price: int, stock: int):
        product = Product(name=name, price=price, stock_quantity=stock)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def update_product_stock(db: Session, product_id: int, new_stock: int):
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            product.stock_quantity = new_stock
            db.commit()
            db.refresh(product)
        return product

    @staticmethod
    def delete_product(db: Session, product_id: int):
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            db.delete(product)
            db.commit()
        return product

    @staticmethod
    def get_customers(db: Session):
        return db.query(Customer).all()

    @staticmethod
    def create_customer(db: Session, name: str, address: str, contact: str, name_kana: str = None):
        customer = Customer(name=name, name_kana=name_kana, address=address, contact=contact)
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer

    @staticmethod
    def delete_customer(db: Session, customer_id: int):
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if customer:
            # 受注データの存在チェック
            order_count = db.query(Order).filter(Order.customer_id == customer_id).count()
            if order_count > 0:
                raise Exception(f"この顧客には{order_count}件の受注データが紐づいているため削除できません。")
            
            db.delete(customer)
            db.commit()
        return customer

class OrderService:
    @staticmethod
    def create_order(db: Session, customer_id: int, items_data: list):
        """
        items_data: list of dicts like {"product_id": 1, "quantity": 2}
        """
        try:
            # 1. 在庫チェックと合計金額の計算
            total_amount = 0
            order_items = []
            
            for item in items_data:
                product = db.query(Product).filter(Product.id == item["product_id"]).with_for_update().first()
                if not product:
                    raise Exception(f"Product ID {item['product_id']} not found.")
                
                if product.stock_quantity < item["quantity"]:
                    raise Exception(f"Insufficient stock for {product.name} (Available: {product.stock_quantity})")
                
                # 在庫を減らす
                product.stock_quantity -= item["quantity"]
                
                total_amount += product.price * item["quantity"]
                order_items.append(
                    OrderItem(
                        product_id=product.id,
                        quantity=item["quantity"],
                        unit_price=product.price
                    )
                )

            # 2. 受注データの作成
            order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
            new_order = Order(
                order_number=order_number,
                customer_id=customer_id,
                total_amount=total_amount,
                status="未対応"
            )
            
            # アイテムを紐付け
            for oi in order_items:
                new_order.items.append(oi)
            
            db.add(new_order)
            db.commit()
            db.refresh(new_order)
            return new_order
            
        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def get_orders(db: Session, status: str = None):
        query = db.query(Order)
        if status and status not in ["ALL", "すべて", ""]:
            query = query.filter(Order.status == status)
        return query.order_by(Order.created_at.desc()).all()

    @staticmethod
    def update_status(db: Session, order_id: int, new_status: str):
        order = db.query(Order).filter(Order.id == order_id).first()
        if order:
            order.status = new_status
            db.commit()
            db.refresh(order)
        return order

from fastapi import FastAPI, Depends, Request, Form, HTTPException, Header
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import engine, get_db, Base
from app.models.models import Product, Customer, Order
from app.services.services import MasterService, OrderService
import os

# データベーステーブルの作成
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Python OMS")

# 静的ファイルとテンプレートの設定
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    total_orders = db.query(Order).count()
    total_products = db.query(Product).count()
    total_sales = sum([o.total_amount for o in db.query(Order).all()])
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "total_orders": total_orders,
        "total_products": total_products,
        "total_sales": total_sales
    })

@app.get("/orders", response_class=HTMLResponse)
async def orders_page(request: Request, status: str = "すべて", db: Session = Depends(get_db)):
    orders = OrderService.get_orders(db, status)
    products = MasterService.get_products(db)
    customers = MasterService.get_customers(db)
    return templates.TemplateResponse("orders.html", {
        "request": request,
        "orders": orders,
        "products": products,
        "customers": customers,
        "current_status": status
    })

@app.post("/orders/{order_id}/status")
async def update_order_status(
    order_id: int,
    status: str = Form(...),
    db: Session = Depends(get_db)
):
    OrderService.update_status(db, order_id, status)
    return RedirectResponse(url="/orders", status_code=303)

@app.post("/orders/create")
async def create_order(
    customer_id: int = Form(...),
    product_ids: list[int] = Form(...),
    quantities: list[int] = Form(...),
    db: Session = Depends(get_db)
):
    items_data = []
    for pid, qty in zip(product_ids, quantities):
        if qty > 0:
            items_data.append({"product_id": pid, "quantity": qty})
    
    try:
        OrderService.create_order(db, customer_id, items_data)
        return RedirectResponse(url="/orders", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/master/products", response_class=HTMLResponse)
async def products_page(request: Request, db: Session = Depends(get_db)):
    products = MasterService.get_products(db)
    return templates.TemplateResponse("products.html", {"request": request, "products": products})

@app.post("/master/products/create")
async def create_product(
    name: str = Form(...),
    price: int = Form(...),
    stock: int = Form(...),
    db: Session = Depends(get_db)
):
    MasterService.create_product(db, name, price, stock)
    return RedirectResponse(url="/master/products", status_code=303)

@app.post("/master/products/{product_id}/stock")
async def update_product_stock(
    product_id: int,
    stock: int = Form(...),
    db: Session = Depends(get_db)
):
    MasterService.update_product_stock(db, product_id, stock)
    return RedirectResponse(url="/master/products", status_code=303)

@app.get("/master/customers", response_class=HTMLResponse)
async def customers_page(request: Request, db: Session = Depends(get_db)):
    customers = MasterService.get_customers(db)
    return templates.TemplateResponse("customers.html", {"request": request, "customers": customers})

@app.post("/master/customers/create")
async def create_customer(name: str = Form(...), name_kana: str = Form(None), address: str = Form(...), contact: str = Form(...), db: Session = Depends(get_db)):
    MasterService.create_customer(db, name, address, contact, name_kana)
    return RedirectResponse(url="/master/customers", status_code=303)
@app.post("/master/customers/{customer_id}/delete")
async def delete_customer_endpoint(
    customer_id: int, 
    x_requested_with: str = Header(None),
    db: Session = Depends(get_db)
):
    if x_requested_with != "XMLHttpRequest":
        return {"success": False, "message": "不正なリクエストです(CSRF保護)。"}
        
    try:
        MasterService.delete_customer(db, customer_id)
        return {"success": True, "message": "顧客を正常に削除しました。"}
    except Exception as e:
        return {"success": False, "message": str(e)}
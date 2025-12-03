from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.decorators import login_required
from app.models.product import Product
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.customer import Customer
from app.extensions import db

sales_bp = Blueprint("sales", __name__, url_prefix="/sales")


@sales_bp.route("/")
@login_required
def list_sales():
    """Lista todas las ventas"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    sales_query = Sale.query.order_by(Sale.date.desc())
    
    # filtro por usuario
    if session.get("user_role") != "admin":
        sales_query = sales_query.filter_by(user_id=session.get("user_id"))
    
    sales_pagination = sales_query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template("sales/list.html", sales=sales_pagination)


@sales_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_sale():
    """Crear nueva venta"""
    if request.method == "POST":
        try:
            # obtener datos del formulario
            customer_id = request.form.get("customer_id")
            payment_method = request.form.get("payment_method", "efectivo")
            notes = request.form.get("notes")
            
            # obtener productos y cantidades
            product_ids = request.form.getlist("product_id[]")
            quantities = request.form.getlist("quantity[]")
            
            if not product_ids:
                flash("Debes agregar al menos un producto", "danger")
                return redirect(url_for("sales.new_sale"))
            
            # crear la venta
            new_sale = Sale(
                user_id=session.get("user_id"),
                customer_id=int(customer_id) if customer_id else None,
                payment_method=payment_method,
                notes=notes,
                total=0 
            )
            
            db.session.add(new_sale)
            db.session.flush()  # obtener el ID de la venta
            
            total = 0
            
            # agregar items de la venta
            for product_id, quantity in zip(product_ids, quantities):
                if not product_id or not quantity:
                    continue
                
                product = Product.query.get(int(product_id))
                if not product:
                    continue
                
                qty = int(quantity)
                
                # verificar stock
                if product.stock < qty:
                    db.session.rollback()
                    flash(f"Stock insuficiente para {product.name}. Disponible: {product.stock}", "danger")
                    return redirect(url_for("sales.new_sale"))
                
                subtotal = product.price * qty
                
                sale_item = SaleItem(
                    sale_id=new_sale.id,
                    product_id=product.id,
                    quantity=qty,
                    unit_price=product.price,
                    subtotal=subtotal
                )
                
                db.session.add(sale_item)
                
                # actualizar stock
                product.stock -= qty
                
                total += subtotal
            
            # actualizar total de la venta
            new_sale.total = total
            
            db.session.commit()
            
            flash(f"Venta #{new_sale.id} registrada exitosamente. Total: ${total:.2f}", "success")
            return redirect(url_for("sales.view_sale", id=new_sale.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f"Error al registrar la venta: {str(e)}", "danger")
            return redirect(url_for("sales.new_sale"))
    
    # GET mostrar formulario
    products = Product.query.filter(Product.stock > 0).all()
    customers = Customer.query.all()

    # Convertir a diccionarios JSON serializables
    product_list = [
        {
            "id": p.id,
            "name": p.name,
            "price": float(p.price),
            "stock": p.stock
        }
        for p in products
    ]

    customer_list = [
        {
            "id": c.id,
            "name": c.name
        }
        for c in customers
    ]

    return render_template(
        "sales/new.html",
        products=product_list,
        customers=customer_list
    )

@sales_bp.route("/view/<int:id>")
@login_required
def view_sale(id):
    """Ver detalles de una venta"""
    sale = Sale.query.get_or_404(id)
    
    # si no es admin, solo puede ver sus propias ventas
    if session.get("user_role") != "admin" and sale.user_id != session.get("user_id"):
        flash("No tienes permiso para ver esta venta", "danger")
        return redirect(url_for("sales.list_sales"))
    
    sale_items = SaleItem.query.filter_by(sale_id=id).all()
    return render_template("sales/view.html", sale=sale, sale_items=sale_items)


@sales_bp.route("/cancel/<int:id>", methods=["POST"])
@login_required
def cancel_sale(id):
    """Cancelar una venta y devolver stock"""
    sale = Sale.query.get_or_404(id)
    
    # solo admin o el vendedor puede cancelar
    if session.get("user_role") != "admin" and sale.user_id != session.get("user_id"):
        flash("No tienes permiso para cancelar esta venta", "danger")
        return redirect(url_for("sales.list_sales"))
    
    if sale.status == "cancelada":
        flash("Esta venta ya está cancelada", "warning")
        return redirect(url_for("sales.view_sale", id=id))
    
    try:
        # devolver stock
        for item in sale.items:
            product = Product.query.get(item.product_id)
            if product:
                product.stock += item.quantity
        
        # marcar como cancelada
        sale.status = "cancelada"
        db.session.commit()
        
        flash(f"Venta #{sale.id} cancelada. Stock restaurado.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al cancelar la venta: {str(e)}", "danger")
    
    return redirect(url_for("sales.view_sale", id=id))


@sales_bp.route("/api/search")
@login_required
def search_products_api():
    """API para buscar productos (para el formulario de ventas)"""
    query = request.args.get("q", "")
    products = Product.query.filter(
        Product.name.ilike(f"%{query}%"),
        Product.stock > 0
    ).limit(10).all()
    
    return jsonify([{
        "id": p.id,
        "name": p.name,
        "price": p.price,
        "stock": p.stock
    } for p in products])
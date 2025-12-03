from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.decorators import login_required
from app.models.product import Product
from app.models.variation import ProductVariation
from app.extensions import db

inventory_bp = Blueprint("inventory", __name__, url_prefix="/inventory")


@inventory_bp.route("/")
@login_required
def list_products():
    """Lista todos los productos del inventario"""
    search = request.args.get("search", "")
    
    if search:
        products = Product.query.filter(
            Product.name.ilike(f"%{search}%")
        ).all()
    else:
        products = Product.query.all()
    
    return render_template("inventory/list.html", products=products, search=search)


@inventory_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_product():
    """Agregar nuevo producto"""
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        stock = request.form.get("stock")
        supplier_id = request.form.get("supplier_id")
        
        # Validaciones
        if not name or not price:
            flash("El nombre y precio son obligatorios", "danger")
            return redirect(url_for("inventory.add_product"))
        
        try:
            new_product = Product(
                name=name,
                description=description,
                price=float(price),
                stock=int(stock) if stock else 0,
                supplier_id=int(supplier_id) if supplier_id else None
            )
            
            db.session.add(new_product)
            db.session.commit()
            
            flash(f"Producto '{name}' agregado exitosamente", "success")
            return redirect(url_for("inventory.list_products"))
        
        except Exception as e:
            db.session.rollback()
            flash(f"Error al agregar producto: {str(e)}", "danger")
            return redirect(url_for("inventory.add_product"))
    
    return render_template("inventory/add.html")


@inventory_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_product(id):
    """Editar un producto existente"""
    product = Product.query.get_or_404(id)
    
    if request.method == "POST":
        product.name = request.form.get("name")
        product.description = request.form.get("description")
        product.price = float(request.form.get("price"))
        product.stock = int(request.form.get("stock", 0))
        supplier_id = request.form.get("supplier_id")
        product.supplier_id = int(supplier_id) if supplier_id else None
        
        try:
            db.session.commit()
            flash(f"Producto '{product.name}' actualizado exitosamente", "success")
            return redirect(url_for("inventory.list_products"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar producto: {str(e)}", "danger")
    
    return render_template("inventory/edit.html", product=product)


@inventory_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_product(id):
    """Eliminar un producto"""
    product = Product.query.get_or_404(id)
    
    try:
        db.session.delete(product)
        db.session.commit()
        flash(f"Producto '{product.name}' eliminado exitosamente", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar producto: {str(e)}", "danger")
    
    return redirect(url_for("inventory.list_products"))


@inventory_bp.route("/view/<int:id>")
@login_required
def view_product(id):
    """Ver detalles de un producto"""
    product = Product.query.get_or_404(id)
    variations = ProductVariation.query.filter_by(product_id=id).all()
    return render_template("inventory/view.html", product=product, variations=variations)
from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from products.models import Product
from products.schemas import ProductSchema,RemoveSchema,UpdateSchema,PaginationSchema

product_bp = Blueprint("products", __name__)


@product_bp.route("/create", methods=["POST"])
async def create():
    data = request.json
    try:
        product = ProductSchema(**data)
        try:
            await Product.create(**product.model_dump())
            return jsonify({"message": "Product created successfully"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400


@product_bp.route("/remove", methods=["POST"])
async def remove_product():
    data = request.json

    try:
        remove_s=RemoveSchema(**data)

        try:
            product = await Product.get(id=int(remove_s.product_id))
        except:
            return jsonify({"error": "Bunday product topilmadi"}), 404

        if str(product.owner_id) != remove_s.owner_id:
            return jsonify({"error": "Siz bu product egasi emassiz!"}), 403

        await product.delete()
        return jsonify({"message": "Product muvaffaqiyatli o'chirildi"}), 200
    
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

@product_bp.route("/update", methods=["POST"])
async def update_product():
    try:
        data = request.json


        update = UpdateSchema(**data)

        try:
            product = await Product.get(id=update.id)
        except:
            return jsonify({"error": "Mahsulot topilmadi"}), 404

        if str(product.owner_id) != str(update.owner_id):
            return jsonify({"error": "Siz bu product egasi emassiz!"}), 403

        if update.name:
            product.name = update.name
        if update.description:
            product.description = update.description
        if update.price is not None:
            try:
                product.price = float(update.price)
            except:
                return jsonify({"error": "Narx raqam bo‘lishi kerak"}), 400

        await product.save()
        return jsonify({"message": "Mahsulot muvaffaqiyatli yangilandi"}), 200

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400


@product_bp.route("/products", methods=["POST"])
async def get_products_paginated():
    data = request.get_json()  

    try:
        pagination = PaginationSchema(**data)  
        offset = (pagination.page - 1) * pagination.per_page

        total = await Product.all().count()
        products = await Product.all().offset(offset).limit(pagination.per_page)

        results = []
        for product in products:
            results.append({
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price
            })

        return jsonify({
            "total": total,
            "page": pagination.page,
            "per_page": pagination.per_page,
            "products": results
        })
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

from flask import Blueprint, request, jsonify
from users.models import User
from core.utils import hash_password
from core.schemas import UserCreate, UserLogin, UserGetRequest
import hashlib

user_bp = Blueprint("user", __name__)

@user_bp.route("/register", methods=["POST"])
async def register():
    data = request.form.to_dict()

    # ✅ Pydantic validatsiya
    try:
        validated_data = UserCreate(**data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    hashed_pw = hash_password(validated_data.password)

    try:
        await User.create(
            username=validated_data.username,
            email=validated_data.email,
            password=hashed_pw,
            is_superuser=validated_data.is_superuser
        )
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/login", methods=["POST"])
async def login():
    data = request.form.to_dict()

    # ✅ Pydantic validatsiya
    try:
        validated_data = UserLogin(**data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    try:
        user = await User.get(username=validated_data.username)
    except:
        return jsonify({"error": "Username noto'g'ri"}), 404

    input_hash = hashlib.sha256(validated_data.password.encode()).hexdigest()

    if user.password != input_hash:
        return jsonify({"error": "Parol noto'g'ri"}), 401

    return jsonify({
        "message": f"Xush kelibsiz, {user.username}! Sizning ma'lumotlaringiz: Username - {user.username}, Email - {user.email}, Tizimga kirgan vaqt - {user.created_at}"
    })

@user_bp.route("/get", methods=["POST"])
async def get_user():
    data = request.form.to_dict()

    # ✅ Pydantic validatsiya
    try:
        validated_data = UserGetRequest(**data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    current_user = await User.get(id=validated_data.current_user_id)

    if current_user.is_superuser:
        target_user = await User.get(id=validated_data.id)
        return jsonify({
            "id": target_user.id,
            "username": target_user.username,
            "email": target_user.email
        })
    else:
        return jsonify({"error": "Siz admin emassiz"}), 403

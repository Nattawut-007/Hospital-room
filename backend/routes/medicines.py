from flask import Blueprint, request, jsonify
from models import Medicine
from flask_jwt_extended import jwt_required

medicines = Blueprint('medicines', __name__)

# ✅ อ่านข้อมูลยา
@medicines.route('/medicines', methods=['GET'])
@jwt_required()
def get_medicines():
    all_meds = Medicine.objects()
    return jsonify([
        {
            "name": m.name,
            "brand": m.brand,
            "stock": m.stock
        }
        for m in all_meds
    ])

# ✅ เพิ่มยา
@medicines.route('/medicines', methods=['POST'])
@jwt_required()
def create_medicine():
    data = request.get_json()
    medicine = Medicine(**data).save()
    return jsonify({
        "name": medicine.name,
        "brand": medicine.brand,
        "stock": medicine.stock
    }), 201

# ✅ แก้ไขยา
@medicines.route('/medicines/<id>', methods=['PUT'])
@jwt_required()
def update_medicine(id):
    data = request.get_json()
    medicine = Medicine.objects(id=id).first()
    if not medicine:
        return jsonify({'error': 'Medicine not found'}), 404
    medicine.update(**data)
    return jsonify({'msg': 'Medicine updated'})

# ✅ ลบยา
@medicines.route('/medicines/<id>', methods=['DELETE'])
@jwt_required()
def delete_medicine(id):
    medicine = Medicine.objects(id=id).first()
    if not medicine:
        return jsonify({'error': 'Medicine not found'}), 404
    medicine.delete()
    return jsonify({'msg': 'Medicine deleted'})

# ✅ ค้นหายาด้วยชื่อหรือยี่ห้อ
@medicines.route('/medicines/search', methods=['GET'])
@jwt_required()
def search_medicines():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Query parameter "q" is required'}), 400
    results = Medicine.objects.filter(
        __raw__={
            "$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"brand": {"$regex": query, "$options": "i"}}
            ]
        }
    )
    return jsonify([
        {
            "name": m.name,
            "brand": m.brand,
            "stock": m.stock
        }
        for m in results
    ])

#
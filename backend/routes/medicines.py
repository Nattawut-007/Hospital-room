from flask import Blueprint, request, jsonify
from models import Medicine
from mongoengine import ValidationError
from flask_jwt_extended import jwt_required

medicines = Blueprint('medicines', __name__)

def med_to_dict(m: Medicine):
    return {
        "_id": str(m.id),
        "name": m.name,
        "brand": m.brand,
        "stock": m.stock
    }

# ✅ อ่านข้อมูลยา (list)
@medicines.route('/medicines', methods=['GET'])
@jwt_required()
def get_medicines():
    all_meds = Medicine.objects()
    return jsonify([med_to_dict(m) for m in all_meds])

# ✅ เพิ่มยา (create)
@medicines.route('/medicines', methods=['POST'])
@jwt_required()
def create_medicine():
    try:
        data = request.get_json() or {}
        allowed = {k: data[k] for k in ('name', 'brand', 'stock') if k in data}
        medicine = Medicine(**allowed).save()
        return jsonify(med_to_dict(medicine)), 201
    except ValidationError as ve:
        return jsonify({"error": ve.to_dict()}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ แก้ไขยา (update)
@medicines.route('/medicines/<id>', methods=['PUT'])
@jwt_required()
def update_medicine(id):
    data = request.get_json() or {}
    medicine = Medicine.objects(id=id).first()
    if not medicine:
        return jsonify({'error': 'Medicine not found'}), 404

    # อัปเดตแบบปลอดภัยเฉพาะฟิลด์ที่อนุญาต
    for field in ('name', 'brand', 'stock'):
        if field in data:
            setattr(medicine, field, data[field])
    medicine.save()

    return jsonify(med_to_dict(medicine)), 200

# ✅ ลบยา (delete)
@medicines.route('/medicines/<id>', methods=['DELETE'])
@jwt_required()
def delete_medicine(id):
    medicine = Medicine.objects(id=id).first()
    if not medicine:
        return jsonify({'error': 'Medicine not found'}), 404
    medicine.delete()
    return jsonify({'msg': 'Medicine deleted', '_id': id}), 200

# ✅ ค้นหายาด้วยชื่อหรือยี่ห้อ (search)
@medicines.route('/medicines/search', methods=['GET'])
@jwt_required()
def search_medicines():
    query = request.args.get('q', '').strip()
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
    return jsonify([med_to_dict(m) for m in results])

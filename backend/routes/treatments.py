from flask import Blueprint, request, jsonify
from models import Treatment, Student, Medicine
from flask_jwt_extended import jwt_required
from datetime import datetime
from bson import ObjectId # เพิ่มบรรทัดนี้

treatments = Blueprint('treatments', __name__)

def treatment_to_dict(t: Treatment):
    """
    แปลง object Treatment ให้เป็น dictionary เพื่อใช้ในการส่งคืนเป็น JSON
    """
    return {
        '_id': str(t.id),
        'student': {
            'id': str(t.student.id),
            'name': t.student.name,
            'student_id': t.student.student_id
        } if t.student else None,
        'symptoms': t.symptoms,
        'medicines': [
            {'id': str(m.id), 'name': m.name} for m in t.medicines if m is not None
        ],
        'date': t.date.isoformat() if t.date else None
    }

# ✅ ค้นหาการรักษาและนักเรียนที่ได้รับการรักษา (list)
@treatments.route('/treatments', methods=['GET'])
@jwt_required()
def get_treatments():
    all_treatments = Treatment.objects()
    return jsonify([treatment_to_dict(t) for t in all_treatments])

# ✅ สร้างการรักษาใหม่ (create)
@treatments.route('/treatments', methods=['POST'])
@jwt_required()
def create_treatment():
    data = request.get_json() or {}
    student = Student.objects(student_id=data.get('student_id')).first()
    if not student:
        return jsonify({'error': 'Student not found'}), 400

    medicine_ids = data.get('medicine_ids', [])
    medicine_objs = []
    for mid in medicine_ids:
        med = Medicine.objects(id=mid).first()
        if not med:
            return jsonify({'error': f'Medicine with id {mid} not found'}), 400
        medicine_objs.append(med)

    treatment = Treatment(
        student=student,
        symptoms=data.get('symptoms', ''),
        medicines=medicine_objs,
        date=datetime.utcnow()
    ).save()
    
    return jsonify(treatment_to_dict(treatment)), 201

# ✅ ค้นหาจากนักเรียนที่ได้รับการรักษา (distinct list)
@treatments.route('/treated_students', methods=['GET'])
@jwt_required()
def get_treated_students():
    treated_students = Treatment.objects().distinct('student')
    students = []
    for student in treated_students:
        students.append({
            'id': str(student.id),
            'name': student.name,
            'student_id': student.student_id
        })
    return jsonify(students), 200

# ✅ ค้นหาประวัติการรักษาของนักเรียนเฉพาะเจาะจง (history)
@treatments.route('/treatment_history/<student_id>', methods=['GET'])
@jwt_required()
def treatment_history(student_id):
    student = Student.objects(student_id=student_id).first()
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    treatments_qs = Treatment.objects(student=student)
    history = []
    for t in treatments_qs:
        history.append({
            'id': str(t.id),
            'symptoms': t.symptoms,
            'medicines': [
                {'id': str(m.id), 'name': m.name} for m in t.medicines if m is not None
            ],
            'date': t.date.isoformat() if t.date else None
        })
    return jsonify({
        'student': {
            'id': str(student.id),
            'name': student.name,
            'student_id': student.student_id
        },
        'treatment_count': treatments_qs.count(),
        'history': history
    }), 200

# ✅ แก้ไขข้อมูลการรักษาตาม id (update)
@treatments.route('/treatments/<id>', methods=['PUT'])
@jwt_required()
def update_treatment(id):
    data = request.get_json() or {}

    # ตรวจสอบ ID ของ Treatment
    if not ObjectId.is_valid(id):
        return jsonify({'error': 'Invalid treatment ID format'}), 400

    treatment = Treatment.objects(id=ObjectId(id)).first()
    if not treatment:
        return jsonify({'error': 'Treatment not found'}), 404

    if 'student_id' in data:
        student = Student.objects(student_id=data['student_id']).first()
        if not student:
            return jsonify({'error': 'Student not found'}), 400
        treatment.student = student

    if 'symptoms' in data:
        treatment.symptoms = data['symptoms']

    if 'medicine_ids' in data:
        medicine_objs = []
        for mid in data['medicine_ids']:
            # ตรวจสอบ ID ของยา
            if not ObjectId.is_valid(mid):
                return jsonify({'error': f'Invalid medicine ID format: {mid}'}), 400

            med = Medicine.objects(id=ObjectId(mid)).first()
            if not med:
                return jsonify({'error': f'Medicine with id {mid} not found'}), 400
            medicine_objs.append(med)
        treatment.medicines = medicine_objs

    if 'date' in data:
        try:
            treatment.date = datetime.fromisoformat(data['date'])
        except Exception:
            return jsonify({'error': 'Invalid date format'}), 400

    treatment.save()
    return jsonify(treatment_to_dict(treatment)), 200

# ✅ ลบการรักษาตาม id (delete)
@treatments.route('/treatments/<_id>', methods=['DELETE'])
@jwt_required()
def delete_treatment(id):
    treatment = Treatment.objects(id=id).first()
    if not treatment:
        return jsonify({'error': 'Treatment not found'}), 404
    treatment.delete()
    return jsonify({'msg': 'Treatment deleted', '_id': id}), 200
#
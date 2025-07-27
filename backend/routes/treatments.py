from flask import Blueprint, request, jsonify
from models import Treatment, Student, Medicine
from flask_jwt_extended import jwt_required
from datetime import datetime
from bson import ObjectId

treatments = Blueprint('treatments', __name__)
# ค้นหาการรักษาและนักเรียนที่ได้รับการรักษา
@treatments.route('/treatments', methods=['GET'])
@jwt_required()
def get_treatments():
    result = []
    for t in Treatment.objects():
        result.append({
            'id': str(t.id),
            'student': {
                'id': str(t.student.id),
                'name': t.student.name,
                'student_id': t.student.student_id
            },
            'symptoms': t.symptoms,
            'medicines': [
                {
                    'id': str(m.id),
                    'name': m.name
                } for m in t.medicines if m is not None
            ],
            'date': t.date.isoformat() if t.date else None
        })
    return jsonify(result)
# สร้างการรักษาใหม่
@treatments.route('/treatments', methods=['POST'])
@jwt_required()
def create_treatment():
    data = request.json
    # ค้นหานักเรียนจาก id
    student = Student.objects(student_id=data.get('student_id')).first()
    print(student)
    if not student:
        return jsonify({'error': 'Student not found'}), 400

    # ดึง medicine จาก id
    medicine_ids = data.get('medicine_ids', [])
    medicine_objs = []
    for mid in medicine_ids:
        med = Medicine.objects(id=mid).first()
        if not med:
            return jsonify({'error': f'Medicine with id {mid} not found'}), 400
        medicine_objs.append(med)

    # สร้างการรักษาใหม่
    treatment = Treatment(
        student=student,
        symptoms=data.get('symptoms', ''),
        medicines=medicine_objs,
        date=datetime.utcnow()
    ).save()

    return jsonify({'msg': 'Treatment recorded', 'treatment_id': str(treatment.id)})

# ค้นหาจากนักเรียนที่ได้รับการรักษา
@treatments.route('/treated_students', methods=['GET'])
@jwt_required()
def get_treated_students():
    # ดึง student id ที่มีใน Treatment อย่างน้อย 1 ครั้ง
    treated_students = Treatment.objects().distinct('student')
    students = []
    for student in treated_students:
        students.append({
            'id': str(student.id),
            'name': student.name,
            'student_id': student.student_id
        })
    return jsonify(students), 200

# ค้นหาประวัติการรักษาของนักเรียนเฉพาะเจาะจง
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
                {
                    'id': str(m.id),
                    'name': m.name
                } for m in t.medicines if m is not None
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

# แก้ไขข้อมูลการรักษาตาม id
@treatments.route('/treatments/<treatment_id>', methods=['PUT'])
@jwt_required()
def update_treatment(treatment_id):
    data = request.json
    treatment = Treatment.objects(id=treatment_id).first()
    if not treatment:
        return jsonify({'error': 'Treatment not found'}), 404

    # อัปเดต student ถ้ามีส่งมา
    student_id = data.get('student_id')
    if student_id:
        student = Student.objects(student_id=student_id).first()
        if not student:
            return jsonify({'error': 'Student not found'}), 400
        treatment.student = student

    # อัปเดต medicines ถ้ามีส่งมา
    medicine_ids = data.get('medicine_ids')
    if medicine_ids is not None:
        medicine_objs = []
        for mid in medicine_ids:
            med = Medicine.objects(id=mid).first()
            if not med:
                return jsonify({'error': f'Medicine with id {mid} not found'}), 400
            medicine_objs.append(med)
        treatment.medicines = medicine_objs

    # อัปเดต symptoms ถ้ามีส่งมา
    if 'symptoms' in data:
        treatment.symptoms = data['symptoms']

    # อัปเดตวันที่ ถ้ามีส่งมา
    if 'date' in data:
        try:
            treatment.date = datetime.fromisoformat(data['date'])
        except Exception:
            return jsonify({'error': 'Invalid date format'}), 400

    treatment.save()
    return jsonify({'msg': 'Treatment updated', 'treatment_id': str(treatment.id)}), 200

# ลบการรักษาตาม id
@treatments.route('/treatments/<treatment_id>', methods=['DELETE'])
@jwt_required()
def delete_treatment(treatment_id):
    treatment = Treatment.objects(id=treatment_id).first()
    if not treatment:
        return jsonify({'error': 'Treatment not found'}), 404
    treatment.delete()
    return jsonify({'msg': 'Treatment deleted'}), 200
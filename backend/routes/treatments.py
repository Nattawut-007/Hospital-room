from flask import Blueprint, request, jsonify
from models import Treatment, Student, Medicine
from flask_jwt_extended import jwt_required
from datetime import datetime

treatments = Blueprint('treatments', __name__)

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

@treatments.route('/treatments', methods=['POST'])
@jwt_required()
def create_treatment():
    data = request.json

    # ค้นหานักเรียนจาก id
    student = Student.objects(id=data.get('student_id')).first()
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
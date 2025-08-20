from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Student

students = Blueprint('students', __name__)

def student_to_dict(s: Student):
    return {
        "_id": str(s.id),
        "student_id": s.student_id,
        "name": s.name,
        "age": s.age,
        "department": s.department,
        "grade_level": s.grade_level
    }

# ✅ ดึงนักเรียนทั้งหมด
@students.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    all_students = Student.objects().order_by('student_id')
    return jsonify([student_to_dict(s) for s in all_students])

# ✅ เพิ่มนักเรียน
@students.route('/students', methods=['POST'])
@jwt_required()
def create_student():
    data = request.get_json() or {}
    # ป้องกัน field แปลก ๆ หลุดเข้าโมเดล
    allowed = {k: data[k] for k in ('student_id', 'name', 'age', 'department', 'grade_level') if k in data}
    student = Student(**allowed).save()
    return jsonify(student_to_dict(student)), 201

# ✅ แก้ไขนักเรียน
@students.route('/students/<id>', methods=['PUT'])
@jwt_required()
def update_student(id):
    data = request.get_json() or {}
    student = Student.objects(id=id).first()
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    # อัปเดตแบบปลอดภัยเฉพาะฟิลด์ที่อนุญาต
    for field in ('student_id', 'name', 'age', 'department', 'grade_level'):
        if field in data:
            setattr(student, field, data[field])
    student.save()

    return jsonify(student_to_dict(student)), 200

# ✅ ลบนักเรียน
@students.route('/students/<id>', methods=['DELETE'])
@jwt_required()
def delete_student(id):
    student = Student.objects(id=id).first()
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    student.delete()
    return jsonify({'msg': 'Student deleted', '_id': id}), 200
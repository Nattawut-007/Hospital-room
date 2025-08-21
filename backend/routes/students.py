# routes/students.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Student

students = Blueprint('students', __name__)

# ✅ ดึงนักเรียนทั้งหมด
@students.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    all_students = Student.objects().order_by('student_id')
    return jsonify([{
        "id": str(s.id),
        "student_id": s.student_id,
        "name": s.name,
        "age": s.age,
        "department": s.department,
        "grade_level": s.Grade_level
    } for s in all_students])

# ✅ เพิ่มนักเรียน
@students.route('/students', methods=['POST'])
@jwt_required()
def create_student():
    data = request.get_json()
    student = Student(
        student_id=data['student_id'],
        name=data['name'],
        age=data.get('age'),
        department=data.get('department'),
        Grade_level=data.get('grade_level')
    )
    student.save()
    return jsonify({"msg": "Student created!"})

# ✅ แก้ไขนักเรียน
@students.route('/students/<student_id>', methods=['PUT'])
@jwt_required()
def update_student(student_id):
    data = request.get_json()
    Student.objects(id=student_id).update_one(
        student_id=data.get('student_id'),
        name=data.get('name'),
        age=data.get('age'),
        department=data.get('department'),
        Grade_level=data.get('grade_level')
    )
    return jsonify({"msg": "Student updated!"})

# ✅ ลบนักเรียน
@students.route('/students/<student_id>', methods=['DELETE'])
@jwt_required()
def delete_student(student_id):
    Student.objects(id=student_id).delete()
    return jsonify({"msg": "Student deleted!"})
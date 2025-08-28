# routes/students.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from mongoengine import ValidationError
from models import Student
import re

students = Blueprint('students', __name__)

def parse_grade_level(grade_input):
    """
    Parse grade level input to extract integer value.
    Handles inputs like: "Year 3", "Grade 10", "3", 3
    Returns integer or None if cannot parse
    """
    if grade_input is None:
        return None
    
    # If already an integer, return it
    if isinstance(grade_input, int):
        return grade_input
    
    # If it's a string, try to extract number
    if isinstance(grade_input, str):
        # Try direct conversion first
        if grade_input.isdigit():
            return int(grade_input)
        
        # Extract number from strings like "Year 3" or "Grade 10"
        match = re.search(r'\d+', grade_input)
        if match:
            return int(match.group())
    
    return None

# ✅ ดึงนักเรียนทั้งหมด
@students.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    try:
        all_students = Student.objects().order_by('student_id')
        return jsonify([{
            "id": str(s.id),
            "student_id": s.student_id,
            "name": s.name,
            "age": s.age,
            "department": s.department,
            "grade_level": s.Grade_level  # Note: Capital G to match your model
        } for s in all_students])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ เพิ่มนักเรียน
@students.route('/students', methods=['POST'])
@jwt_required()
def create_student():
    try:
        data = request.get_json()
        
        if not data or 'student_id' not in data or 'name' not in data:
            return jsonify({"error": "student_id and name are required"}), 400
        
        grade_level = parse_grade_level(data.get('grade_level'))
        
        student = Student(
            student_id=data['student_id'],
            name=data['name'],
            age=data.get('age'),
            department=data.get('department'),
            Grade_level=grade_level
        )
        student.save()
        
        return jsonify({
            "msg": "Student created!",
            "student": {
                "id": str(student.id),
                "student_id": student.student_id,
                "name": student.name,
                "age": student.age,
                "department": student.department,
                "grade_level": student.Grade_level
            }
        }), 201
    
    except ValidationError as ve:
        # ส่ง 400 หากข้อมูลไม่ถูกต้องตาม model
        return jsonify({"error": ve.to_dict()}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ ดึงนักเรียนคนเดียว
@students.route('/students/<student_id>', methods=['GET'])
@jwt_required()
def get_student(student_id):
    try:
        student = Student.objects(id=student_id).first()
        if not student:
            return jsonify({"error": "Student not found"}), 404
        
        return jsonify({
            "id": str(student.id),
            "student_id": student.student_id,
            "name": student.name,
            "age": student.age,
            "department": student.department,
            "grade_level": student.Grade_level  # Note: Capital G to match your model
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ แก้ไขนักเรียน
@students.route('/students/<student_id>', methods=['PUT'])
@jwt_required()
def update_student(student_id):
    try:
        data = request.get_json()
        
        # Find student first
        student = Student.objects(id=student_id).first()
        if not student:
            return jsonify({"error": "Student not found"}), 404
        
        # Parse grade level if provided
        grade_level = parse_grade_level(data.get('grade_level')) if 'grade_level' in data else student.Grade_level
        
        # Prepare update data
        update_data = {}
        if 'student_id' in data:
            update_data['student_id'] = data['student_id']
        if 'name' in data:
            update_data['name'] = data['name']
        if 'age' in data:
            update_data['age'] = data['age']
        if 'department' in data:
            update_data['department'] = data['department']
        if 'grade_level' in data:
            update_data['Grade_level'] = grade_level  # Note: Capital G to match your model
        
        # Update student
        Student.objects(id=student_id).update_one(**update_data)
        
        # Return updated student
        updated_student = Student.objects(id=student_id).first()
        return jsonify({
            "msg": "Student updated!",
            "student": {
                "id": str(updated_student.id),
                "student_id": updated_student.student_id,
                "name": updated_student.name,
                "age": updated_student.age,
                "department": updated_student.department,
                "grade_level": updated_student.Grade_level  # Note: Capital G to match your model
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ ลบนักเรียน
@students.route('/students/<student_id>', methods=['DELETE'])
@jwt_required()
def delete_student(student_id):
    try:
        student = Student.objects(id=student_id).first()
        if not student:
            return jsonify({"error": "Student not found"}), 404
        
        Student.objects(id=student_id).delete()
        return jsonify({"msg": "Student deleted!"})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
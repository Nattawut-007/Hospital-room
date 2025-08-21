from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Student

students = Blueprint('students', __name__)

def student_to_dict(s: Student):
    """
    Converts a Student object to a dictionary with correct key names for the frontend.
    """
    return {
        "_id": str(s.id),
        "studentId": s.student_id,
        "name": s.name,
        "age": s.age,
        "major": s.major,
        "year": s.year
    }

# --- API Endpoints ---

# ✅ ดึงนักเรียนทั้งหมด
@students.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    """Fetches all students from the database."""
    all_students = Student.objects().order_by('student_id')
    return jsonify([student_to_dict(s) for s in all_students])

# ✅ เพิ่มนักเรียน
@students.route('/students', methods=['POST'])
@jwt_required()
def create_student():
    """Adds a new student to the database."""
    data = request.get_json() or {}
    try:
        # Check for required fields and handle potential duplicates
        if not all(k in data for k in ['studentId', 'name', 'age', 'major', 'year']):
            return jsonify({'error': 'Missing required fields'}), 400

        if Student.objects(student_id=data.get('studentId')).first():
            return jsonify({'error': 'Student with this ID already exists'}), 409
        
        student = Student(
            student_id=data['studentId'],
            name=data['name'],
            age=data['age'],
            major=data['major'],
            year=data['year']
        ).save()
        
        return jsonify(student_to_dict(student)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ✅ แก้ไขนักเรียน
@students.route('/students/<id>', methods=['PUT'])
@jwt_required()
def update_student(id):
    """Updates an existing student's information."""
    data = request.get_json() or {}
    student = Student.objects(id=id).first()
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    try:
        student.update(**data)
        updated_student = Student.objects(id=id).first()
        return jsonify(student_to_dict(updated_student)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ✅ ลบนักเรียน
@students.route('/students/<id>', methods=['DELETE'])
@jwt_required()
def delete_student(id):
    """Deletes a student from the database."""
    student = Student.objects(id=id).first()
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    student.delete()
    return jsonify({'msg': 'Student deleted', '_id': id}), 200
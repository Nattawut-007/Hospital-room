#!/usr/bin/env python3
"""
Hospital Room API Tests using pytest
ทดสอบการเชื่อมต่อ MongoDB และ API endpoints ด้วย pytest framework
"""

import os
import pytest
import requests
import pymongo
from datetime import datetime
from dotenv import load_dotenv

# โหลด environment variables
load_dotenv()


class TestConfig:
    """Configuration for tests"""
    BASE_URL = "http://127.0.0.1:5000/api"
    TEST_USER = {
        "username": "pytest_user",
        "password": "pytest_password123"
    }
    TEST_STUDENT = {
        "student_id": "PYTEST001",
        "name": "Pytest Test Student",
        "age": 21,
        "department": "Software Engineering",
        "grade_level": "Year 3"
    }
    TEST_MEDICINE = {
        "name": "Pytest Medicine",
        "brand": "Pytest Brand",
        "stock": 50
    }


@pytest.fixture(scope="session")
def mongodb_client():
    """MongoDB connection fixture"""
    # อ่านค่า config จาก environment
    mongo_user = os.getenv('MONGO_USER')
    mongo_pass = os.getenv('MONGO_PASS')
    mongo_host = os.getenv('MONGO_HOST', 'localhost')
    mongo_port = os.getenv('MONGO_PORT', '27017')
    mongo_db = os.getenv('MONGO_DB', 'hospital_room')
    mongo_auth_db = os.getenv('MONGO_AUTH_DB', 'admin')
    
    # สร้าง connection string
    if mongo_user and mongo_pass:
        uri = f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}/{mongo_db}?authSource={mongo_auth_db}"
    else:
        uri = f"mongodb://{mongo_host}:{mongo_port}/{mongo_db}"
    
    try:
        client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        yield client
    finally:
        client.close()


@pytest.fixture(scope="session")
def api_session():
    """HTTP session fixture"""
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    yield session
    session.close()


@pytest.fixture(scope="session")
def authenticated_session(api_session):
    """Authenticated session with JWT token"""
    # สมัครสมาชิก (อาจจะ fail ถ้ามี user อยู่แล้ว - ไม่เป็นไร)
    try:
        api_session.post(f"{TestConfig.BASE_URL}/register", json=TestConfig.TEST_USER)
    except:
        pass
    
    # เข้าสู่ระบบ
    response = api_session.post(f"{TestConfig.BASE_URL}/login", json=TestConfig.TEST_USER)
    assert response.status_code == 200, f"Login failed: {response.text}"
    
    token = response.json().get('access_token')
    assert token, "No access token received"
    
    api_session.headers.update({"Authorization": f"Bearer {token}"})
    return api_session


@pytest.fixture
def sample_student_id(authenticated_session):
    """Create a sample student and return its ID"""
    response = authenticated_session.post(f"{TestConfig.BASE_URL}/students", json=TestConfig.TEST_STUDENT)
    if response.status_code in [200, 201]:
        return TestConfig.TEST_STUDENT['student_id']
    
    # ถ้าสร้างไม่ได้ ให้ดึง student ที่มีอยู่แล้ว
    response = authenticated_session.get(f"{TestConfig.BASE_URL}/students")
    if response.status_code == 200:
        students = response.json()
        if students:
            return students[0]['student_id']
    
    pytest.skip("Cannot create or find any student for testing")


@pytest.fixture
def sample_medicine_id(authenticated_session):
    """Create a sample medicine and return its ID"""
    response = authenticated_session.post(f"{TestConfig.BASE_URL}/medicines", json=TestConfig.TEST_MEDICINE)
    if response.status_code in [200, 201]:
        return response.json()['_id']
    
    # ถ้าสร้างไม่ได้ ให้ดึง medicine ที่มีอยู่แล้ว
    response = authenticated_session.get(f"{TestConfig.BASE_URL}/medicines")
    if response.status_code == 200:
        medicines = response.json()
        if medicines:
            return medicines[0]['_id']
    
    pytest.skip("Cannot create or find any medicine for testing")


class TestMongoDB:
    """Test MongoDB connection and basic operations"""
    
    def test_mongodb_connection(self, mongodb_client):
        """ทดสอบการเชื่อมต่อ MongoDB"""
        # ทดสอบ ping
        result = mongodb_client.admin.command('ping')
        assert result['ok'] == 1.0
        
        # ตรวจสอบ database
        mongo_db = os.getenv('MONGO_DB', 'hospital_room')
        db = mongodb_client[mongo_db]
        collections = db.list_collection_names()
        
        print(f"\n📊 Database: {mongo_db}")
        print(f"📁 Collections: {collections}")
        
        # แสดงจำนวนเอกสารในแต่ละ collection
        for collection in collections:
            count = db[collection].count_documents({})
            print(f"   - {collection}: {count} documents")
    
    def test_database_collections(self, mongodb_client):
        """ทดสอบ collections ที่จำเป็น"""
        mongo_db = os.getenv('MONGO_DB', 'hospital_room')
        db = mongodb_client[mongo_db]
        
        expected_collections = ['user']  # collection พื้นฐานที่ต้องมี
        for collection in expected_collections:
            # ทดสอบการเข้าถึง collection
            count = db[collection].count_documents({})
            print(f"   ✓ {collection}: {count} documents")


class TestAuthentication:
    """Test user authentication endpoints"""
    
    def test_user_registration(self, api_session):
        """ทดสอบการสมัครสมาชิก"""
        test_user = {
            "username": f"test_reg_{datetime.now().microsecond}",
            "password": "test123456"
        }
        
        response = api_session.post(f"{TestConfig.BASE_URL}/register", json=test_user)
        assert response.status_code in [200, 400], f"Registration failed: {response.text}"
        
        if response.status_code == 200:
            assert 'msg' in response.json()
            print(f"✅ Registration: {response.json()['msg']}")
        else:
            # 400 หมายถึง user มีอยู่แล้ว
            assert 'already exists' in response.json().get('msg', '').lower()
            print("✅ Registration: User already exists (expected)")
    
    def test_user_login(self, api_session):
        """ทดสอบการเข้าสู่ระบบ"""
        # สมัครสมาชิกก่อน
        api_session.post(f"{TestConfig.BASE_URL}/register", json=TestConfig.TEST_USER)
        
        # ทดสอบ login
        response = api_session.post(f"{TestConfig.BASE_URL}/login", json=TestConfig.TEST_USER)
        assert response.status_code == 200, f"Login failed: {response.text}"
        
        data = response.json()
        assert 'access_token' in data
        assert len(data['access_token']) > 50  # JWT token should be long
        print(f"✅ Login successful, token length: {len(data['access_token'])}")
    
    def test_invalid_login(self, api_session):
        """ทดสอบการเข้าสู่ระบบด้วยข้อมูลผิด"""
        invalid_user = {
            "username": "nonexistent_user",
            "password": "wrong_password"
        }
        
        response = api_session.post(f"{TestConfig.BASE_URL}/login", json=invalid_user)
        assert response.status_code == 401
        assert 'Invalid credentials' in response.json().get('msg', '')
    
    def test_get_users(self, api_session):
        """ทดสอบการดึงรายชื่อ users"""
        response = api_session.get(f"{TestConfig.BASE_URL}/get_user")
        assert response.status_code == 200
        
        users = response.json()
        assert isinstance(users, list)
        print(f"✅ Found {len(users)} users in system")


class TestStudentsAPI:
    """Test Students API endpoints"""
    
    def test_create_student(self, authenticated_session):
        """ทดสอบการเพิ่มนักเรียน"""
        student_data = {
            **TestConfig.TEST_STUDENT,
            "student_id": f"CREATE_{datetime.now().microsecond}"
        }
        
        response = authenticated_session.post(f"{TestConfig.BASE_URL}/students", json=student_data)
        assert response.status_code in [200, 201], f"Create student failed: {response.text}"
        
        result = response.json()
        assert 'msg' in result
        print(f"✅ Student created: {student_data['name']}")
    
    def test_get_all_students(self, authenticated_session):
        """ทดสอบการดึงข้อมูลนักเรียนทั้งหมด"""
        response = authenticated_session.get(f"{TestConfig.BASE_URL}/students")
        assert response.status_code == 200, f"Get students failed: {response.text}"
        
        students = response.json()
        assert isinstance(students, list)
        print(f"✅ Found {len(students)} students")
        
        if students:
            student = students[0]
            required_fields = ['id', 'student_id', 'name', 'age', 'department', 'grade_level']
            for field in required_fields:
                assert field in student, f"Missing field: {field}"
    
    def test_update_student(self, authenticated_session, sample_student_id):
        """ทดสอบการแก้ไขข้อมูลนักเรียน"""
        # ดึงข้อมูล student ก่อน
        response = authenticated_session.get(f"{TestConfig.BASE_URL}/students")
        assert response.status_code == 200
        
        students = response.json()
        if not students:
            pytest.skip("No students found for update test")
        
        student_obj_id = students[0]['id']
        update_data = {
            "name": "Updated Name",
            "age": 25,
            "department": "Updated Department"
        }
        
        response = authenticated_session.put(
            f"{TestConfig.BASE_URL}/students/{student_obj_id}", 
            json=update_data
        )
        assert response.status_code == 200, f"Update student failed: {response.text}"
        print("✅ Student updated successfully")
    
    def test_delete_student(self, authenticated_session):
        """ทดสอบการลบนักเรียน"""
        # สร้าง student สำหรับลบ
        student_data = {
            **TestConfig.TEST_STUDENT,
            "student_id": f"DELETE_{datetime.now().microsecond}"
        }
        
        create_response = authenticated_session.post(f"{TestConfig.BASE_URL}/students", json=student_data)
        if create_response.status_code not in [200, 201]:
            pytest.skip("Cannot create student for delete test")
        
        # ดึง ID ของ student ที่สร้าง
        get_response = authenticated_session.get(f"{TestConfig.BASE_URL}/students")
        students = get_response.json()
        
        target_student = next((s for s in students if s['student_id'] == student_data['student_id']), None)
        if not target_student:
            pytest.skip("Cannot find created student for delete test")
        
        # ลบ student
        response = authenticated_session.delete(f"{TestConfig.BASE_URL}/students/{target_student['id']}")
        assert response.status_code == 200, f"Delete student failed: {response.text}"
        print("✅ Student deleted successfully")


class TestMedicinesAPI:
    """Test Medicines API endpoints"""
    
    def test_create_medicine(self, authenticated_session):
        """ทดสอบการเพิ่มยา"""
        medicine_data = {
            **TestConfig.TEST_MEDICINE,
            "name": f"Test Medicine {datetime.now().microsecond}"
        }
        
        response = authenticated_session.post(f"{TestConfig.BASE_URL}/medicines", json=medicine_data)
        assert response.status_code in [200, 201], f"Create medicine failed: {response.text}"
        
        result = response.json()
        assert '_id' in result
        assert result['name'] == medicine_data['name']
        print(f"✅ Medicine created: {result['name']}")
    
    def test_get_all_medicines(self, authenticated_session):
        """ทดสอบการดึงข้อมูลยาทั้งหมด"""
        response = authenticated_session.get(f"{TestConfig.BASE_URL}/medicines")
        assert response.status_code == 200, f"Get medicines failed: {response.text}"
        
        medicines = response.json()
        assert isinstance(medicines, list)
        print(f"✅ Found {len(medicines)} medicines")
        
        if medicines:
            medicine = medicines[0]
            required_fields = ['_id', 'name', 'brand', 'stock']
            for field in required_fields:
                assert field in medicine, f"Missing field: {field}"
    
    def test_search_medicines(self, authenticated_session, sample_medicine_id):
        """ทดสอบการค้นหายา"""
        # ค้นหาด้วยคำว่า "Test"
        response = authenticated_session.get(f"{TestConfig.BASE_URL}/medicines/search?q=Test")
        assert response.status_code == 200, f"Search medicines failed: {response.text}"
        
        results = response.json()
        assert isinstance(results, list)
        print(f"✅ Search found {len(results)} medicines with 'Test'")
        
        # ทดสอบ search แบบไม่มี query
        response = authenticated_session.get(f"{TestConfig.BASE_URL}/medicines/search")
        assert response.status_code == 400
        assert 'required' in response.json().get('error', '').lower()
    
    def test_update_medicine(self, authenticated_session, sample_medicine_id):
        """ทดสอบการแก้ไขยา"""
        update_data = {
            "name": "Updated Medicine Name",
            "stock": 200
        }
        
        response = authenticated_session.put(
            f"{TestConfig.BASE_URL}/medicines/{sample_medicine_id}", 
            json=update_data
        )
        assert response.status_code == 200, f"Update medicine failed: {response.text}"
        
        result = response.json()
        assert result['name'] == update_data['name']
        assert result['stock'] == update_data['stock']
        print("✅ Medicine updated successfully")
    
    def test_delete_medicine(self, authenticated_session):
        """ทดสอบการลบยา"""
        # สร้าง medicine สำหรับลบ
        medicine_data = {
            **TestConfig.TEST_MEDICINE,
            "name": f"Delete Test {datetime.now().microsecond}"
        }
        
        create_response = authenticated_session.post(f"{TestConfig.BASE_URL}/medicines", json=medicine_data)
        if create_response.status_code not in [200, 201]:
            pytest.skip("Cannot create medicine for delete test")
        
        medicine_id = create_response.json()['_id']
        
        # ลบ medicine
        response = authenticated_session.delete(f"{TestConfig.BASE_URL}/medicines/{medicine_id}")
        assert response.status_code == 200, f"Delete medicine failed: {response.text}"
        
        result = response.json()
        assert result['_id'] == medicine_id
        print("✅ Medicine deleted successfully")


class TestTreatmentsAPI:
    """Test Treatments API endpoints"""
    
    def test_create_treatment(self, authenticated_session, sample_student_id, sample_medicine_id):
        """ทดสอบการสร้าง treatment"""
        treatment_data = {
            "student_id": sample_student_id,
            "symptoms": "Pytest test symptoms - fever, headache",
            "medicine_ids": [sample_medicine_id]
        }
        
        response = authenticated_session.post(f"{TestConfig.BASE_URL}/treatments", json=treatment_data)
        assert response.status_code in [200, 201], f"Create treatment failed: {response.text}"
        
        result = response.json()
        assert '_id' in result
        assert result['symptoms'] == treatment_data['symptoms']
        assert result['student']['id'] is not None
        print(f"✅ Treatment created: {result['_id']}")
    
    def test_get_all_treatments(self, authenticated_session):
        """ทดสอบการดึงข้อมูล treatments ทั้งหมด"""
        response = authenticated_session.get(f"{TestConfig.BASE_URL}/treatments")
        assert response.status_code == 200, f"Get treatments failed: {response.text}"
        
        treatments = response.json()
        assert isinstance(treatments, list)
        print(f"✅ Found {len(treatments)} treatments")
        
        if treatments:
            treatment = treatments[0]
            required_fields = ['_id', 'student', 'symptoms', 'medicines', 'date']
            for field in required_fields:
                assert field in treatment, f"Missing field: {field}"
    
    def test_get_treated_students(self, authenticated_session):
        """ทดสอบการดึงรายชื่อนักเรียนที่ได้รับการรักษา"""
        response = authenticated_session.get(f"{TestConfig.BASE_URL}/treated_students")
        assert response.status_code == 200, f"Get treated students failed: {response.text}"
        
        students = response.json()
        assert isinstance(students, list)
        print(f"✅ Found {len(students)} treated students")
    
    def test_treatment_history(self, authenticated_session, sample_student_id):
        """ทดสอบการดึงประวัติการรักษา"""
        response = authenticated_session.get(f"{TestConfig.BASE_URL}/treatment_history/{sample_student_id}")
        assert response.status_code == 200, f"Get treatment history failed: {response.text}"
        
        result = response.json()
        assert 'student' in result
        assert 'treatment_count' in result
        assert 'history' in result
        assert isinstance(result['history'], list)
        print(f"✅ Treatment history: {result['treatment_count']} treatments")


class TestAPIErrors:
    """Test API error handling"""
    
    def test_unauthorized_access(self):
        """ทดสอบการเข้าถึงโดยไม่มี token"""
        endpoints = [
            '/students',    # ไม่ต้องมี /api เพราะ BASE_URL มีแล้ว
            '/medicines',
            '/treatments'
        ]

        for endpoint in endpoints:
            response = requests.get(f"{TestConfig.BASE_URL}{endpoint}")
            print("Request headers:", response.request.headers)
            print("Response status:", response.status_code, "Body:", response.text)
            assert response.status_code == 401, f"Should require auth: {endpoint}"
    
    def test_nonexistent_resources(self, authenticated_session):
        """ทดสอบการเข้าถึง resource ที่ไม่มีอยู่"""
        # ทดสอบ treatment history ที่ไม่มี
        response = authenticated_session.get(f"{TestConfig.BASE_URL}/treatment_history/NONEXISTENT")
        assert response.status_code == 404
        
        # ทดสอบ medicine ที่ไม่มี - ใช้ ObjectId ที่ไม่มีจริง
        fake_id = "507f1f77bcf86cd799439011"
        response = authenticated_session.put(f"{TestConfig.BASE_URL}/medicines/{fake_id}", json={
            "name": "Test Medicine",
            "price": 100
        })
        assert response.status_code == 404
    
    def test_invalid_data(self, authenticated_session):
        """ทดสอบการส่งข้อมูลผิดรูปแบบ"""
        # ทดสอบสร้าง student โดยไม่มี required fields
        invalid_student = {
            "age": 20
            # ขาด name และ student_id ที่จำเป็น
        }
        response = authenticated_session.post(f"{TestConfig.BASE_URL}/students", json=invalid_student)
        assert response.status_code == 400
        
        # ทดสอบสร้าง treatment โดยไม่มี student
        invalid_treatment = {
            "student_id": "NONEXISTENT_STUDENT_ID",
            "symptoms": "Test symptoms",
            "diagnosis": "Test diagnosis"
        }
        response = authenticated_session.post(f"{TestConfig.BASE_URL}/treatments", json=invalid_treatment)
        assert response.status_code in [400, 404]  # อาจจะได้ 400 หรือ 404
        
        # ทดสอบสร้าง medicine โดยไม่มี required fields
        invalid_medicine = {
            "description": "Test description"
            # ขาด name ที่จำเป็น
        }
        response = authenticated_session.post(f"{TestConfig.BASE_URL}/medicines", json=invalid_medicine)
        assert response.status_code == 400


if __name__ == "__main__":
    """รัน tests ด้วย pytest"""
    import sys
    
    print("🧪 Running Hospital API Tests with pytest")
    print("=" * 60)
    
    # ตรวจสอบ environment variables
    required_vars = ['SECRET_KEY', 'JWT_SECRET_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"⚠️  Warning: Missing environment variables: {missing_vars}")
        print("   Please check your .env file")
        print()
    
    # รัน pytest
    pytest_args = [
        __file__,
        "-v",           # verbose output
        "-s",           # don't capture output
        "--tb=short",   # short traceback format
        "--color=yes",  # colored output
        "-x",           # stop on first failure
    ]
    
    # เพิ่ม arguments จาก command line
    if len(sys.argv) > 1:
        pytest_args.extend(sys.argv[1:])
    
    exit_code = pytest.main(pytest_args)
    sys.exit(exit_code)
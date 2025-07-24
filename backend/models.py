from mongoengine import Document, StringField, ReferenceField, DateTimeField, IntField, ListField
from datetime import datetime

# ผู้ดูแลระบบ (แอดมิน)
class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)

# นักเรียน
class Student(Document):
    student_id = StringField(required=True, unique=True)
    name = StringField(required=True)
    age = IntField()
    department = StringField()
    Grade_level = IntField()

# ยา
class Medicine(Document):
    name = StringField(required=True)
    brand = StringField()
    stock = IntField(default=0)

# ใบรับการรักษา
class Treatment(Document):
    student = ReferenceField(Student, required=True)
    symptoms = StringField()
    medicines = ListField(ReferenceField(Medicine))
    date = DateTimeField(default=datetime.utcnow)

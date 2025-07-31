<template>
  <div class="container">
    <h1>🩺 จัดการข้อมูลนักเรียน</h1>

    <!-- ฟอร์มเพิ่ม/แก้ไข -->
    <div class="form-card">
      <h2>{{ isEditing ? '✏️ แก้ไขข้อมูลนักเรียน' : '➕ เพิ่มนักเรียนใหม่' }}</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>รหัสนักเรียน</label>
          <input v-model="form.studentId" placeholder="รหัสนักเรียน" required />
        </div>

        <div class="form-group">
          <label>ชื่อ</label>
          <input v-model="form.name" placeholder="ชื่อนักเรียน" required />
        </div>

        <div class="form-group">
          <label>อายุ</label>
          <input v-model.number="form.age" type="number" min="0" placeholder="อายุ" required />
        </div>

        <div class="form-group">
          <label>สาขา</label>
          <input v-model="form.major" placeholder="สาขาวิชา" required />
        </div>

        <div class="form-group">
          <label>ชั้นปี</label>
          <input v-model.number="form.year" type="number" min="1" max="5" placeholder="ชั้นปี" required />
        </div>

        <div class="button-group">
          <button type="submit" class="btn primary">{{ isEditing ? 'บันทึกการแก้ไข' : 'เพิ่มนักเรียน' }}</button>
          <button type="button" class="btn secondary" @click="resetForm" v-if="isEditing">ยกเลิก</button>
        </div>
      </form>
    </div>

    <!-- ตารางข้อมูล -->
    <table class="student-table">
      <thead>
        <tr>
          <th>รหัส</th>
          <th>ชื่อ</th>
          <th>อายุ</th>
          <th>สาขา</th>
          <th>ชั้นปี</th>
          <th>การจัดการ</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="student in students" :key="student.studentId">
          <td>{{ student.studentId }}</td>
          <td>{{ student.name }}</td>
          <td>{{ student.age }}</td>
          <td>{{ student.major }}</td>
          <td>{{ student.year }}</td>
          <td>
            <button class="btn small blue" @click="editStudent(student)">แก้ไข</button>
            <button class="btn small red" @click="deleteStudent(student.studentId)">ลบ</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const students = ref([])

const form = ref({
  studentId: '',
  name: '',
  age: null,
  major: '',
  year: null
})

const isEditing = ref(false)
let editingIndex = -1

const handleSubmit = () => {
  if (isEditing.value) {
    students.value[editingIndex] = { ...form.value }
  } else {
    students.value.push({ ...form.value })
  }
  resetForm()
}

const editStudent = (student) => {
  editingIndex = students.value.findIndex(s => s.studentId === student.studentId)
  form.value = { ...student }
  isEditing.value = true
}

const deleteStudent = (studentId) => {
  students.value = students.value.filter(s => s.studentId !== studentId)
  if (isEditing.value && form.value.studentId === studentId) {
    resetForm()
  }
}

const resetForm = () => {
  form.value = {
    studentId: '',
    name: '',
    age: null,
    major: '',
    year: null
  }
  isEditing.value = false
  editingIndex = -1
}
</script>

<style scoped>
.container {
  max-width: 900px;
  margin: auto;
  padding: 20px;
  font-family: 'Segoe UI', sans-serif;
  color: #333;
}

h1 {
  text-align: center;
  color: #00bc7d;
  margin-bottom: 20px;
}

.form-card {
  background: #f9f9ff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 6px rgba(0, 0, 0, 0.05);
  margin-bottom: 30px;
}

.form-card h2 {
  margin-bottom: 16px;
  color: #444;
}

.form-group {
  margin-bottom: 12px;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 4px;
}

input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
}

.button-group {
  margin-top: 12px;
}

.btn {
  padding: 8px 14px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
}

.btn.primary {
  background-color: #00bc7d;
  color: white;
}

.btn.secondary {
  background-color: #e0e1e2;
  color: #333;
  margin-left: 8px;
}

.student-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border: 1px solid #ccc;
}

.student-table th, .student-table td {
  padding: 10px;
  text-align: center;
  border: 1px solid #ddd;
}

.student-table th {
  background-color: #eef7ff;
}

.btn.small {
  padding: 4px 10px;
  font-size: 12px;
}

.btn.blue {
  background-color: #00bc7d;
  color: white;
  margin-right: 5px;
}

.btn.red {
  background-color: #e74c3c;
  color: white;
}
</style>

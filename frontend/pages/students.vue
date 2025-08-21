<template>
  <div class="container">
    <h1>🩺 จัดการข้อมูลนักเรียน</h1>

    <!-- ฟอร์มเพิ่ม/แก้ไข -->
    <div class="form-card">
      <h2>{{ isEditing ? '✏️ แก้ไขข้อมูลนักเรียน' : '➕ เพิ่มนักเรียนใหม่' }}</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>รหัสนักเรียน</label>
          <input v-model="form.student_id" placeholder="รหัสนักเรียน" required />
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
          <input v-model="form.department" placeholder="สาขาวิชา" required />
        </div>

        <div class="form-group">
          <label>ชั้นปี</label>
          <input v-model="form.grade_level" type="text" placeholder="เช่น ปวช.1 / ปวส.2" required />
        </div>

        <div class="button-group">
          <button type="submit" class="btn primary">{{ isEditing ? 'บันทึกการแก้ไข' : 'เพิ่มนักเรียน' }}</button>
          <button type="button" class="btn secondary" @click="resetForm" v-if="isEditing">ยกเลิก</button>
        </div>
      </form>

      <!-- ✅ แถบค้นหา -->
      <div class="search-box">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="🔍 ค้นหาด้วยรหัส ชื่อ หรือ สาขา"
        />
      </div>
    </div>

    <!-- ตารางข้อมูล -->
    <table class="student-table" v-if="filteredStudents.length">
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
        <tr v-for="student in filteredStudents" :key="student.id">
          <td>{{ student.student_id }}</td>
          <td>{{ student.name }}</td>
          <td>{{ student.age }}</td>
          <td>{{ student.department }}</td>
          <td>{{ student.grade_level }}</td>
          <td>
            <button class="btn small blue" @click="editStudent(student)">แก้ไข</button>
            <button class="btn small red" @click="deleteStudent(student.id)">ลบ</button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-if="message" class="text-center mt-4 font-medium" :class="messageColor">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

// ✅ state
const students = ref([])
const form = ref({
  student_id: '',
  name: '',
  age: null,
  department: '',
  grade_level: ''
})
const isEditing = ref(false)
const editId = ref(null)
const searchQuery = ref('')
const message = ref('')
const messageColor = ref('text-green-600')

// ✅ axios instance
const apiUrl = import.meta.env.VITE_API_URL
const token = localStorage.getItem('token')
const axiosInstance = axios.create({
  baseURL: apiUrl,
  headers: {
    Authorization: `Bearer ${token}`
  }
})

// ✅ โหลดข้อมูลเมื่อเริ่มต้น
onMounted(fetchStudents)

async function fetchStudents() {
  try {
    const res = await axiosInstance.get('/api/students')
    students.value = res.data
  } catch (err) {
    console.error('Fetch error:', err)
    message.value = '❌ โหลดข้อมูลนักเรียนไม่สำเร็จ'
    messageColor.value = 'text-red-600'
  }
}

async function handleSubmit() {
  try {
    if (isEditing.value && editId.value) {
      await axiosInstance.put(`/api/students/${editId.value}`, form.value)
      message.value = '✅ แก้ไขข้อมูลนักเรียนสำเร็จ'
    } else {
      const res = await axiosInstance.post('/api/students', form.value)
      students.value.push(res.data) // backend คืน object ทั้งตัว
      message.value = '✅ เพิ่มนักเรียนสำเร็จ'
    }
    messageColor.value = 'text-green-600'
    await fetchStudents()
    resetForm()
  } catch (err) {
    console.error('Save error:', err)
    message.value = '❌ บันทึกข้อมูลไม่สำเร็จ'
    messageColor.value = 'text-red-600'
  }
}

function editStudent(student) {
  form.value = {
    student_id: student.student_id,
    name: student.name,
    age: student.age,
    department: student.department,
    grade_level: student.grade_level
  }
  editId.value = student.id
  isEditing.value = true
  message.value = ''
}

async function deleteStudent(id) {
  if (!confirm('คุณแน่ใจหรือไม่ว่าต้องการลบ?')) return
  try {
    await axiosInstance.delete(`/api/students/${id}`)
    message.value = '🗑️ ลบข้อมูลนักเรียนแล้ว'
    messageColor.value = 'text-green-600'
    await fetchStudents()
  } catch (err) {
    console.error('Delete error:', err)
    message.value = '❌ ไม่สามารถลบได้'
    messageColor.value = 'text-red-600'
  }
}

function resetForm() {
  form.value = {
    student_id: '',
    name: '',
    age: null,
    department: '',
    grade_level: ''
  }
  isEditing.value = false
  editId.value = null
}

// ✅ filter นักเรียน
const filteredStudents = computed(() =>
  students.value.filter(s =>
    (s.student_id?.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
    (s.name?.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
    (s.department?.toLowerCase().includes(searchQuery.value.toLowerCase()))
  )
)
</script>

<style scoped>
/* ใช้สไตล์เดิม */
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
.form-group { margin-bottom: 12px; }
label { font-weight: bold; display: block; margin-bottom: 4px; }
input {
  width: 100%; padding: 8px 12px;
  border: 1px solid #ccc; border-radius: 6px; font-size: 14px;
}
.search-box { margin-top: 15px; }
.search-box input {
  width: 100%; padding: 8px 12px;
  border: 1px solid #00bc7d; border-radius: 6px; font-size: 14px;
}
.button-group { margin-top: 12px; }
.btn {
  padding: 8px 14px; border: none; border-radius: 6px;
  font-size: 14px; cursor: pointer;
}
.btn.primary { background: #00bc7d; color: white; }
.btn.secondary { background: #e0e1e2; color: #333; margin-left: 8px; }
.student-table {
  width: 100%; border-collapse: collapse; background: white; border: 1px solid #ccc;
}
.student-table th, .student-table td {
  padding: 10px; text-align: center; border: 1px solid #ddd;
}
.student-table th { background: #eef7ff; }
.btn.small { padding: 4px 10px; font-size: 12px; }
.btn.blue { background: #00bc7d; color: white; margin-right: 5px; }
.btn.red { background: #e74c3c; color: white; }
</style>

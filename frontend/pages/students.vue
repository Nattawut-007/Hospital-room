<template>
  <div class="min-h-screen flex justify-center items-center bg-gradient-to-tr from-sky-100 via-blue-100 to-indigo-100 p-4">
    <div class="bg-white/90 backdrop-blur-md p-8 rounded-2xl shadow-2xl w-full max-w-5xl">

      <div class="flex justify-center mb-4">
        <img src="https://www.pngmart.com/files/16/Student-PNG-Picture.png" alt="Student" class="h-16 w-16" />
      </div>
      <h1 class="text-3xl font-bold text-center text-blue-700 mb-2">ระบบจัดการข้อมูลนักเรียน</h1>
      <p class="text-center text-gray-500 mb-6">เพิ่ม / แก้ไข / ลบ ข้อมูลนักเรียน</p>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div>
          <label class="block text-gray-700 font-medium mb-1">รหัสนักเรียน</label>
          <input v-model="form.student_id" placeholder="รหัสนักเรียน" class="w-full p-3 border rounded-lg focus:ring-blue-400" />
        </div>
        <div>
          <label class="block text-gray-700 font-medium mb-1">ชื่อ</label>
          <input v-model="form.name" placeholder="ชื่อนักเรียน" class="w-full p-3 border rounded-lg focus:ring-blue-400" />
        </div>
        <div>
          <label class="block text-gray-700 font-medium mb-1">อายุ</label>
          <input v-model.number="form.age" type="number" min="0" placeholder="อายุ" class="w-full p-3 border rounded-lg focus:ring-blue-400" />
        </div>
        <div>
          <label class="block text-gray-700 font-medium mb-1">สาขา</label>
          <input v-model="form.department" placeholder="สาขาวิชา" class="w-full p-3 border rounded-lg focus:ring-blue-400" />
        </div>
        <div>
          <label class="block text-gray-700 font-medium mb-1">ชั้นปี</label>
          <input v-model.number="form.grade_level" type="number" min="1" max="5" placeholder="ชั้นปี" class="w-full p-3 border rounded-lg focus:ring-blue-400" />
        </div>
      </div>

      <button
        @click="isEditing ? updateStudent() : addStudent()"
        class="w-full bg-blue-500 hover:bg-blue-600 text-white py-3 rounded-lg font-semibold mb-4"
      >
        {{ isEditing ? 'อัปเดตข้อมูลนักเรียน' : 'บันทึกข้อมูลนักเรียน' }}
      </button>

      <div class="relative w-full mb-4">
        <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-400">🔍</span>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="ค้นหาด้วยรหัส ชื่อ หรือ สาขา"
          class="w-full pl-10 pr-3 py-3 border rounded-lg focus:ring-blue-400 focus:border-blue-400"
        />
      </div>

      <div v-if="filteredStudents.length" class="overflow-x-auto">
        <table class="w-full border table-auto text-sm">
          <thead class="bg-blue-200 text-blue-800">
            <tr>
              <th class="px-4 py-2 border">#</th>
              <th class="px-4 py-2 border">รหัสนักเรียน</th>
              <th class="px-4 py-2 border">ชื่อ</th>
              <th class="px-4 py-2 border">อายุ</th>
              <th class="px-4 py-2 border">สาขา</th>
              <th class="px-4 py-2 border">ชั้นปี</th>
              <th class="px-4 py-2 border">การจัดการ</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in filteredStudents" :key="item._id" class="hover:bg-blue-50">
              <td class="px-4 py-2 border text-center">{{ index + 1 }}</td>
              <td class="px-4 py-2 border">{{ item.student_id }}</td>
              <td class="px-4 py-2 border">{{ item.name }}</td>
              <td class="px-4 py-2 border text-center">{{ item.age }}</td>
              <td class="px-4 py-2 border">{{ item.department }}</td>
              <td class="px-4 py-2 border text-center">{{ item.grade_level }}</td>
              <td class="px-4 py-2 border text-center space-x-2">
                <button @click="editStudent(item)" class="bg-yellow-400 hover:bg-yellow-500 text-white px-3 py-1 rounded">แก้ไข</button>
                <button @click="deleteStudent(item._id)" class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded">ลบ</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <p v-if="message" class="text-center text-green-600 mt-4 font-medium">{{ message }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

// เปลี่ยนค่าเริ่มต้นของฟิลด์ตัวเลขเป็น 0 แทน null
const form = ref({ student_id: '', name: '', age: 0, department: '', grade_level: 0 })
const studentsList = ref([])
const isEditing = ref(false)
const editId = ref(null)
const searchQuery = ref('')
const message = ref('')

const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000'
const token = localStorage.getItem('token')

const axiosInstance = axios.create({
  baseURL: apiUrl,
  headers: {
    Authorization: `Bearer ${token}`
  }
})

onMounted(() => {
  fetchStudents()
})

const fetchStudents = async () => {
  try {
    const res = await axiosInstance.get('/api/students')
    studentsList.value = res.data
  } catch (err) {
    console.error('Fetch error:', err)
    message.value = 'ไม่สามารถโหลดข้อมูลนักเรียนได้'
  }
}

const addStudent = async () => {
  // ตรวจสอบข้อมูลก่อนส่ง
  if (!form.value.student_id || !form.value.name || !form.value.department) {
    message.value = 'กรุณากรอกข้อมูลให้ครบ'
    return
  }
  try {
    // ส่งข้อมูลที่มีชื่อฟิลด์ตรงกับ backend
    const res = await axiosInstance.post('/api/students', form.value)
    studentsList.value.push(res.data)
    resetForm()
    message.value = 'เพิ่มข้อมูลนักเรียนสำเร็จ'
  } catch (err) {
    console.error('Add error:', err)
    if (err.response && err.response.data && err.response.data.error) {
      message.value = 'ไม่สามารถเพิ่มข้อมูลนักเรียนได้: ' + err.response.data.error
    } else {
      message.value = 'ไม่สามารถเพิ่มข้อมูลนักเรียนได้'
    }
  }
}

const editStudent = (item) => {
  // นำข้อมูลจากตารางมาใส่ในฟอร์มเพื่อแก้ไข
  form.value = { 
    student_id: item.student_id, 
    name: item.name, 
    age: item.age, 
    department: item.department, 
    grade_level: item.grade_level 
  }
  editId.value = item._id
  isEditing.value = true
  message.value = ''
}

const updateStudent = async () => {
  if (!editId.value) return
  try {
    // ส่งข้อมูลที่มีชื่อฟิลด์ตรงกับ backend
    await axiosInstance.put(`/api/students/${editId.value}`, form.value)
    await fetchStudents()
    resetForm()
    message.value = 'อัปเดตข้อมูลนักเรียนแล้ว'
  } catch (err) {
    console.error('Update error:', err)
    message.value = 'ไม่สามารถอัปเดตข้อมูลนักเรียนได้'
  }
}

const deleteStudent = async (id) => {
  if (!confirm('คุณแน่ใจหรือไม่ว่าต้องการลบ?')) return
  try {
    await axiosInstance.delete(`/api/students/${id}`)
    await fetchStudents()
    message.value = 'ลบข้อมูลนักเรียนแล้ว'
  } catch (err) {
    console.error('Delete error:', err)
    message.value = 'ไม่สามารถลบข้อมูลนักเรียนได้'
  }
}

const filteredStudents = computed(() =>
  studentsList.value.filter(
    s =>
      s.student_id?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      s.name?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      s.department?.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
)

const resetForm = () => {
  form.value = { student_id: '', name: '', age: 0, department: '', grade_level: 0 }
  isEditing.value = false
  editId.value = null
}
</script>

<style scoped>
/*
  Note: This Tailwind CSS-based code does not require a separate <style> block for styling
  as all styles are handled via utility classes within the template.
  The animation is an exception.
*/
img {
  animation: pulse 3s infinite;
}
@keyframes pulse {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.05); opacity: 0.9; }
  100% { transform: scale(1); opacity: 1; }
}
</style>

<style scoped>
/*
  Note: This Tailwind CSS-based code does not require a separate <style> block for styling
  as all styles are handled via utility classes within the template.
  The animation is an exception.
*/
img {
  animation: pulse 3s infinite;
}
@keyframes pulse {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.05); opacity: 0.9; }
  100% { transform: scale(1); opacity: 1; }
}
</style>
<template>
  <div class="flex justify-center items-center min-h-screen bg-gradient-to-tr from-emerald-100 via-blue-100 to-indigo-100 p-4">
    <div class="bg-white/90 backdrop-blur-md p-8 rounded-2xl shadow-2xl w-full max-w-5xl">

      <!-- Header -->
      <div class="flex justify-center mb-6">
        <img src="https://png.pngtree.com/png-vector/20210310/ourlarge/pngtree-nurse-day-doctor-logo-png-image_3038174.jpg" alt="Nurse" class="h-16 w-16" />
      </div>
      <h1 class="text-3xl font-bold text-center text-emerald-700 mb-2">จัดการข้อมูลการรักษา</h1>
      <p class="text-center text-sm text-gray-500 mb-6">ระบบเพิ่ม / แก้ไข / ลบ การรักษา</p>

      <!-- Form -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label class="block text-gray-700 font-medium mb-1">รหัสนักเรียน</label>
          <input v-model="form.student_id" placeholder="เช่น 65001" class="w-full p-3 border rounded-lg focus:ring-emerald-400" />
        </div>
        <div>
          <label class="block text-gray-700 font-medium mb-1">อาการ</label>
          <input v-model="form.symptoms" placeholder="เช่น ไข้ ปวดหัว" class="w-full p-3 border rounded-lg focus:ring-emerald-400" />
        </div>
        <div class="md:col-span-2">
          <label class="block text-gray-700 font-medium mb-1">ยาที่ใช้</label>
          <select v-model="form.medicine_ids" multiple class="w-full p-3 border rounded-lg focus:ring-emerald-400">
            <option v-for="m in medicines" :key="m._id" :value="m._id">{{ m.name }} ({{ m.brand }})</option>
          </select>
          <small class="text-gray-500">กด Ctrl / Cmd เพื่อเลือกหลายรายการ</small>
        </div>
      </div>

      <button
        @click="isEditing ? updateTreatment() : addTreatment()"
        class="w-full bg-emerald-500 hover:bg-emerald-600 text-white py-3 rounded-lg font-semibold mb-4"
      >
        {{ isEditing ? 'อัปเดตข้อมูลการรักษา' : 'บันทึกข้อมูลการรักษา' }}
      </button>

      <!-- ✅ ช่องค้นหา -->
      <div class="mb-6">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="🔍 ค้นหาด้วยชื่อ / รหัส / อาการ"
          class="w-full p-3 border rounded-lg focus:ring-emerald-400"
        />
      </div>

      <!-- Table -->
      <div v-if="filteredTreatments.length" class="overflow-x-auto">
        <table class="w-full border table-auto text-sm">
          <thead class="bg-emerald-200 text-emerald-800">
            <tr>
              <th class="px-4 py-2 border">#</th>
              <th class="px-4 py-2 border">รหัส</th>
              <th class="px-4 py-2 border">ชื่อ</th>
              <th class="px-4 py-2 border">อาการ</th>
              <th class="px-4 py-2 border">ยาที่ใช้</th>
              <th class="px-4 py-2 border">วันที่</th>
              <th class="px-4 py-2 border">การจัดการ</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(t, index) in filteredTreatments" :key="t.id" class="hover:bg-emerald-50">
              <td class="px-4 py-2 border text-center">{{ index + 1 }}</td>
              <td class="px-4 py-2 border">{{ t.student.student_id }}</td>
              <td class="px-4 py-2 border">{{ t.student.name }}</td>
              <td class="px-4 py-2 border">{{ t.symptoms }}</td>
              <td class="px-4 py-2 border">
                <ul>
                  <li v-for="m in t.medicines" :key="m.id">{{ m.name }}</li>
                </ul>
              </td>
              <td class="px-4 py-2 border">{{ new Date(t.date).toLocaleString() }}</td>
              <td class="px-4 py-2 border text-center space-x-2">
                <button @click="editTreatment(t)" class="bg-yellow-400 hover:bg-yellow-500 text-white px-3 py-1 rounded">แก้ไข</button>
                <button @click="deleteTreatment(t.id)" class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded">ลบ</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- ข้อความแจ้งสถานะ -->
      <p v-if="message" class="text-center mt-4 font-medium" :class="messageColor">{{ message }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const treatments = ref([])
const medicines = ref([])
const form = ref({
  student_id: '',
  symptoms: '',
  medicine_ids: []
})

const isEditing = ref(false)
const editId = ref(null)
const searchQuery = ref('')
const message = ref('')
const messageColor = ref('text-green-600')

// แก้ไขตรงนี้ โดยตรวจสอบว่าเป็น client หรือไม่ก่อนเรียก localStorage
const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null

const apiUrl = import.meta.env.VITE_API_URL
const axiosInstance = axios.create({
  baseURL: apiUrl,
  headers: token ? { Authorization: `Bearer ${token}` } : {}
})

onMounted(() => {
  fetchTreatments()
  fetchMedicines()
})

async function fetchTreatments() {
  try {
    const res = await axiosInstance.get('/api/treatments')
    treatments.value = res.data
  } catch (err) {
    message.value = '❌ โหลดข้อมูลการรักษาไม่สำเร็จ'
    messageColor.value = 'text-red-600'
  }
}

async function fetchMedicines() {
  try {
    const res = await axiosInstance.get('/api/medicines')
    medicines.value = res.data
  } catch (err) {
    console.error('ไม่สามารถโหลดรายการยาได้')
  }
}

async function addTreatment() {
  try {
    await axiosInstance.post('/api/treatments', form.value)
    message.value = '✅ เพิ่มข้อมูลการรักษาสำเร็จ'
    messageColor.value = 'text-green-600'
    await fetchTreatments()
    resetForm()
  } catch (err) {
    message.value = '❌ เพิ่มไม่สำเร็จ'
    messageColor.value = 'text-red-600'
  }
}

function editTreatment(t) {
  form.value = {
    student_id: t.student.student_id,
    symptoms: t.symptoms,
    // ✅ แก้ไขตรงนี้: ใช้ m._id แทน m.id
    medicine_ids: t.medicines.map(m => m._id)
  }
  editId.value = t._id // ✅ แก้ไขตรงนี้: ใช้ t._id แทน t.id
  isEditing.value = true
  message.value = ''
}

async function updateTreatment() {
  try {
    // ✅ แก้ไขตรงนี้: ตรวจสอบให้แน่ใจว่า editId.value มีค่าถูกต้อง
    console.log("Updating with ID:", editId.value);
    await axiosInstance.put(`/api/treatments/${editId.value}`, form.value)
    message.value = '✅ อัปเดตข้อมูลการรักษาสำเร็จ'
    messageColor.value = 'text-green-600'
    await fetchTreatments()
    resetForm()
  } catch (err) {
    // โค้ดจัดการ Error
    if (err.response && err.response.status === 400) {
      message.value = `❌ อัปเดตไม่สำเร็จ: ${err.response.data.error}`
    } else {
      message.value = '❌ อัปเดตไม่สำเร็จ'
    }
    messageColor.value = 'text-red-600'
    console.error(err)
  }
}

async function deleteTreatment(id) {
  if (!confirm('คุณแน่ใจหรือไม่ว่าต้องการลบ?')) return
  try {
    await axiosInstance.delete(`/api/treatments/${id}`)
    message.value = '🗑️ ลบข้อมูลการรักษาแล้ว'
    messageColor.value = 'text-green-600'
    await fetchTreatments()
  } catch (err) {
    message.value = '❌ ลบไม่สำเร็จ'
    messageColor.value = 'text-red-600'
  }
}

function resetForm() {
  form.value = { student_id: '', symptoms: '', medicine_ids: [] }
  isEditing.value = false
  editId.value = null
}

const filteredTreatments = computed(() =>
  treatments.value.filter(t =>
    (t.student?.name?.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
    (t.student?.student_id?.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
    (t.symptoms?.toLowerCase().includes(searchQuery.value.toLowerCase()))
  )
)
</script>

<style scoped>
img { animation: pulse 3s infinite; }
@keyframes pulse {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.05); opacity: 0.9; }
  100% { transform: scale(1); opacity: 1; }
}
</style>

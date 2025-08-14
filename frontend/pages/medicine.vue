<template>
  <div class="min-h-screen flex justify-center items-center bg-gradient-to-tr from-emerald-100 via-blue-100 to-indigo-100 p-4">
    <div class="bg-white/90 backdrop-blur-md p-8 rounded-2xl shadow-2xl w-full max-w-4xl">

      <!-- Header -->
      <div class="flex justify-center mb-4">
        <img src="https://png.pngtree.com/png-vector/20210310/ourlarge/pngtree-nurse-day-doctor-logo-png-image_3038174.jpg" alt="Nurse" class="h-16 w-16" />
      </div>
      <h1 class="text-3xl font-bold text-center text-emerald-700 mb-2">ระบบจัดการยา</h1>
      <p class="text-center text-gray-500 mb-6">เพิ่ม / แก้ไข / ลบ ข้อมูลยา</p>

      <!-- Form -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div>
          <label class="block text-gray-700 font-medium mb-1">ชื่อยา</label>
          <input v-model="form.name" placeholder="ชื่อยา" class="w-full p-3 border rounded-lg focus:ring-emerald-400" />
        </div>
        <div>
          <label class="block text-gray-700 font-medium mb-1">ยี่ห้อ</label>
          <input v-model="form.brand" placeholder="ยี่ห้อ" class="w-full p-3 border rounded-lg focus:ring-emerald-400" />
        </div>
        <div>
          <label class="block text-gray-700 font-medium mb-1">จำนวน</label>
          <input v-model="form.stock" type="number" min="0" placeholder="จำนวน" class="w-full p-3 border rounded-lg focus:ring-emerald-400" />
        </div>
      </div>

      <button
        @click="isEditing ? updateMedicine() : addMedicine()"
        class="w-full bg-emerald-500 hover:bg-emerald-600 text-white py-3 rounded-lg font-semibold mb-4"
      >
        {{ isEditing ? 'อัปเดตข้อมูลยา' : 'บันทึกข้อมูลยา' }}
      </button>

      <!-- Search -->
      <div class="relative w-full mb-4">
        <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-400">🔍</span>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="ค้นหาชื่อยา หรือ ยี่ห้อ"
          class="w-full pl-10 pr-3 py-3 border rounded-lg focus:ring-emerald-400 focus:border-emerald-400"
        />
      </div>

      <!-- Table -->
      <div v-if="filteredMedicines.length" class="overflow-x-auto">
        <table class="w-full border table-auto text-sm">
          <thead class="bg-emerald-200 text-emerald-800">
            <tr>
              <th class="px-4 py-2 border">#</th>
              <th class="px-4 py-2 border">ชื่อยา</th>
              <th class="px-4 py-2 border">ยี่ห้อ</th>
              <th class="px-4 py-2 border">จำนวน</th>
              <th class="px-4 py-2 border">การจัดการ</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in filteredMedicines" :key="item._id" class="hover:bg-emerald-50">
              <td class="px-4 py-2 border text-center">{{ index + 1 }}</td>
              <td class="px-4 py-2 border">{{ item.name }}</td>
              <td class="px-4 py-2 border">{{ item.brand }}</td>
              <td class="px-4 py-2 border text-center">{{ item.stock }}</td>
              <td class="px-4 py-2 border text-center space-x-2">
                <button @click="editMedicine(item)" class="bg-yellow-400 hover:bg-yellow-500 text-white px-3 py-1 rounded">แก้ไข</button>
                <button @click="deleteMedicine(item._id)" class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded">ลบ</button>
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

const form = ref({ name: '', brand: '', stock: 0 })
const medicineList = ref([])
const isEditing = ref(false)
const editId = ref(null)
const searchQuery = ref('')
const message = ref('')

const apiUrl = import.meta.env.VITE_API_URL
const token = localStorage.getItem('token')

const axiosInstance = axios.create({
  baseURL: apiUrl,
  headers: {
    Authorization: `Bearer ${token}`
  }
})

onMounted(() => {
  fetchMedicines()
})

const fetchMedicines = async () => {
  try {
    const res = await axiosInstance.get('/api/medicines')
    medicineList.value = res.data
  } catch (err) {
    console.error('Fetch error:', err)
    message.value = 'ไม่สามารถโหลดข้อมูลยาได้'
  }
}

const addMedicine = async () => {
  if (!form.value.name || !form.value.brand || form.value.stock < 0) {
    message.value = 'กรุณากรอกข้อมูลให้ครบ'
    return
  }
  try {
    const res = await axiosInstance.post('/api/medicines', form.value)
    medicineList.value.push(res.data)
    resetForm()
    message.value = 'เพิ่มข้อมูลยาสำเร็จ'
  } catch (err) {
    console.error('Add error:', err)
    message.value = 'ไม่สามารถเพิ่มข้อมูลยาได้'
  }
}

const editMedicine = (item) => {
  form.value = { name: item.name, brand: item.brand, stock: item.stock }
  editId.value = item._id
  isEditing.value = true
  message.value = ''
}

const updateMedicine = async () => {
  if (!editId.value) return
  try {
    await axiosInstance.put(`/api/medicines/${editId.value}`, form.value)
    await fetchMedicines()
    resetForm()
    message.value = 'อัปเดตข้อมูลยาแล้ว'
  } catch (err) {
    console.error('Update error:', err)
    message.value = 'ไม่สามารถอัปเดตข้อมูลยาได้'
  }
}

const deleteMedicine = async (id) => {
  if (!confirm('คุณแน่ใจหรือไม่ว่าต้องการลบ?')) return
  try {
    await axiosInstance.delete(`/api/medicines/${id}`)
    await fetchMedicines()
    message.value = 'ลบข้อมูลยาแล้ว'
  } catch (err) {
    console.error('Delete error:', err)
    message.value = 'ไม่สามารถลบข้อมูลยาได้'
  }
}

const filteredMedicines = computed(() =>
  medicineList.value.filter(
    m =>
      m.name?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      m.brand?.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
)

const resetForm = () => {
  form.value = { name: '', brand: '', stock: 0 }
  isEditing.value = false
  editId.value = null
}
</script>

<style scoped>
img {
  animation: pulse 3s infinite;
}
@keyframes pulse {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.05); opacity: 0.9; }
  100% { transform: scale(1); opacity: 1; }
}
</style>

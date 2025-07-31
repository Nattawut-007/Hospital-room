<template>
  <div class="flex justify-center items-center min-h-screen bg-gradient-to-tr from-emerald-100 via-blue-100 to-indigo-100 p-4">
    <div class="bg-white/90 backdrop-blur-md p-8 rounded-2xl shadow-2xl w-full max-w-3xl">
      
      <!-- Header -->
      <div class="flex justify-center mb-6">
        <img src="https://png.pngtree.com/png-vector/20210310/ourlarge/pngtree-nurse-day-doctor-logo-png-image_3038174.jpg" alt="Nurse" class="h-16 w-16" />
      </div>
      <h1 class="text-3xl font-bold text-center text-emerald-700 mb-2">จัดการข้อมูลยา</h1>
      <p class="text-center text-sm text-gray-500 mb-6">ระบบเพื่มข้อมูลยา</p>

      <!-- Form -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div>
          <label class="block text-gray-700 font-medium mb-1">ชื่อยา</label>
          <input v-model="form.name" placeholder="ชื่อยา" class="w-full p-3 border rounded-lg focus:ring-emerald-400" />
        </div>
        <div>
          <label class="block text-gray-700 font-medium mb-1">ประเภท</label>
          <input v-model="form.type" placeholder="เช่น ยาเม็ด" class="w-full p-3 border rounded-lg focus:ring-emerald-400" />
        </div>
        <div>
          <label class="block text-gray-700 font-medium mb-1">จำนวน</label>
          <input v-model="form.quantity" type="number" placeholder="จำนวน" class="w-full p-3 border rounded-lg focus:ring-emerald-400" />
        </div>
      </div>

      <button
        @click="isEditing ? updateMedicine() : addMedicine()"
        class="w-full bg-emerald-500 hover:bg-emerald-600 text-white py-3 rounded-lg font-semibold mb-6"
      >
        {{ isEditing ? 'อัปเดตข้อมูลยา' : 'บันทึกข้อมูลยา' }}
      </button>

      <!-- Table -->
      <div v-if="medicineList.length" class="overflow-x-auto">
        <table class="w-full border table-auto text-sm">
          <thead class="bg-emerald-200 text-emerald-800">
            <tr>
              <th class="px-4 py-2 border">#</th>
              <th class="px-4 py-2 border">ชื่อยา</th>
              <th class="px-4 py-2 border">ประเภท</th>
              <th class="px-4 py-2 border">จำนวน</th>
              <th class="px-4 py-2 border">การจัดการ</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in medicineList" :key="index" class="hover:bg-emerald-50">
              <td class="px-4 py-2 border text-center">{{ index + 1 }}</td>
              <td class="px-4 py-2 border">{{ item.name }}</td>
              <td class="px-4 py-2 border">{{ item.type }}</td>
              <td class="px-4 py-2 border text-center">{{ item.quantity }}</td>
              <td class="px-4 py-2 border text-center space-x-2">
                <button @click="editMedicine(index)" class="bg-yellow-400 hover:bg-yellow-500 text-white px-3 py-1 rounded">แก้ไข</button>
                <button @click="deleteMedicine(index)" class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded">ลบ</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <p v-if="message" class="text-green-600 text-sm mt-4 text-center font-medium">
        {{ message }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const form = ref({
  name: '',
  type: '',
  quantity: ''
})

const medicineList = ref([])
const isEditing = ref(false)
const editIndex = ref(null)
const message = ref('')

const addMedicine = () => {
  if (form.value.name && form.value.type && form.value.quantity) {
    medicineList.value.push({ ...form.value })
    resetForm()
    message.value = 'เพิ่มข้อมูลยาสำเร็จแล้ว'
  } else {
    message.value = 'กรุณากรอกข้อมูลให้ครบ'
  }
}

const editMedicine = (index) => {
  form.value = { ...medicineList.value[index] }
  isEditing.value = true
  editIndex.value = index
  message.value = ''
}

const updateMedicine = () => {
  if (editIndex.value !== null) {
    medicineList.value[editIndex.value] = { ...form.value }
    message.value = 'อัปเดตข้อมูลยาสำเร็จแล้ว'
    resetForm()
  }
}

const deleteMedicine = (index) => {
  medicineList.value.splice(index, 1)
  message.value = 'ลบข้อมูลยาแล้ว'
  resetForm()
}

const resetForm = () => {
  form.value = { name: '', type: '', quantity: '' }
  isEditing.value = false
  editIndex.value = null
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

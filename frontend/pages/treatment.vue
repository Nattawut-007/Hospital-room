<template>
  <div class="flex justify-center items-center min-h-screen bg-gradient-to-tr from-emerald-100 via-blue-100 to-indigo-100 p-4">
    <div class="bg-white/90 backdrop-blur-md p-8 rounded-2xl shadow-2xl w-full max-w-4xl">

      <!-- Header -->
      <div class="flex justify-center mb-6">
        <img src="https://png.pngtree.com/png-vector/20210310/ourlarge/pngtree-nurse-day-doctor-logo-png-image_3038174.jpg" alt="Nurse" class="h-16 w-16" />
      </div>
      <h1 class="text-3xl font-bold text-center text-emerald-700 mb-2">จัดการข้อมูลการรักษา</h1>
      <p class="text-center text-sm text-gray-500 mb-6">ระบบเพิ่มข้อมูลแผนการรักษา</p>

      <!-- Form -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label class="block text-gray-700 font-medium mb-1">ชื่อผู้ป่วย</label>
          <input v-model="form.patient_name" placeholder="ชื่อผู้ป่วย" class="w-full p-3 border rounded-lg focus:ring-emerald-400" />
        </div>
        <div>
          <label class="block text-gray-700 font-medium mb-1">ชื่อแพทย์</label>
          <input v-model="form.doctor" placeholder="ชื่อแพทย์" class="w-full p-3 border rounded-lg focus:ring-emerald-400" />
        </div>
        <div>
          <label class="block text-gray-700 font-medium mb-1">วินิจฉัยโรค</label>
          <input v-model="form.diagnosis" placeholder="วินิจฉัยโรค" class="w-full p-3 border rounded-lg focus:ring-emerald-400" />
        </div>
        <div>
          <label class="block text-gray-700 font-medium mb-1">วันที่รักษา</label>
          <input type="date" v-model="form.date" class="w-full p-3 border rounded-lg focus:ring-emerald-400" />
        </div>
        <!-- เพิ่มช่องค่าใช้จ่าย -->
        <div>
          <label class="block text-gray-700 font-medium mb-1">ค่าใช้จ่าย (บาท)</label>
          <input
            type="text"
            v-model="form.cost"
            @input="onCostInput"
            placeholder="ค่าใช้จ่าย"
            class="w-full p-3 border rounded-lg focus:ring-emerald-400"
          />
        </div>
        <div class="md:col-span-2">
          <label class="block text-gray-700 font-medium mb-1">แผนการรักษา</label>
          <textarea v-model="form.treatment_plan" placeholder="แผนการรักษา" rows="3" class="w-full p-3 border rounded-lg focus:ring-emerald-400"></textarea>
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
          placeholder="🔍 ค้นหาด้วยชื่อผู้ป่วย / วินิจฉัยโรค / แพทย์"
          class="w-full p-3 border rounded-lg focus:ring-emerald-400"
        />
      </div>

      <!-- Table -->
      <div v-if="treatmentList.length" class="overflow-x-auto">
        <table class="w-full border table-auto text-sm">
          <thead class="bg-emerald-200 text-emerald-800">
            <tr>
              <th class="px-4 py-2 border">#</th>
              <th class="px-4 py-2 border">ชื่อผู้ป่วย</th>
              <th class="px-4 py-2 border">วินิจฉัยโรค</th>
              <th class="px-4 py-2 border">แผนการรักษา</th>
              <th class="px-4 py-2 border">ชื่อแพทย์</th>
              <th class="px-4 py-2 border">วันที่รักษา</th>
              <th class="px-4 py-2 border">ค่าใช้จ่าย (บาท)</th>
              <th class="px-4 py-2 border">การจัดการ</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in filteredTreatmentList" :key="index" class="hover:bg-emerald-50">
              <td class="px-4 py-2 border text-center">{{ index + 1 }}</td>
              <td class="px-4 py-2 border">{{ item.patient_name }}</td>
              <td class="px-4 py-2 border">{{ item.diagnosis }}</td>
              <td class="px-4 py-2 border">{{ item.treatment_plan }}</td>
              <td class="px-4 py-2 border">{{ item.doctor }}</td>
              <td class="px-4 py-2 border">{{ item.date }}</td>
              <td class="px-4 py-2 border text-right">{{ item.cost.toLocaleString() }}</td>
              <td class="px-4 py-2 border text-center space-x-2">
                <button @click="editTreatment(index)" class="bg-yellow-400 hover:bg-yellow-500 text-white px-3 py-1 rounded">แก้ไข</button>
                <button @click="deleteTreatment(index)" class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded">ลบ</button>
                <button @click="openReceipt(index)" class="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded">ออกใบเสร็จ</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- ข้อความแจ้งสถานะ -->
      <p v-if="message" class="text-green-600 text-sm mt-4 text-center font-medium">
        {{ message }}
      </p>

      <!-- Modal ใบเสร็จ -->
      <div v-if="showReceipt" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center p-4">
        <div class="bg-white p-6 rounded shadow-lg max-w-md w-full relative print:p-0 print:shadow-none">
          <button class="absolute top-2 right-2 text-gray-600 hover:text-gray-800" @click="closeReceipt">✖</button>
          <h2 class="text-xl font-bold mb-4 text-center">ใบเสร็จรับเงิน</h2>
          <div class="mb-4">
            <p><strong>ชื่อผู้ป่วย:</strong> {{ currentReceipt.patient_name }}</p>
            <p><strong>วันที่รักษา:</strong> {{ currentReceipt.date }}</p>
            <p><strong>ชื่อแพทย์:</strong> {{ currentReceipt.doctor }}</p>
            <p><strong>วินิจฉัยโรค:</strong> {{ currentReceipt.diagnosis }}</p>
            <p><strong>แผนการรักษา:</strong> {{ currentReceipt.treatment_plan }}</p>
            <p><strong>ค่าใช้จ่ายทั้งหมด:</strong> {{ currentReceipt.cost.toLocaleString() }} บาท</p>
          </div>
          <div class="text-center">
            <button @click="printReceipt" class="bg-emerald-500 hover:bg-emerald-600 text-white px-4 py-2 rounded">
              พิมพ์ใบเสร็จ
            </button>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const form = ref({
  patient_name: '',
  diagnosis: '',
  treatment_plan: '',
  doctor: '',
  date: '',
  cost: 0
})

const treatmentList = ref([])
const isEditing = ref(false)
const editIndex = ref(null)
const message = ref('')

const searchQuery = ref('') // ✅ เก็บคำค้นหา

const filteredTreatmentList = computed(() =>
  treatmentList.value.filter(item =>
    item.patient_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    item.diagnosis.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    item.doctor.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
)

const showReceipt = ref(false)
const currentReceipt = ref({})

const addTreatment = () => {
  if (
    form.value.patient_name &&
    form.value.diagnosis &&
    form.value.treatment_plan &&
    form.value.doctor &&
    form.value.date &&
    form.value.cost >= 0
  ) {
    treatmentList.value.push({ ...form.value })
    resetForm()
    message.value = 'เพิ่มข้อมูลการรักษาสำเร็จแล้ว'
  } else {
    message.value = 'กรุณากรอกข้อมูลให้ครบทุกช่อง และค่าใช้จ่ายต้องไม่ติดลบ'
  }
}

const editTreatment = (index) => {
  form.value = { ...treatmentList.value[index] }
  isEditing.value = true
  editIndex.value = index
  message.value = ''
}

const updateTreatment = () => {
  if (editIndex.value !== null) {
    treatmentList.value[editIndex.value] = { ...form.value }
    resetForm()
    message.value = 'อัปเดตข้อมูลการรักษาสำเร็จแล้ว'
  }
}

const deleteTreatment = (index) => {
  treatmentList.value.splice(index, 1)
  message.value = 'ลบข้อมูลการรักษาแล้ว'
  resetForm()
}

const resetForm = () => {
  form.value = {
    patient_name: '',
    diagnosis: '',
    treatment_plan: '',
    doctor: '',
    date: '',
    cost: 0
  }
  isEditing.value = false
  editIndex.value = null
}

const openReceipt = (index) => {
  currentReceipt.value = { ...treatmentList.value[index] }
  showReceipt.value = true
}

const closeReceipt = () => {
  showReceipt.value = false
}

const printReceipt = () => {
  const originalTitle = document.title
  document.title = `ใบเสร็จรับเงิน_${currentReceipt.value.patient_name}_${currentReceipt.value.date}`
  window.print()
  document.title = originalTitle
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
@media print {
  body * { visibility: hidden; }
  .print\:block, .print\:block * { visibility: visible; }
  .print\:p-0 { padding: 0 !important; }
  .print\:shadow-none { box-shadow: none !important; }
  .fixed { position: static !important; }
}
</style>

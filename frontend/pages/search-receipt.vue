<template>
  <div class="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 flex flex-col items-center py-10">
    <h1 class="text-2xl font-bold text-emerald-700 mb-6">ค้นหาใบเสร็จ</h1>

    <form @submit.prevent="searchReceipt" class="bg-white p-6 rounded-xl shadow-md w-full max-w-md space-y-4">
      <input
        v-model="patientName"
        type="text"
        placeholder="พิมพ์ชื่อผู้ป่วย"
        class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-400"
        required
      />
      <button
        type="submit"
        class="w-full bg-emerald-500 hover:bg-emerald-600 text-white font-semibold py-2 px-4 rounded-lg transition"
      >
        ค้นหา
      </button>
    </form>

    <!-- แสดงผลลัพธ์ -->
    <div v-if="results.length > 0" class="mt-6 w-full max-w-md bg-white rounded-xl shadow p-4">
      <h2 class="text-lg font-semibold mb-3">ผลการค้นหา</h2>
      <ul class="space-y-2">
        <li
          v-for="(item, index) in results"
          :key="index"
          class="p-3 border rounded-lg hover:bg-gray-50"
        >
          <p><strong>เลขที่ใบเสร็จ:</strong> {{ item.receipt_no }}</p>
          <p><strong>จำนวนเงิน:</strong> {{ item.amount }} บาท</p>
        </li>
      </ul>
    </div>

    <p v-else-if="searched" class="mt-6 text-red-500">ไม่พบข้อมูลใบเสร็จ</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const patientName = ref('')
const results = ref([])
const searched = ref(false)

const searchReceipt = async () => {
  searched.value = false
  results.value = []

  try {
    // ตัวอย่าง: เรียก API ที่คุณสร้างไว้
    const res = await fetch(`/api/search-receipt?patient=${encodeURIComponent(patientName.value)}`)
    const data = await res.json()

    if (data.length > 0) {
      results.value = data
    }
    searched.value = true
  } catch (error) {
    console.error(error)
  }
}
</script>

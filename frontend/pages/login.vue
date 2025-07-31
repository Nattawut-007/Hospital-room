<template>
  <div class="flex justify-center items-center min-h-screen bg-gradient-to-tr from-emerald-100 via-blue-100 to-indigo-100 p-4">
    <div class="bg-white/90 backdrop-blur-md p-8 rounded-2xl shadow-2xl w-full max-w-md transition-all duration-300 hover:shadow-emerald-300">
      <div class="flex items-center justify-center mb-6">
        <img src="https://png.pngtree.com/png-vector/20210310/ourlarge/pngtree-nurse-day-doctor-logo-png-image_3038174.jpg" alt="Nurse Login" class="h-16 w-16" />
      </div>

      <h1 class="text-3xl font-bold text-center text-emerald-700 mb-2">Nurse Station</h1>
      <p class="text-center text-sm text-gray-500 mb-6">ระบบดูแลสุขภาพนักเรียน</p>

      <div class="mb-4">
        <label class="block text-gray-700 font-medium mb-1" for="username">ชื่อผู้ใช้</label>
        <input
          id="username"
          v-model="username"
          placeholder="กรอกชื่อผู้ใช้"
          class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-400"
        />
      </div>

      <div class="mb-6">
        <label class="block text-gray-700 font-medium mb-1" for="password">รหัสผ่าน</label>
        <input
          id="password"
          v-model="password"
          type="password"
          placeholder="กรอกรหัสผ่าน"
          class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-400"
        />
      </div>

      <button
        @click="handleLogin"
        class="w-full bg-emerald-500 hover:bg-emerald-600 text-white font-semibold py-3 rounded-lg transition duration-300"
      >
        เข้าสู่ระบบ
      </button>

      <p v-if="errorMsg" class="text-red-600 text-sm mt-4 text-center font-medium">
        {{ errorMsg }}
      </p>

      <div class="mt-6 text-center text-sm text-gray-600">
        <a href="#" class="text-emerald-500 hover:underline">ลืมรหัสผ่าน?</a>
        <span class="mx-2">|</span>
        <a href="#" class="text-emerald-500 hover:underline">สมัครสมาชิก</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const errorMsg = ref('')
const router = useRouter()

const handleLogin = async () => {
  errorMsg.value = ''
  try {
    const res = await axios.post('http://localhost:5000/api/login', {
      username: username.value,
      password: password.value
    })

    localStorage.setItem('token', res.data.access_token)
    router.push('/dashboard')
  } catch (err) {
    errorMsg.value =
      err.response?.data?.msg || 'ไม่สามารถเข้าสู่ระบบได้ กรุณาตรวจสอบอีกครั้ง'
  }
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

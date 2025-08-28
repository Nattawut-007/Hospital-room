export default defineNuxtRouteMiddleware((to, from) => {
  // ตรวจสอบว่าโค้ดรันอยู่บนฝั่ง client
  if (process.client) {
    const token = localStorage.getItem('token')
    if (!token) {
      return navigateTo('/login')
    }
  }
})
<!-- pages/index.vue -->
<template>
  <div>
    <!-- แสดงข้อความระหว่างรอ redirect -->
    <p>กำลังเปลี่ยนหน้า...</p>
  </div>
</template>

<script setup>
navigateTo('/login')  // redirect ไปหน้า login
</script>
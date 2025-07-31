<template>
  <nav class="bg-white shadow-md px-6 py-4 flex justify-between items-center border-b border-emerald-200">
    <div class="flex items-center space-x-3">
      <img src="https://cdn-icons-png.flaticon.com/512/9436/9436354.png" class="h-8 w-8" alt="nurse icon" />
      <NuxtLink to="/" class="text-emerald-700 font-extrabold text-2xl hover:text-emerald-600 transition">
        Hospital Room
      </NuxtLink>
    </div>

    <div class="space-x-4">
      <NuxtLink
        to="/login"
        class="text-gray-600 hover:text-emerald-600 font-medium transition duration-200"
      >เข้าสู่ระบบ</NuxtLink>

      <NuxtLink
        to="/dashboard"
        class="text-gray-600 hover:text-emerald-600 font-medium transition duration-200"
      >แดชบอร์ด</NuxtLink>

      <NuxtLink
        to="/medicine"
        class="text-gray-600 hover:text-emerald-600 font-medium transition duration-200"
      >ยา</NuxtLink>

      <NuxtLink
        to="/student"
        class="text-gray-600 hover:text-emerald-600 font-medium transition duration-200"
      >นักเรียน</NuxtLink>

      <NuxtLink
        to="/treatment"
        class="text-gray-600 hover:text-emerald-600 font-medium transition duration-200"
      >การรักษา</NuxtLink>
    </div>
  </nav>
</template>

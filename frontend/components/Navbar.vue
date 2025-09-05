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
      >Login</NuxtLink>

      <NuxtLink
        to="/dashboard"
        class="text-gray-600 hover:text-emerald-600 font-medium transition duration-200"
      >Dashboard</NuxtLink>

      <NuxtLink
        to="/medicine"
        class="text-gray-600 hover:text-emerald-600 font-medium transition duration-200"
      >medicine</NuxtLink>

      <NuxtLink
        to="/treatment"
        class="text-gray-600 hover:text-emerald-600 font-medium transition duration-200"
      >treatment</NuxtLink>

      <NuxtLink to="/students"
      class="text-gray-600 hover:text-emerald-600 font-medium transition duration-200"
      >studens</NuxtLink>

      <!-- ✅ เพิ่มปุ่มค้นหาใบเสร็จ -->
      <NuxtLink
        to="/search-receipt"
        class="text-gray-600 hover:text-emerald-600 font-medium transition duration-200"
      >ค้นหาใบเสร็จ</NuxtLink>
      <NuxtLink
        to="/about"
        class="text-gray-600 hover:text-emerald-600 font-medium transition duration-200"
      >About</NuxtLink>
    </div>
  </nav>
</template>
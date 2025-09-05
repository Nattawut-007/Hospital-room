<template>
  <div class="min-h-screen bg-gradient-to-tr from-emerald-100 via-blue-100 to-indigo-100 pt-12 pb-8 px-8 flex justify-center items-start">
    <div class="bg-white/90 backdrop-blur-md rounded-2xl shadow-2xl p-10 w-full max-w-6xl transition-all duration-300 hover:shadow-emerald-300">
      <h1 class="text-3xl font-bold text-emerald-700 text-center mb-8">ทีมพัฒนา</h1>

      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-8">
        <div
          v-for="(member, index) in team"
          :key="index"
          class="bg-white rounded-xl shadow-md p-6 flex flex-col items-center transition hover:scale-105 hover:shadow-emerald-400"
        >
          <img
            :src="member.image"
            alt="profile"
            class="w-40 h-40 object-cover mb-4 rounded-xl border-4 border-emerald-200"
          />
          <h2 class="text-lg font-semibold text-gray-700">{{ member.name }}</h2>
          <p class="text-sm text-gray-500">{{ member.role }}</p>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
const team = [
  {
    name: 'Pond',
    role: 'Backend Developer',
    image: 'https://media.discordapp.net/attachments/1032668625905143809/1413441117705207838/att.rZVh63iZSk4UKdI9jALGItLcqAjC98ZIPvt44AguVds.jpg?ex=68bbf11e&is=68ba9f9e&hm=ee45887fb6de05883dff8f0314cc003cc1de0ae33d3e663937a330b45ed2cd1b&=&format=webp&width=800&height=800',
  },
  {
    name: 'Boat',
    role: 'Backend Developer',
    image: 'https://media.discordapp.net/attachments/1032668625905143809/1413443406465859655/8c83e940ed093cbdd782b4c2c8951261.jpg?ex=68bbf340&is=68baa1c0&hm=f8b6a8818ac734a76babd1177656d59654aa55d050f08042dd4ca2b98a9a1f97&=&format=webp&width=930&height=930',
  },
  {
    name: 'Job',
    role: 'Frontend Developer',
    image: 'https://media.discordapp.net/attachments/1032668625905143809/1413441117952802858/att.fYOJ1vEqaJaVZzPjC382wicH7-eJxdQqxy0gEytrCmg.jpg?ex=68bbf11e&is=68ba9f9e&hm=f13e60aea239dafc3a638daf6f1f74cbf6beed6f451fbcec39e68833faf64120&=&format=webp&width=800&height=800',
  },
  {
    name: 'Kim',
    role: 'Frontend Developer',
    image: 'https://media.discordapp.net/attachments/1032668625905143809/1413441118200139856/IMG_9520.png?ex=68bbf11f&is=68ba9f9f&hm=6b0dfca58737684daab985bf0d7e325a9eb44da5f3dd8e3fd428128803213a83&=&format=webp&quality=lossless&width=568&height=568',
  },
]
</script>

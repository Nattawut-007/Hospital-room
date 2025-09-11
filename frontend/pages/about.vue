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
    name: 'ณัฐวุฒิ จันทิหล้า (ป้อน)',
    role: 'Backend Developer',
    image: 'https://media.discordapp.net/attachments/1032668625905143809/1415676607888232508/att.rZVh63iZSk4UKdI9jALGItLcqAjC98ZIPvt44AguVds.jpg?ex=68c41315&is=68c2c195&hm=c0c766b192866ad5a8f87147015ce1407556a36a418ca75d7c5549e742a52e2e&=&format=webp&width=800&height=800',
  },
  {
    name: 'บารมี แคภูเขียว (โบ๊ท)',
    role: 'Backend Developer',
    image: 'https://media.discordapp.net/attachments/1032668625905143809/1415676608425230476/8c83e940ed093cbdd782b4c2c8951261.jpg?ex=68c41315&is=68c2c195&hm=e16e6f12a31f9aa210de7521d6fad54e6def0606196732d2d826c367914d6882&=&format=webp&width=800&height=800',
  },
  {
    name: 'นัฐวุฒน์ อุทธตรี (จ๊อบ)',
    role: 'Frontend Developer',
    image: 'https://media.discordapp.net/attachments/1032668625905143809/1415676602091573248/att.fYOJ1vEqaJaVZzPjC382wicH7-eJxdQqxy0gEytrCmg.jpg?ex=68c41313&is=68c2c193&hm=ac03f452ded4cc313473a5e099cb553e036f4d5bc4299892d752589ec0f2c7d7&=&format=webp&width=800&height=800',
  },
  {
    name: 'คิมหันต์ ละดาห์ (คิม)',
    role: 'Frontend Developer',
    image: 'https://media.discordapp.net/attachments/1032668625905143809/1415676601399775262/IMG_9520.png?ex=68c41313&is=68c2c193&hm=d38891e4f1c472ae78672fee53e8aa6f3e8d328f866094ebe38f059455612ed6&=&format=webp&quality=lossless&width=568&height=568',
  },
]
</script>
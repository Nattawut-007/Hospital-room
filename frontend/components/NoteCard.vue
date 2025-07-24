<template>
  <div class="bg-white p-4 shadow rounded mb-3">
    <h2 class="font-bold">{{ note.title }}</h2>
    <p class="text-sm text-gray-600">{{ note.content }}</p>
    <p class="text-xs text-right">{{ note.created_at }}</p>
    <button @click="$emit('delete', note.id)" class="text-red-500 text-sm mt-2">Delete</button>
  </div>
</template>

<script setup>
defineProps({ note: Object })
defineEmits(['delete'])
</script>

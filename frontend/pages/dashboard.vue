<template>
  <div class="min-h-screen bg-gradient-to-br from-cyan-50 via-emerald-50 to-white p-6">
    <div class="max-w-5xl mx-auto">
      <h1 class="text-4xl font-bold text-center text-emerald-700 mb-10">🏥 Hospital Dashboard</h1>

      <!-- Add Button -->
      <div class="text-right mb-4">
        <button
          @click="openModal()"
          class="bg-emerald-500 hover:bg-emerald-600 text-white px-4 py-2 rounded-xl shadow"
        >
          ➕ Add Note
        </button>
      </div>

      <!-- Card Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div
          class="bg-white shadow-lg border border-emerald-200 rounded-2xl p-6 relative"
          v-for="note in notes"
          :key="note.id"
        >
          <h2 class="text-xl font-semibold text-emerald-700 mb-2">📋 {{ note.title }}</h2>
          <p class="text-gray-600 text-sm mb-4">{{ note.content }}</p>

          <div class="absolute top-3 right-3 flex gap-2">
            <button
              @click="openModal(note)"
              class="text-blue-500 hover:text-blue-700"
              title="Edit"
            >✏️</button>
            <button
              @click="deleteNote(note.id)"
              class="text-red-500 hover:text-red-700"
              title="Delete"
            >🗑️</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black/40 flex justify-center items-center z-50">
      <div class="bg-white p-6 rounded-xl w-full max-w-md shadow-lg border">
        <h2 class="text-2xl font-bold mb-4 text-emerald-600">
          {{ isEditing ? 'Edit Note' : 'Add Note' }}
        </h2>
        <input
          v-model="form.title"
          placeholder="Title"
          class="w-full border p-3 rounded-lg mb-3"
        />
        <textarea
          v-model="form.content"
          placeholder="Content"
          class="w-full border p-3 rounded-lg mb-3"
        />
        <div class="flex justify-end gap-2">
          <button
            @click="closeModal"
            class="bg-gray-300 hover:bg-gray-400 text-black px-4 py-2 rounded-lg"
          >Cancel</button>
          <button
            @click="isEditing ? updateNote() : createNote()"
            class="bg-emerald-500 hover:bg-emerald-600 text-white px-4 py-2 rounded-lg"
          >
            {{ isEditing ? 'Update' : 'Save' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const notes = ref([])
const showModal = ref(false)
const isEditing = ref(false)
const editId = ref(null)
const form = ref({ title: '', content: '' })

// Load from localStorage
onMounted(() => {
  const saved = localStorage.getItem('hospital_notes')
  if (saved) notes.value = JSON.parse(saved)
})

// Save to localStorage whenever notes change
watch(notes, (newNotes) => {
  localStorage.setItem('hospital_notes', JSON.stringify(newNotes))
}, { deep: true })

const openModal = (note = null) => {
  showModal.value = true
  if (note) {
    isEditing.value = true
    editId.value = note.id
    form.value = { title: note.title, content: note.content }
  } else {
    isEditing.value = false
    editId.value = null
    form.value = { title: '', content: '' }
  }
}

const closeModal = () => {
  showModal.value = false
  isEditing.value = false
  editId.value = null
  form.value = { title: '', content: '' }
}

const createNote = () => {
  if (!form.value.title.trim() || !form.value.content.trim()) return
  const newNote = {
    id: Date.now(),
    title: form.value.title,
    content: form.value.content
  }
  notes.value.unshift(newNote)
  closeModal()
}

const updateNote = () => {
  const index = notes.value.findIndex(n => n.id === editId.value)
  if (index !== -1) {
    notes.value[index].title = form.value.title
    notes.value[index].content = form.value.content
  }
  closeModal()
}

const deleteNote = (id) => {
  notes.value = notes.value.filter(n => n.id !== id)
}
</script>

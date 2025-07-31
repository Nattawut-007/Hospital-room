<template>
  <div class="p-6 max-w-3xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">My Medicine Tracker</h1>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
      <input v-model="medicineName" placeholder="Medicine Name" class="border p-2" />
      <input v-model="dosage" placeholder="Dosage (e.g., 500mg, 1 tablet)" class="border p-2" />
      <input v-model="frequency" placeholder="Frequency (e.g., Daily, Every 4 hrs)" class="border p-2" />
      <input v-model="instructions" placeholder="Instructions (e.g., With food)" class="border p-2" />
      <input v-model="quantity" type="number" placeholder="Quantity (e.g., 30)" class="border p-2" />
      <input v-model="startDate" type="date" placeholder="Start Date" class="border p-2" />
      <input v-model="endDate" type="date" placeholder="End Date (Optional)" class="border p-2" />
      <button @click="addMedicine" class="bg-green-500 text-white p-2 col-span-full">Add Medicine</button>
    </div>

    <MedicineCard
      v-for="medicine in medicines"
      :key="medicine.id"
      :medicine="medicine"
      @delete="deleteMedicine"
      @update="updateMedicine"
    />
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
// You would create a new component called MedicineCard
// import MedicineCard from './MedicineCard.vue'

const medicineName = ref('')
const dosage = ref('')
const frequency = ref('')
const instructions = ref('')
const quantity = ref(null) // Using null for initial number input
const startDate = ref('')
const endDate = ref('')

const medicines = ref([])

const fetchMedicines = async () => {
  const token = localStorage.getItem('token')
  try {
    const res = await axios.get('http://localhost:5000/api/medicines', { // Changed endpoint
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    medicines.value = res.data
  } catch (e) {
    console.error('Failed to fetch medicines:', e)
  }
}

const addMedicine = async () => {
  const token = localStorage.getItem('token')
  try {
    await axios.post('http://localhost:5000/api/medicines', { // Changed endpoint
      name: medicineName.value,
      dosage: dosage.value,
      frequency: frequency.value,
      instructions: instructions.value,
      quantity: quantity.value,
      startDate: startDate.value,
      endDate: endDate.value
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    // Clear inputs
    medicineName.value = ''
    dosage.value = ''
    frequency.value = ''
    instructions.value = ''
    quantity.value = null
    startDate.value = ''
    endDate.value = ''
    fetchMedicines() // Refresh the list
  } catch (e) {
    console.error('Failed to add medicine:', e)
  }
}

const deleteMedicine = async (id) => {
  const token = localStorage.getItem('token')
  try {
    await axios.delete(`http://localhost:5000/api/medicines/${id}`, { // Changed endpoint
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    fetchMedicines() // Refresh the list
  } catch (e) {
    console.error('Failed to delete medicine:', e)
  }
}

// You would also want an update function for editing medicine details
const updateMedicine = async (medicineToUpdate) => {
  const token = localStorage.getItem('token')
  try {
    await axios.put(`http://localhost:5000/api/medicines/${medicineToUpdate.id}`, medicineToUpdate, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    fetchMedicines() // Refresh the list
  } catch (e) {
    console.error('Failed to update medicine:', e)
  }
}

onMounted(fetchMedicines)
</script>
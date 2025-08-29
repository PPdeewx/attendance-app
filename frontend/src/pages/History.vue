<template>
  <div class="min-h-screen bg-gray-100">
    <Navbar />
    <div class="p-8 max-w-6xl mx-auto">
      <h1 class="text-2xl font-bold mb-6 text-gray-800">ประวัติการลงเวลา</h1>
      <input placeholder="Search..." class="w-full p-3 mb-4 border rounded focus:ring-2 focus:ring-blue-400 transition">
      <div class="overflow-x-auto rounded-3xl shadow-xl bg-white">
        <table class="min-w-full border-collapse">
          <thead class="bg-gray-200">
            <tr>
              <th class="border px-6 py-4 text-left text-gray-700">เวลา</th>
              <th class="border px-6 py-4 text-left text-gray-700">สถานที่</th>
              <th class="border px-6 py-4 text-left text-gray-700">ประเภทเวลา</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="log in logs" :key="log.id" :class="{'bg-gray-50': log.id % 2 === 0, 'hover:bg-gray-100': true}" class="transition transform hover:scale-101">
              <td class="border px-6 py-4">{{ new Date(log.timestamp).toLocaleString() }}</td>
              <td class="border px-6 py-4">{{ log.location.name }}</td>
              <td class="border px-6 py-4 capitalize">{{ log.time_type }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Navbar from '../components/Navbar.vue'

const logs = ref([])
const token = localStorage.getItem('token')

onMounted(() => {
  axios.get('http://localhost:8000/api/check-in/', { headers: { Authorization: `Token ${token}` }})
    .then(res => logs.value = res.data)
})
</script>

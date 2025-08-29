<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-100 to-blue-300">
    <div class="bg-white p-8 rounded-3xl shadow-2xl w-full max-w-md transform hover:scale-105 transition duration-300 border border-gray-200">
      <h1 class="text-4xl font-bold mb-6 text-center text-blue-700">Login</h1>
      <div class="space-y-6">
        <div class="relative">
          <input v-model="username" placeholder="Username" class="w-full p-4 border rounded mb-4 focus:ring-2 focus:ring-blue-400 focus:outline-none transition pl-10"/>
          <svg class="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
          </svg>
        </div>
        <div class="relative">
          <input v-model="password" type="password" placeholder="Password" class="w-full p-4 border rounded mb-6 focus:ring-2 focus:ring-blue-400 focus:outline-none transition pl-10"/>
          <svg class="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 11c1.38 0 2.5-1.12 2.5-2.5S13.38 6 12 6s-2.5 1.12-2.5 2.5S10.62 11 12 11zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5z"/>
          </svg>
        </div>
        <button @click="login" class="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-600 text-white py-3 rounded font-semibold shadow-lg transition transform hover:scale-105">Login</button>
      </div>
      <p v-if="error" class="text-red-500 mt-4 text-center">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

const login = () => {
  axios.post('http://localhost:8000/api/login/', {
    username: username.value,
    password: password.value
  }).then(res => {
    localStorage.setItem('token', res.data.token)
    router.push('/attendance')
  }).catch(() => error.value = 'Login failed')
}
</script>
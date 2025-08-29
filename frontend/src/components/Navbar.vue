<template>
  <nav class="bg-gradient-to-r from-blue-600 to-blue-500 text-white p-4 flex flex-col md:flex-row justify-between items-center shadow-lg rounded-b-2xl">
    <div class="font-bold text-2xl mb-2 md:mb-0 flex items-center space-x-2">
      <span>Attendance App</span>
    </div>
    <div class="flex flex-col md:flex-row md:space-x-4 space-y-2 md:space-y-0">
      <button @click="go('/attendance')" class="hover:bg-blue-400 px-4 py-2 rounded shadow transition duration-200">ลงเวลา</button>
      <button @click="go('/history')" class="hover:bg-blue-400 px-4 py-2 rounded shadow transition duration-200">ประวัติ</button>
      <button @click="go('/faceregister')" class="hover:bg-blue-400 px-4 py-2 rounded shadow transition duration-200">ลงทะเบียนใบหน้า</button>
      <button @click="logout" class="hover:bg-blue-400 px-4 py-2 rounded shadow transition duration-200">Logout</button>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
const go = (path) => router.push(path)
const logout = () => {
  localStorage.removeItem('token')
  router.push('/')
}
</script>

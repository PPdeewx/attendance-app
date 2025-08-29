<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-100 to-gray-200">
    <Navbar />
    <div class="flex flex-col items-center p-8">
      <h1 class="text-3xl font-bold mb-8 text-gray-800">ลงทะเบียนใบหน้า</h1>

      <div class="bg-white p-10 rounded-3xl shadow-2xl w-full max-w-md space-y-8 border border-gray-200">
        <!-- กล้อง + Canvas -->
        <div class="flex flex-col items-center space-y-4">
          <div class="w-48 h-48 overflow-hidden rounded-full border-4 border-blue-200 shadow-lg relative">
            <video ref="video" autoplay class="w-full h-full object-cover"></video>
            <canvas ref="canvas" class="hidden"></canvas>
          </div>
        </div>

        <!-- ปุ่มลงทะเบียน -->
        <button @click="registerFace" class="w-full bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-500 text-white py-3 rounded-lg font-semibold shadow-lg transition transform hover:scale-105">
          ลงทะเบียนใบหน้า
        </button>

        <!-- ข้อความแจ้งผล -->
        <p v-if="message" class="mt-3 text-center text-red-500 font-medium">{{ message }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Navbar from '../components/Navbar.vue'

const video = ref(null)
const canvas = ref(null)
const message = ref('')
const token = localStorage.getItem('token')

// เปิดกล้อง
onMounted(() => {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => { video.value.srcObject = stream })
    .catch(err => message.value = 'ไม่สามารถเข้าถึงกล้องได้')
})

// ถ่ายรูปจาก Video
const takeSnapshot = () => {
  const ctx = canvas.value.getContext('2d')
  canvas.value.width = video.value.videoWidth
  canvas.value.height = video.value.videoHeight
  ctx.drawImage(video.value, 0, 0, canvas.value.width, canvas.value.height)
  return new Promise(resolve => {
    canvas.value.toBlob(blob => resolve(blob), 'image/jpeg')
  })
}

// ฟังก์ชันลงทะเบียนใบหน้า
const registerFace = async () => {
  try {
    const blob = await takeSnapshot()
    const form = new FormData()
    form.append('image', blob)

    const res = await axios.post('http://localhost:8000/api/face-register/', form, {
      headers: { Authorization: `Token ${token}`, 'Content-Type': 'multipart/form-data' }
    })

    message.value = res.data.status || 'ลงทะเบียนสำเร็จ ✅'
  } catch(err) {
    message.value = err.response?.data?.error || 'เกิดข้อผิดพลาด'
  }
}
</script>

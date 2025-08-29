<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-100 to-gray-200">
    <Navbar />
    <div class="flex flex-col items-center p-8">
      <h1 class="text-3xl font-bold mb-8 text-gray-800">ลงเวลาทำงาน</h1>
      <div class="bg-white p-10 rounded-3xl shadow-2xl w-full max-w-md space-y-8 transform hover:scale-102 transition duration-300 border border-gray-200">
        
        <!-- เลือก Action -->
        <div>
          <label class="block mb-2 font-semibold text-gray-700">Action</label>
          <select v-model="action" class="w-full border rounded p-3 focus:ring-2 focus:ring-blue-400">
            <option value="in">เข้า</option>
            <option value="out">ออก</option>
          </select>
        </div>

        <!-- เลือก TimeType -->
        <div>
          <label class="block mb-2 font-semibold text-gray-700">เลือกเวลา</label>
          <select v-model="timeType" class="w-full border rounded p-3 focus:ring-2 focus:ring-blue-400 transition bg-white">
            <option value="morning">เช้า</option>
            <option value="noon">กลางวัน</option>
            <option value="afternoon">บ่าย</option>
            <option value="evening">เย็น</option>
          </select>
        </div>

        <!-- เลือก Location -->
        <div>
          <label class="block mb-2 font-semibold text-gray-700">เลือกสถานที่</label>
          <select v-model="locationId" class="w-full border rounded p-3 focus:ring-2 focus:ring-blue-400 transition bg-white">
            <option v-for="loc in locations" :key="loc.id" :value="loc.id">{{ loc.name }}</option>
          </select>
        </div>

        <!-- กล้อง + Canvas -->
        <div class="flex flex-col items-center space-y-4">
          <div class="w-48 h-48 overflow-hidden rounded-full border-4 border-blue-200 shadow-lg relative">
            <video ref="video" autoplay class="w-full h-full object-cover"></video>
            <canvas ref="canvas" class="hidden"></canvas>
          </div>
        </div>

        <!-- ปุ่มลงเวลา + สแกนหน้า -->
        <button @click="checkInWithFace" class="w-full bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-500 text-white py-3 rounded-lg font-semibold shadow-lg transition transform hover:scale-105">
          สแกนหน้า & ลงเวลา
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

const action = ref('in')
const timeType = ref('morning')
const locationId = ref(null)
const locations = ref([])
const message = ref('')
const token = localStorage.getItem('token')

const video = ref(null)
const canvas = ref(null)

onMounted(() => {
  // ดึงสถานที่
  axios.get('http://localhost:8000/api/locations/', { headers: { Authorization: `Token ${token}` }})
    .then(res => locations.value = res.data)
    .catch(() => message.value = 'ไม่สามารถโหลดสถานที่ได้')

  // เปิดกล้อง
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => { video.value.srcObject = stream })
    .catch(() => message.value = 'ไม่สามารถเข้าถึงกล้องได้')
})

// ฟังก์ชันถ่ายรูปจาก Video
const takeSnapshot = () => {
  const ctx = canvas.value.getContext('2d')
  canvas.value.width = video.value.videoWidth
  canvas.value.height = video.value.videoHeight
  ctx.drawImage(video.value, 0, 0, canvas.value.width, canvas.value.height)
  return new Promise(resolve => {
    canvas.value.toBlob(blob => resolve(blob), 'image/jpeg')
  })
}

// ฟังก์ชันสแกนหน้า + ลงเวลา
const checkInWithFace = async () => {
  if (!locationId.value) { message.value = 'กรุณาเลือกสถานที่'; return }

  navigator.geolocation.getCurrentPosition(async pos => {
    try {
      message.value = 'กำลังสแกนใบหน้า...'

      // 1️⃣ ถ่ายรูปและส่งไป backend
      const blob = await takeSnapshot()
      const faceForm = new FormData()
      faceForm.append('image', blob)

      const faceRes = await axios.post('http://localhost:8000/api/face-checkin/', faceForm, {
        headers: { Authorization: `Token ${token}`, 'Content-Type': 'multipart/form-data' }
      })

      if (faceRes.data.error) {
        message.value = faceRes.data.error
        return
      }

      // 2️⃣ ส่ง check-in พร้อมระบุ face_verified = true
      await axios.post('http://localhost:8000/api/check-in/', {
        time_type: timeType.value,
        location: locationId.value,
        latitude: pos.coords.latitude,
        longitude: pos.coords.longitude,
        action: action.value,
        face_verified: true
      }, { headers: { Authorization: `Token ${token}` } })

      message.value = 'บันทึกสำเร็จ พร้อมยืนยันใบหน้า ✅'
    } catch(err) {
      message.value = err.response?.data?.error || 'เกิดข้อผิดพลาดในการสแกนหน้า'
    }
  }, () => message.value = 'ไม่สามารถเข้าถึงตำแหน่ง GPS ได้')
}
</script>

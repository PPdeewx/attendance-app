import { createRouter, createWebHistory } from 'vue-router'
import Login from '../pages/Login.vue'
import Attendance from '../pages/Attendance.vue'
import History from '../pages/History.vue'
import FaceRegister from '../pages/FaceRegister.vue'

const routes = [
  { path: '/', component: Login },
  { path: '/attendance', component: Attendance },
  { path: '/history', component: History },
  { path: '/faceregister', component: FaceRegister }
]

export default createRouter({
  history: createWebHistory(),
  routes
})

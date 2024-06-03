import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomeView.vue')
  },
    {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/RegisterView.vue')
  },
    {
    path: '/query',
    name: 'query',
    component: () => import('../views/QueryView.vue')
  },
    {
    path: '/database',
    name: 'database',
    component: () => import('../views/DatabaseView.vue')
  },
    {
    path: '/user',
    name: 'user',
    component: () => import('../views/UserView.vue')
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router

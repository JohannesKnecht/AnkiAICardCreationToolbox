import { createRouter, createWebHistory } from 'vue-router'
import OverviewView from '../views/OverviewView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: OverviewView,
    },
    {
      path: '/Image2LaTeX',
      name: 'Image2LaTeX',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/Image2LaTeX.vue'),
    },
    {
      path: '/CardCreation',
      name: 'CardCreation',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/CardCreation.vue'),
    },
  ],
})

export default router

import { createRouter, createWebHistory } from 'vue-router'
import RecipesView from '../views/RecipesView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'recipes',
      component: RecipesView,
    },
    {
      path: '/add',
      name: 'add-recipe',
      component: RecipesView, // Pops up RecipeForm modal when routed here
    }
  ],
})

export default router

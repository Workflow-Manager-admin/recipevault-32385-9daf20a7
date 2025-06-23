<template>
  <div>
    <div v-if="!recipes.length" class="empty-list">
      <div class="no-recipes">No recipes found.</div>
    </div>
    <div v-else>
      <div v-for="recipe in recipes" :key="recipe.id" class="wrap">
        <RecipeCard
          :recipe="recipe"
          :editable="!!isOwner(recipe.user_id)"
          :showFavorite="true"
          @view="$emit('view', recipe)"
          @edit="$emit('edit', recipe)"
          @delete="$emit('delete', recipe)"
          @toggleFavorite="toggleFavorite"
        />
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import RecipeCard from './RecipeCard.vue'
import { useUserStore } from '../stores/user'
import { defineProps, defineEmits } from 'vue'

interface Recipe {
  id: number
  user_id?: number
  title: string
  description?: string
  cuisine?: string
  tags?: string[]
  time?: number
  favorite?: boolean
}

defineProps<{ recipes: Recipe[] }>()
const emit = defineEmits(['view', 'edit', 'delete', 'toggleFavorite'])
const userStore = useUserStore()
function isOwner(userId: number|undefined) {
  return userStore.user && userId === userStore.user.id
}
function toggleFavorite(recipe: Recipe) {
  emit('toggleFavorite', recipe)
}
</script>
<style scoped>
.wrap {
  margin-bottom: 1.6em;
}
.empty-list {
  text-align: center;
  color: #999;
}
.no-recipes {
  margin-top: 2.5em;
  font-size: 1.13em;
  color: #888;
}
</style>

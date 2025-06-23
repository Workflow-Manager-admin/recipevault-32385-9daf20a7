<template>
  <div class="detail-view" v-if="recipe">
    <h1>{{ recipe.title }}</h1>
    <div class="meta">
      <span v-if="recipe.cuisine" class="meta-chip accent">{{ recipe.cuisine }}</span>
      <span v-for="tag in recipe.tags" :key="tag" class="meta-chip">{{ tag }}</span>
      <span v-if="recipe.time" class="meta-chip">{{ recipe.time }} min</span>
      <span class="meta-right" v-if="recipe.favorite">&#9733; Favorite</span>
    </div>
    <div class="author">By {{ recipe.author || 'Unknown' }}</div>
    <p class="desc">{{ recipe.description }}</p>
    <div class="section">
      <h2>Ingredients</h2>
      <ul>
        <li v-for="(ingredient, i) in recipe.ingredients" :key="i">{{ ingredient }}</li>
      </ul>
    </div>
    <div class="section">
      <h2>Instructions</h2>
      <ol>
        <li v-for="(step, i) in recipe.instructions" :key="i">{{ step }}</li>
      </ol>
    </div>
    <div class="actions">
      <button class="secondary" @click="$emit('close')">Close</button>
      <button v-if="editable" class="primary" @click="$emit('edit', recipe)">Edit</button>
      <button v-if="editable" class="accent" @click="$emit('delete', recipe)">Delete</button>
    </div>
  </div>
</template>
<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'

interface Recipe {
  id: number
  title: string
  cuisine?: string
  tags?: string[]
  time?: number
  favorite?: boolean
  ingredients?: string[]
  instructions?: string[]
  description?: string
  author?: string
  user_id?: number
}

defineProps<{ recipe: Recipe, editable?: boolean }>()
defineEmits(['close', 'edit', 'delete'])
</script>
<style scoped>
.detail-view {
  background: #fff;
  border-radius: 11px;
  box-shadow: 0 2px 12px #0002;
  padding: 2rem 2.3rem 1.5rem 2.3rem;
  max-width: 720px;
  margin: 2em auto;
}
h1 {
  color: #4caf50;
  font-size: 2em;
  margin-bottom: 0.4em;
}
.meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.7em;
  align-items: center;
  margin-bottom: 0.9em;
}
.meta-chip {
  background: #e8f5e9;
  color: #4caf50;
  border-radius: 8px;
  padding: 0.08em 0.7em;
  font-size: 0.98em;
}
.meta-chip.accent {
  background: #ff980018;
  color: #ff9800;
}
.meta-right {
  margin-left: auto;
  color: #ff9800;
  font-weight: bold;
}
.author {
  color: #9e9e9e;
  font-size: 1.07em;
  margin-bottom: 1.2em;
}
.desc {
  margin-bottom: 1.2em;
  font-size: 1.17em;
}
.section {
  margin-top: 1.2em;
  margin-bottom: 1.3em;
}
.actions {
  display: flex;
  gap: 0.65em;
  margin-top: 1.5em;
}
button {
  font: inherit;
  padding: 0.45em 1.2em;
  border-radius: 3px;
  border: none;
  cursor: pointer;
  background: #f6f8f7;
  color: #333;
  margin-left: 0;
  transition: background .17s, color .17s;
}
button.primary { background: #4caf50; color: white; }
button.secondary { background: #8bc34a; color: #fff;}
button.accent { background: #ff9800; color: #fff;}
</style>

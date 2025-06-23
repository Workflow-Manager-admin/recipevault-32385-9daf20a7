<template>
  <div class="card" :class="{ favorite: recipe.favorite }">
    <div class="card-header">
      <h3>{{ recipe.title }}</h3>
      <button v-if="showFavorite" class="star"
        :title="recipe.favorite ? 'Unfavorite' : 'Favorite'"
        @click.stop="toggleFavorite">
        <span v-if="recipe.favorite">&#9733;</span>
        <span v-else>&#9734;</span>
      </button>
    </div>
    <div class="meta">
      <span v-if="recipe.cuisine" class="meta-chip accent">{{ recipe.cuisine }}</span>
      <span v-for="tag in recipe.tags" :key="tag" class="meta-chip">{{ tag }}</span>
      <span v-if="recipe.time" class="meta-chip">{{ recipe.time }} min</span>
    </div>
    <p class="desc">{{ recipe.description }}</p>
    <div class="actions">
      <button class="secondary" @click="$emit('view', recipe)">View</button>
      <button class="primary" v-if="editable" @click="$emit('edit', recipe)">Edit</button>
      <button class="accent" v-if="editable" @click="$emit('delete', recipe)">Delete</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'
const props = defineProps<{
  recipe: {
    id: number, title: string, description?: string, cuisine?: string,
    tags?: string[], time?: number, favorite?: boolean
  },
  editable?: boolean,
  showFavorite?: boolean
}>()
const emit = defineEmits(['view', 'edit', 'delete', 'toggleFavorite'])
function toggleFavorite() {
  emit('toggleFavorite', props.recipe)
}
</script>

<style scoped>
.card {
  background: #fff;
  border: 1.5px solid #eee;
  box-shadow: 0 2px 10px #0001;
  margin-bottom: 1.5em;
  border-radius: 11px;
  padding: 1.2em 1.3em 0.95em 1.3em;
  position: relative;
  min-width: 260px;
}
.card.favorite {
  border-color: #ff9800ac;
  box-shadow: 0 4px 16px #ff98003b;
}
.card-header {
  display: flex;
  align-items: center;
  gap: 0.6em;
  justify-content: space-between;
}
h3 {
  font-size: 1.25em;
  color: #181818;
}
.star {
  background: none;
  border: none;
  font-size: 1.4em;
  color: #ff9800;
  cursor: pointer;
}
.meta {
  margin: 0.5em 0 0.7em 0;
  display: flex;
  gap: 0.5em;
  flex-wrap: wrap;
}
.meta-chip {
  background: #e8f5e9;
  color: #4caf50;
  border-radius: 8px;
  padding: 0.08em 0.7em;
  font-size: 0.95em;
}
.meta-chip.accent {
  background: #ff980018;
  color: #ff9800;
}
.desc {
  min-height: 1.7em;
  margin: 0.5em 0 0.7em 0;
  color: #222;
  font-size: 1.1em;
}
.actions {
  display: flex;
  gap: 0.45em;
}
button {
  font: inherit;
  padding: 0.32em 0.85em;
  margin-left: 0;
  border-radius: 3px;
  border: none;
  cursor: pointer;
  background: #f6f8f7;
  color: #333;
  transition: background .17s, color .17s;
}
button.primary { background: #4caf50; color: white; }
button.secondary { background: #8bc34a; color: #fff;}
button.accent { background: #ff9800; color: #fff;}
</style>

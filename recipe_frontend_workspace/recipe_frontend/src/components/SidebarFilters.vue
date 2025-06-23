<template>
  <aside class="sidebar">
    <h2>Filters</h2>
    <input v-model="query" type="text" placeholder="Search recipes..." @input="emitFilter" />
    <div>
      <label>
        <input type="checkbox" v-model="favoritesOnly" @change="emitFilter" />
        Favorites
      </label>
    </div>
    <div v-if="tags && tags.length">
      <h3>Tags</h3>
      <div class="tag-list">
        <span v-for="tag in tags" :key="tag" @click="toggleTag(tag)"
              :class="[{ selected: activeTags.includes(tag) }, 'tag']">
          {{ tag }}
        </span>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { ref, defineEmits, defineProps } from 'vue'

defineProps<{ tags?: string[] }>()
const emit = defineEmits(['filter'])
const query = ref('')
const favoritesOnly = ref(false)
const activeTags = ref<string[]>([])
function emitFilter() {
  emit('filter', { query: query.value, favoritesOnly: favoritesOnly.value, tags: [...activeTags.value] })
}
function toggleTag(tag: string) {
  const i = activeTags.value.indexOf(tag)
  if (i >= 0) activeTags.value.splice(i, 1)
  else activeTags.value.push(tag)
  emitFilter()
}
</script>

<style scoped>
.sidebar {
  width: 240px;
  background: #fafbfc;
  border-right: 1.5px solid #ededed;
  padding: 2rem 1.5rem;
  min-height: 80vh;
}
h2 {
  margin-bottom: 1.15rem;
  color: #4caf50;
}
input[type="text"] {
  padding: 0.5em;
  width: 100%;
  border: 1.5px solid #ddd;
  border-radius: 3px;
  margin-bottom: 1.1em;
  font-size: 1em;
}
.tag-list {
  margin-top: 0.7rem;
  display: flex;
  flex-wrap: wrap;
  gap: .45em;
}
.tag {
  background: #e8f5e9;
  color: #4caf50;
  padding: 0.25em 0.8em;
  border-radius: 16px;
  font-size: 0.93em;
  cursor: pointer;
  border: 1px solid #4caf5085;
  transition: background .18s, color .18s;
  user-select: none;
}
.tag.selected {
  background: #4caf50;
  color: white;
  border-color: #388e3c;
}
</style>

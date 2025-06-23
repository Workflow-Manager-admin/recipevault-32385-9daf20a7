<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal">
      <h2>{{ editing ? "Edit Recipe" : "Add Recipe" }}</h2>
      <form @submit.prevent="submit">
        <label>
          Title
          <input v-model="form.title" required maxlength="60" />
        </label>
        <label>
          Cuisine
          <input v-model="form.cuisine" maxlength="32" />
        </label>
        <label>
          Time (min)
          <input type="number" v-model.number="form.time" min="1" max="999" />
        </label>
        <label>
          Description
          <textarea v-model="form.description" rows="2" maxlength="160"></textarea>
        </label>
        <label>
          Tags (comma separated)
          <input v-model="tagsString" placeholder="e.g. vegan, dessert" />
        </label>
        <label>
          Ingredients (one per line)
          <textarea v-model="ingredientsString" rows="4" required></textarea>
        </label>
        <label>
          Instructions (one per line or step)
          <textarea v-model="instructionsString" rows="6" required></textarea>
        </label>
        <div class="actions">
          <button class="secondary" type="button" @click="$emit('close')">Cancel</button>
          <button class="primary" type="submit">{{ editing ? 'Update' : 'Add' }}</button>
        </div>
      </form>
    </div>
  </div>
</template>
<script setup lang="ts">
import { defineProps, defineEmits, ref, watch } from 'vue'
interface Recipe {
  id?: number
  title: string
  cuisine?: string
  time?: number | string
  description?: string
  tags?: string[]
  ingredients?: string[]
  instructions?: string[]
  user_id?: number
}

const props = defineProps<{ value?: Recipe, editing?: boolean }>()
const emit = defineEmits(['close', 'submit'])

const blank: Recipe = { title: '', cuisine: '', time: '', description: '', tags: [], ingredients: [], instructions: [] }
const form = ref<Recipe>({ ...blank, ...(props.value || {}) })
const tagsString = ref(form.value.tags?.join(', ') || '')
const ingredientsString = ref((form.value.ingredients || []).join('\n'))
const instructionsString = ref((form.value.instructions || []).join('\n'))

watch(() => props.value, (val) => {
  Object.assign(form.value, blank, val || {})
  tagsString.value = form.value.tags?.join(', ') || ''
  ingredientsString.value = (form.value.ingredients || []).join('\n')
  instructionsString.value = (form.value.instructions || []).join('\n')
})

function submit() {
  form.value.tags = tagsString.value.split(',').map((t: string) => t.trim()).filter(Boolean)
  form.value.ingredients = ingredientsString.value.split('\n').map((i: string) => i.trim()).filter(Boolean)
  form.value.instructions = instructionsString.value.split('\n').map((i: string) => i.trim()).filter(Boolean)
  emit('submit', { ...form.value })
}
</script>
<style scoped>
.modal-backdrop {
  position: fixed;
  z-index: 9000;
  inset: 0;
  background: #0007;
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal {
  background: #fff;
  border-radius: 11px;
  width: 420px;
  max-width: 96vw;
  box-shadow: 0 4px 32px #0003;
  padding: 2.3em 2em 1.6em 2em;
  margin: 0;
}
h2 {
  color: #4caf50;
  margin-bottom: 1em;
  text-align: center;
}
form label {
  display: block;
  color: #333;
  margin-bottom: 0.4em;
  font-weight: 500;
  margin-top: 0.8em;
}
input, textarea {
  width: 100%;
  font: inherit;
  padding: 0.6em;
  border-radius: 4px;
  border: 1.5px solid #e1e1e1;
  margin-top: 0.12em;
  margin-bottom: 0.4em;
  background: #fafbfc;
  resize: none;
}
.actions {
  margin-top: 1.6em;
  display: flex;
  gap: 0.7em;
  justify-content: flex-end;
}
button {
  font: inherit;
  padding: 0.44em 1.45em;
  border-radius: 3px;
  border: none;
  cursor: pointer;
  background: #f6f8f7;
  color: #333;
}
button.primary { background: #4caf50; color: white; }
button.secondary { background: #8bc34a; color: #fff;}
button.accent { background: #ff9800; color: #fff;}
</style>

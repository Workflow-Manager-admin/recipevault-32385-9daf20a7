<template>
  <div class="layout">
    <SidebarFilters :tags="recipesStore.tags" @filter="onFilter" />
    <main class="main-content">
      <div class="actions-row">
        <button class="primary" v-if="userStore.isAuthenticated" @click="showRecipeForm = true">Add Recipe</button>
        <div v-if="recipesStore.loading" class="loading">Loading...</div>
      </div>
      <RecipeList
        :recipes="recipesStore.recipes"
        @view="onView"
        @edit="onEdit"
        @delete="onDelete"
        @toggleFavorite="onToggleFavorite"
      />
      <RecipeDetail v-if="selectedRecipe"
                    :recipe="selectedRecipe"
                    :editable="userStore.user?.id === selectedRecipe.user_id"
                    @close="selectedRecipe = null"
                    @edit="onEdit"
                    @delete="onDelete" />
      <RecipeForm v-if="showRecipeForm"
                  :editing="editRecipe !== null"
                  :value="editRecipe || undefined"
                  @submit="onFormSubmit"
                  @close="closeForm" />
    </main>
  </div>
</template>
<script setup lang="ts">
import SidebarFilters from '../components/SidebarFilters.vue'
import RecipeList from '../components/RecipeList.vue'
import RecipeDetail from '../components/RecipeDetail.vue'
import RecipeForm from '../components/RecipeForm.vue'
import { useRecipesStore } from '../stores/recipes'
import type { Recipe } from '../stores/recipes'
import { useUserStore } from '../stores/user'
import { ref, onMounted } from 'vue'

const recipesStore = useRecipesStore()
const userStore = useUserStore()

const selectedRecipe = ref<Recipe | null>(null)
const showRecipeForm = ref(false)
const editRecipe = ref<Recipe | null>(null)

onMounted(() => { recipesStore.fetchRecipes() })

function onFilter(filters: Record<string, unknown>) {
  recipesStore.fetchRecipes(filters)
}
function onView(recipe: Recipe) {
  selectedRecipe.value = recipe
}
function onEdit(recipe: Recipe) {
  showRecipeForm.value = true
  editRecipe.value = { ...recipe }
}
async function onDelete(recipe: Recipe) {
  if (confirm('Delete this recipe?')) {
    await recipesStore.deleteRecipe(recipe.id)
    if (selectedRecipe.value && selectedRecipe.value.id === recipe.id) selectedRecipe.value = null
  }
}
function onToggleFavorite(recipe: Recipe) {
  recipesStore.toggleFavorite(recipe)
}
async function onFormSubmit(recipe: Recipe) {
  try {
    if (editRecipe.value) await recipesStore.updateRecipe(editRecipe.value.id, recipe)
    else await recipesStore.addRecipe(recipe)
    closeForm()
  } catch (e) {
    alert((e as Error)?.message || "Error submitting recipe")
  }
}
function closeForm() {
  showRecipeForm.value = false
  editRecipe.value = null
}
</script>
<style scoped>
.layout {
  display: flex;
  min-height: 90vh;
  margin: 0 auto;
}
.main-content {
  flex: 1;
  padding: 2.5em 2.7em;
  background: #fcfcfc;
}
.actions-row {
  display: flex;
  gap: 1.1em;
  margin-bottom: 1.25em;
}
.loading {
  margin-left: 1.5em;
  color: #4caf50;
}
</style>

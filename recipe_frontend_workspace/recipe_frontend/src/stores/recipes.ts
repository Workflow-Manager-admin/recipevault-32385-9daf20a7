import { defineStore } from 'pinia'
import { useUserStore } from './user'

export type Recipe = {
  id: number
  user_id?: number
  title: string
  cuisine?: string
  time?: number
  description?: string
  tags?: string[]
  ingredients?: string[]
  instructions?: string[]
  favorite?: boolean
  author?: string
}

// PUBLIC_INTERFACE
export const useRecipesStore = defineStore('recipes', {
  state: () => ({
    recipes: [] as Recipe[],
    loading: false,
    error: '',
    tags: [] as string[],
  }),
  getters: {},
  actions: {
    // PUBLIC_INTERFACE
    async fetchRecipes(filters: Record<string, unknown> = {}) {
      this.loading = true; this.error = ''
      const userStore = useUserStore()
      let url = `${import.meta.env.VITE_API_URL || 'http://localhost:3001'}/recipes`
      const params = new URLSearchParams()
      for (const [k, v] of Object.entries(filters)) {
        if (v === true) params.set(k, '1')
        else if (v) params.set(k, `${v}`)
      }
      if (params.toString()) url += '?' + params.toString()
      const res = await fetch(url, {
        headers: userStore.token ? { Authorization: `Bearer ${userStore.token}` } : {}
      })
      if (!res.ok) { this.error = 'Error loading recipes'; this.loading = false; return }
      const data = await res.json()
      this.recipes = data.recipes || data
      this.tags = Array.from(new Set(this.recipes.flatMap((r: Recipe) => r.tags || [])))
      this.loading = false
    },
    // PUBLIC_INTERFACE
    async fetchRecipe(id: number): Promise<Recipe> {
      this.loading = true
      const userStore = useUserStore()
      const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:3001'}/recipes/${id}`, {
        headers: userStore.token ? { Authorization: `Bearer ${userStore.token}` } : {}
      })
      this.loading = false
      if (!res.ok) throw new Error('Recipe not found')
      return await res.json()
    },
    // PUBLIC_INTERFACE
    async addRecipe(recipe: Omit<Recipe, 'id'>) {
      const userStore = useUserStore()
      const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:3001'}/recipes`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(userStore.token && { Authorization: `Bearer ${userStore.token}` }),
        },
        body: JSON.stringify(recipe)
      })
      if (!res.ok) throw new Error('Failed to add recipe')
      const newRecipe: Recipe = await res.json()
      this.recipes.unshift(newRecipe)
      return newRecipe
    },
    // PUBLIC_INTERFACE
    async updateRecipe(id: number, recipe: Partial<Recipe>) {
      const userStore = useUserStore()
      const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:3001'}/recipes/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          ...(userStore.token && { Authorization: `Bearer ${userStore.token}` }),
        },
        body: JSON.stringify(recipe)
      })
      if (!res.ok) throw new Error('Failed to update recipe')
      const updated: Recipe = await res.json()
      const i = this.recipes.findIndex(r => r.id === id)
      if (i >= 0) this.recipes[i] = updated
      return updated
    },
    // PUBLIC_INTERFACE
    async deleteRecipe(id: number) {
      const userStore = useUserStore()
      const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:3001'}/recipes/${id}`, {
        method: "DELETE",
        headers: userStore.token ? { Authorization: `Bearer ${userStore.token}` } : {}
      })
      if (!res.ok) throw new Error('Failed to delete recipe')
      this.recipes = this.recipes.filter((r) => r.id !== id)
    },
    // PUBLIC_INTERFACE
    async toggleFavorite(recipe: Recipe) {
      const userStore = useUserStore()
      const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:3001'}/recipes/${recipe.id}/favorite`, {
        method: 'POST',
        headers: {
          ...(userStore.token && { Authorization: `Bearer ${userStore.token}` }),
        }
      })
      if (!res.ok) throw new Error('Failed to update favorite')
      recipe.favorite = !recipe.favorite
    }
  }
})

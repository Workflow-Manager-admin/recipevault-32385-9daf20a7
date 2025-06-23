import { defineStore } from 'pinia'

// PUBLIC_INTERFACE
export const useUserStore = defineStore('user', {
  state: () => ({
    user: null as null | { id: number, username: string },
    token: window.localStorage.getItem('token') || '',
    loading: false,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    // PUBLIC_INTERFACE
    async login(username: string, password: string) {
      this.loading = true
      try {
        // Update with actual endpoint!
        const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:3001'}/auth/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password })
        })
        if (!res.ok) throw new Error('Login failed')
        const data = await res.json()
        this.token = data.token
        window.localStorage.setItem('token', data.token)
        this.user = data.user
      } finally {
        this.loading = false
      }
    },
    // PUBLIC_INTERFACE
    async register(username: string, password: string) {
      this.loading = true
      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:3001'}/auth/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password })
        })
        if (!res.ok) throw new Error('Registration failed')
        const data = await res.json()
        this.token = data.token
        window.localStorage.setItem('token', data.token)
        this.user = data.user
      } finally {
        this.loading = false
      }
    },
    // PUBLIC_INTERFACE
    logout() {
      this.user = null
      this.token = ''
      window.localStorage.removeItem('token')
    },
    // PUBLIC_INTERFACE
    async fetchProfile() {
      if (!this.token) return
      const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:3001'}/auth/me`, {
        headers: { Authorization: `Bearer ${this.token}` }
      })
      if (res.ok) {
        const data = await res.json()
        this.user = data.user
      }
    }
  }
})

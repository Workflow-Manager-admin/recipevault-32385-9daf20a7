<template>
  <header class="header">
    <nav>
      <router-link to="/" class="logo">RecipeVault</router-link>
      <router-link to="/" exact>Recipes</router-link>
      <router-link to="/add">Add Recipe</router-link>
      <span class="spacer"></span>
      <div v-if="userStore.isAuthenticated">
        <span>Welcome, {{ userStore.user?.username }}</span>
        <button class="accent" @click="logout">Logout</button>
      </div>
      <div v-else>
        <button class="primary" @click="$emit('show-login')">Login</button>
        <button class="secondary" @click="$emit('show-register')">Register</button>
      </div>
    </nav>
  </header>
</template>

<script setup lang="ts">
import { useUserStore } from '../stores/user'
const userStore = useUserStore()
const logout = () => userStore.logout()
</script>

<style scoped>
.header {
  background: #fff;
  border-bottom: 2px solid #e8e8e8;
  padding: 0.75rem 2rem;
  box-shadow: 0 2px 8px 0 #0001;
}
nav {
  display: flex;
  align-items: center;
  gap: 1.1rem;
}
.logo {
  font-weight: bold;
  font-size: 1.3rem;
  color: #4caf50;
  margin-right: 2rem;
}
.spacer {
  flex: 1;
}
a {
  color: #181818;
  text-decoration: none;
  padding: 0 0.3rem;
}
a.router-link-active {
  color: #4caf50;
  border-bottom: 2px solid #4caf50;
}
button {
  font: inherit;
  padding: 0.45em 1.1em;
  border-radius: 4px;
  border: none;
  margin-left: 0.25rem;
  cursor: pointer;
  background: #f1f3f5;
  color: #555;
  transition: background .2s, color .2s;
}
button.primary { background: #4caf50; color: #fff; }
button.secondary { background: #8bc34a; color: white; }
button.accent { background: #ff9800; color: #fff; }
button:hover { opacity: 0.9; }
</style>

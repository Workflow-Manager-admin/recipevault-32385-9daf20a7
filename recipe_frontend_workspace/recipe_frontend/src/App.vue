<script setup lang="ts">
import HeaderBar from './components/HeaderBar.vue'
import { ref } from 'vue'
import AuthModal from './components/AuthModal.vue'
import { useUserStore } from './stores/user'
const showAuth = ref(false)
const authMode = ref<'login'|'register'>('login')
const userStore = useUserStore()
function showLogin() {
  authMode.value = 'login'
  showAuth.value = true
}
function showRegister() {
  authMode.value = 'register'
  showAuth.value = true
}
function closeAuth() { showAuth.value = false }
function authDone() {
  showAuth.value = false
  userStore.fetchProfile()
}
</script>

<template>
  <HeaderBar @show-login="showLogin" @show-register="showRegister" />
  <RouterView />
  <AuthModal v-if="showAuth" :mode="authMode" @close="closeAuth" @done="authDone" @switchMode="authMode = $event" />
</template>

<style scoped>
body {
  background: #f9f9f9;
}
</style>

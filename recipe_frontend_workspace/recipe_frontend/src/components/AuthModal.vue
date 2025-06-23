<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal">
      <h2>{{ mode === 'register' ? 'Register' : 'Login' }}</h2>
      <form @submit.prevent="submit">
        <label>
          Username
          <input v-model="username" required maxlength="32" />
        </label>
        <label>
          Password
          <input v-model="password" type="password" required minlength="4" maxlength="64" />
        </label>
        <div class="actions">
          <button class="secondary" @click="$emit('close')">Cancel</button>
          <button class="primary" type="submit">{{ mode === 'register' ? 'Register' : 'Login' }}</button>
        </div>
        <div class="toggle">
          <span v-if="mode === 'login'">Don't have an account? <a @click.prevent="switchMode('register')">Register</a></span>
          <span v-else>Already have an account? <a @click.prevent="switchMode('login')">Login</a></span>
        </div>
      </form>
      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, defineProps, defineEmits } from 'vue'
import { useUserStore } from '../stores/user'
const props = defineProps<{ mode: 'login' | 'register' }>()
const emit = defineEmits(['close', 'done', 'switchMode'])

const userStore = useUserStore()
const username = ref('')
const password = ref('')
const error = ref('')
function switchMode(m: 'login' | 'register') {
  emit('switchMode', m)
}
async function submit() {
  error.value = ''
  try {
    if (props.mode === 'login') {
      await userStore.login(username.value, password.value)
    } else {
      await userStore.register(username.value, password.value)
    }
    emit('done')
  } catch (e) {
    error.value = (e as Error)?.message || 'Authentication failed'
  }
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
  width: 340px;
  max-width: 96vw;
  box-shadow: 0 4px 32px #0003;
  padding: 2.3em 2em 1.7em 2em;
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
input {
  width: 100%;
  font: inherit;
  padding: 0.6em;
  border-radius: 4px;
  border: 1.5px solid #e1e1e1;
  margin-top: 0.12em;
  margin-bottom: 0.4em;
  background: #fafbfc;
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
.toggle {
  font-size: 0.98em;
  margin-top: 1.2em;
  text-align: center;
}
.toggle a { color: #ff9800; cursor: pointer; }
.error {
  color: #ff9800;
  margin-top: 1em;
  text-align: center;
}
</style>

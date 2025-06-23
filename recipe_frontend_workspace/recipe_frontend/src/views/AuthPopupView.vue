<template>
  <AuthModal :mode="mode" @close="onClose" @done="onDone" @switchMode="switchMode" />
</template>
<script setup lang="ts">
import AuthModal from '../components/AuthModal.vue'
import { ref } from 'vue'
const mode = ref<'login' | 'register'>('login')
const emit = defineEmits(['done'])

function onClose() { emit('done') }
function onDone() { emit('done') }
function switchMode(m: 'login' | 'register') { mode.value = m }
</script>

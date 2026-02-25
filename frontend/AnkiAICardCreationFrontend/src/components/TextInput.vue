<template>
  <div class="container">
    <h2>Enter Content to create cards for</h2>

    <textarea v-model="inputText" placeholder="Enter text..." rows="4" />

    <button @click="sendRequest" :disabled="loading || !inputText.trim()">
      {{ loading ? 'Sending...' : 'Send' }}
    </button>

    <div v-if="error" class="error"><strong>Error:</strong> {{ error }}</div>

    <div v-if="response" class="response">
      <strong>Response:</strong>
      <pre>{{ response }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const inputText = ref('')
const response = ref(null)
const error = ref(null)
const loading = ref(false)

var url
if (import.meta.env.DEV) {
  url = 'http://127.0.0.1:8000'
} else {
  url = 'https://f618ad7356200906-backend-service-y55vgiciiq-uc.a.run.app'
}
url += '/create_cards'

async function sendRequest() {
  error.value = null
  response.value = null
  loading.value = true

  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: inputText.value,
      }),
    })

    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`)
    }

    const data = await res.json()
    response.value = JSON.stringify(data, null, 2)
  } catch (err) {
    error.value = err.message || 'Unknown error'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.container {
  max-width: 500px;
  margin: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

textarea {
  padding: 8px;
  font-family: monospace;
}

button {
  padding: 8px;
  cursor: pointer;
}

.error {
  color: red;
}

.response {
  background: #f4f4f4;
  padding: 10px;
  border-radius: 4px;
}
</style>

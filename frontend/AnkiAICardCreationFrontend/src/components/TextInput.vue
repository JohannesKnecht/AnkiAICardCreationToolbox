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
      <button @click="downloadResponse()">Download</button>
      <p style="word-break: break-all">{{ response }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const inputText = ref<string>('')
const response = ref<string | null>(null)
const error = ref<string | null>(null)
const loading = ref<boolean>(false)

let url: string = import.meta.env.DEV
  ? 'http://127.0.0.1:8000'
  : 'https://f618ad7356200906-backend-service-y55vgiciiq-uc.a.run.app'

url += '/create_cards'

async function sendRequest(): Promise<void> {
  error.value = null
  response.value = null
  loading.value = true

  try {
    const res: Response = await fetch(url, {
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

    const data: unknown = await res.json()

    response.value = JSON.stringify(data, null, 2)
  } catch (err: unknown) {
    if (err instanceof Error) {
      error.value = err.message
    } else {
      error.value = 'Unknown error'
    }
  } finally {
    loading.value = false
  }
}

function downloadResponse(): void {
  if (!response.value) {
    console.warn('Nothing to download')
    return
  }

  // Use plain text instead of JSON to avoid "undefined" issues
  const blob = new Blob([response.value], { type: 'text/plain' })
  const url: string = URL.createObjectURL(blob)
  const a: HTMLAnchorElement = document.createElement('a')
  a.href = url
  a.download = 'response.txt'
  a.click()
  URL.revokeObjectURL(url) // clean up
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

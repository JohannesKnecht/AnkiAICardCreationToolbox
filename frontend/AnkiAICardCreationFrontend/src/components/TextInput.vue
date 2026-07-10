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
import { useCardCreation } from '../composables/useCardCreation'

const { inputText, response, error, loading, sendRequest, downloadResponse } = useCardCreation()
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

import { ref } from 'vue'

const BASE_URL: string = import.meta.env.DEV
  ? 'http://127.0.0.1:8000'
  : 'https://f618ad7356200906-backend-service-y55vgiciiq-uc.a.run.app'

const CREATE_CARDS_URL = `${BASE_URL}/create_cards`

export function useCardCreation() {
  const inputText = ref<string>('')
  const response = ref<string | null>(null)
  const error = ref<string | null>(null)
  const loading = ref<boolean>(false)

  async function sendRequest(): Promise<void> {
    error.value = null
    response.value = null
    loading.value = true

    try {
      const res: Response = await fetch(CREATE_CARDS_URL, {
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

    const blob = new Blob([response.value], { type: 'text/plain' })
    const url: string = URL.createObjectURL(blob)
    const a: HTMLAnchorElement = document.createElement('a')
    a.href = url
    a.download = 'response.txt'
    a.click()
    URL.revokeObjectURL(url)
  }

  return {
    inputText,
    response,
    error,
    loading,
    sendRequest,
    downloadResponse,
  }
}

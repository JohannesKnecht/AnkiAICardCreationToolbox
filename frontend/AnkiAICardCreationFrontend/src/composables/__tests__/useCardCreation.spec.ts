import { describe, it, expect, vi, afterEach } from 'vitest'
import { useCardCreation } from '../useCardCreation'

describe('useCardCreation', () => {
  afterEach(() => {
    vi.restoreAllMocks()
    vi.unstubAllGlobals()
  })

  it('initializes with empty state', () => {
    const { inputText, response, error, loading } = useCardCreation()
    expect(inputText.value).toBe('')
    expect(response.value).toBeNull()
    expect(error.value).toBeNull()
    expect(loading.value).toBe(false)
  })

  it('sets loading to true while request is in flight', async () => {
    let resolveRequest!: () => void
    vi.spyOn(global, 'fetch').mockReturnValue(
      new Promise<Response>((resolve) => {
        resolveRequest = () => resolve({ ok: true, json: async () => ({}) } as Response)
      }),
    )
    const { inputText, loading, sendRequest } = useCardCreation()
    inputText.value = 'some text'
    const pending = sendRequest()
    expect(loading.value).toBe(true)
    resolveRequest()
    await pending
  })

  it('stores the JSON response on a successful fetch', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValue({
      ok: true,
      json: async () => ({ cards: ['Q: What is 2+2?', 'A: 4'] }),
    } as Response)

    const { inputText, response, error, loading, sendRequest } = useCardCreation()
    inputText.value = 'some text'
    await sendRequest()

    expect(loading.value).toBe(false)
    expect(error.value).toBeNull()
    expect(response.value).toContain('"cards"')
  })

  it('sets error on non-ok HTTP response', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValue({
      ok: false,
      status: 500,
    } as Response)

    const { inputText, response, error, sendRequest } = useCardCreation()
    inputText.value = 'some text'
    await sendRequest()

    expect(error.value).toContain('HTTP 500')
    expect(response.value).toBeNull()
  })

  it('sets error on network failure', async () => {
    vi.spyOn(global, 'fetch').mockRejectedValue(new Error('Network error'))

    const { inputText, error, sendRequest } = useCardCreation()
    inputText.value = 'some text'
    await sendRequest()

    expect(error.value).toBe('Network error')
  })

  it('does nothing when downloadResponse is called with no response', () => {
    const warnSpy = vi.spyOn(console, 'warn').mockImplementation(() => {})
    const { downloadResponse } = useCardCreation()
    downloadResponse()
    expect(warnSpy).toHaveBeenCalledWith('Nothing to download')
  })

  it('triggers a download when downloadResponse is called with a response', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValue({
      ok: true,
      json: async () => ({ cards: [] }),
    } as Response)

    const createObjectURL = vi.fn().mockReturnValue('blob:fake-url')
    const revokeObjectURL = vi.fn()
    vi.stubGlobal('URL', { createObjectURL, revokeObjectURL })

    const clickSpy = vi.fn()
    const fakeAnchor = { href: '', download: '', click: clickSpy } as unknown as HTMLAnchorElement
    const originalCreateElement = document.createElement.bind(document)
    vi.spyOn(document, 'createElement').mockImplementation((tag: string) => {
      if (tag === 'a') return fakeAnchor
      return originalCreateElement(tag)
    })

    const { inputText, sendRequest, downloadResponse } = useCardCreation()
    inputText.value = 'some text'
    await sendRequest()
    downloadResponse()

    expect(createObjectURL).toHaveBeenCalled()
    expect(clickSpy).toHaveBeenCalled()
    expect(revokeObjectURL).toHaveBeenCalledWith('blob:fake-url')
  })
})

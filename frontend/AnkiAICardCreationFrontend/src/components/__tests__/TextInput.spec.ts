import { describe, it, expect, vi, afterEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import TextInput from '../TextInput.vue'

const BACKEND_TIMEOUT = 30000

describe('TextInput', () => {
  afterEach(() => {
    vi.restoreAllMocks()
    vi.unstubAllGlobals()
  })

  it('renders the heading, textarea, and Send button', () => {
    const wrapper = mount(TextInput)
    expect(wrapper.find('h2').text()).toBe('Enter Content to create cards for')
    expect(wrapper.find('textarea').attributes('placeholder')).toBe('Enter text...')
    expect(wrapper.find('button').text()).toBe('Send')
  })

  it('disables the Send button when textarea is empty', () => {
    const wrapper = mount(TextInput)
    expect(wrapper.find('button').attributes('disabled')).toBeDefined()
  })

  it('enables the Send button when textarea has text', async () => {
    const wrapper = mount(TextInput)
    await wrapper.find('textarea').setValue('some text')
    expect(wrapper.find('button').attributes('disabled')).toBeUndefined()
  })

  it('shows "Sending..." and disables the button while loading', async () => {
    vi.spyOn(global, 'fetch').mockReturnValue(new Promise(() => {}))
    const wrapper = mount(TextInput)
    await wrapper.find('textarea').setValue('some text')
    await wrapper.find('button').trigger('click')
    expect(wrapper.find('button').text()).toBe('Sending...')
    expect(wrapper.find('button').attributes('disabled')).toBeDefined()
  })

  it(
    'displays the response and Download button on successful fetch',
    async () => {
      const wrapper = mount(TextInput)
      await wrapper.find('textarea').setValue('Water boils at 100°C.')
      await wrapper.find('button').trigger('click')

      // Wait for the real HTTP response to arrive and Vue to re-render
      await vi.waitFor(() => {
        expect(wrapper.find('.response').exists()).toBe(true)
      }, { timeout: BACKEND_TIMEOUT })

      expect(wrapper.find('.response button').text()).toBe('Download')
    },
    BACKEND_TIMEOUT,
  )

  it('shows an error on non-ok response', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValue({
      ok: false,
      status: 500,
    } as Response)

    const wrapper = mount(TextInput)
    await wrapper.find('textarea').setValue('some text')
    await wrapper.find('button').trigger('click')
    await flushPromises()

    expect(wrapper.find('.error').exists()).toBe(true)
    expect(wrapper.find('.error').text()).toContain('HTTP 500')
  })

  it('shows an error on network failure', async () => {
    vi.spyOn(global, 'fetch').mockRejectedValue(new Error('Network error'))

    const wrapper = mount(TextInput)
    await wrapper.find('textarea').setValue('some text')
    await wrapper.find('button').trigger('click')
    await flushPromises()

    expect(wrapper.find('.error').exists()).toBe(true)
    expect(wrapper.find('.error').text()).toContain('Network error')
  })

  it(
    'triggers a download when Download button is clicked',
    async () => {
      const createObjectURL = vi.fn().mockReturnValue('blob:fake-url')
      const revokeObjectURL = vi.fn()
      vi.stubGlobal('URL', { createObjectURL, revokeObjectURL })

      const clickSpy = vi.fn()
      const fakeAnchor = {
        href: '',
        download: '',
        click: clickSpy,
        setAttribute: vi.fn(),
      } as unknown as HTMLAnchorElement

      const originalCreateElement = document.createElement.bind(document)
      vi.spyOn(document, 'createElement').mockImplementation((tag: string) => {
        if (tag === 'a') return fakeAnchor
        return originalCreateElement(tag)
      })

      const wrapper = mount(TextInput)
      await wrapper.find('textarea').setValue('Water boils at 100°C.')
      await wrapper.find('button').trigger('click')

      // Wait for the real HTTP response to arrive and Vue to re-render
      await vi.waitFor(() => {
        expect(wrapper.find('.response button').exists()).toBe(true)
      }, { timeout: BACKEND_TIMEOUT })

      await wrapper.find('.response button').trigger('click')

      expect(createObjectURL).toHaveBeenCalled()
      expect(clickSpy).toHaveBeenCalled()
      expect(revokeObjectURL).toHaveBeenCalledWith('blob:fake-url')
    },
    BACKEND_TIMEOUT,
  )
})



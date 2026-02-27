import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import TextInput from '../TextInput.vue'

describe('TextInput', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn())
  })

  afterEach(() => {
    vi.restoreAllMocks()
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
    vi.mocked(global.fetch).mockReturnValue(new Promise(() => {}))
    const wrapper = mount(TextInput)
    await wrapper.find('textarea').setValue('some text')
    await wrapper.find('button').trigger('click')
    expect(wrapper.find('button').text()).toBe('Sending...')
    expect(wrapper.find('button').attributes('disabled')).toBeDefined()
  })

  it('displays the response and Download button on successful fetch', async () => {
    const fakeData = { cards: ['card1'] }
    vi.mocked(global.fetch).mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(fakeData),
    } as Response)

    const wrapper = mount(TextInput)
    await wrapper.find('textarea').setValue('some text')
    await wrapper.find('button').trigger('click')
    await flushPromises()

    expect(wrapper.find('.response').exists()).toBe(true)
    expect(wrapper.find('.response').text()).toContain(JSON.stringify(fakeData, null, 2))
    expect(wrapper.find('.response button').text()).toBe('Download')
  })

  it('shows an error on non-ok response', async () => {
    vi.mocked(global.fetch).mockResolvedValue({
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
    vi.mocked(global.fetch).mockRejectedValue(new Error('Network error'))

    const wrapper = mount(TextInput)
    await wrapper.find('textarea').setValue('some text')
    await wrapper.find('button').trigger('click')
    await flushPromises()

    expect(wrapper.find('.error').exists()).toBe(true)
    expect(wrapper.find('.error').text()).toContain('Network error')
  })

  it('triggers a download when Download button is clicked', async () => {
    const fakeData = { cards: ['card1'] }
    vi.mocked(global.fetch).mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(fakeData),
    } as Response)

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
    await wrapper.find('textarea').setValue('some text')
    await wrapper.find('button').trigger('click')
    await flushPromises()

    await wrapper.find('.response button').trigger('click')

    expect(createObjectURL).toHaveBeenCalled()
    expect(clickSpy).toHaveBeenCalled()
    expect(revokeObjectURL).toHaveBeenCalledWith('blob:fake-url')
  })
})

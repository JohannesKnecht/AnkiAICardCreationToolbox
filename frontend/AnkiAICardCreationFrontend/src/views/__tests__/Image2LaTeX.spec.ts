import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Image2LaTeX from '../Image2LaTeX.vue'

describe('Image2LaTeX', () => {
  it('renders "Coming soon" in an h1', () => {
    const wrapper = mount(Image2LaTeX)
    expect(wrapper.find('h1').text()).toBe('Coming soon')
  })
})

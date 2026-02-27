import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils'
import ImageInput from '../ImageInput.vue'

describe('ImageInput', () => {
  it('renders as an empty div', () => {
    const wrapper = mount(ImageInput)
    expect(wrapper.html()).toBe('<div></div>')
  })
})

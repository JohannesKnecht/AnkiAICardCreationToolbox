import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils'
import Overview from '../OverviewComponent.vue'

describe('OverviewComponent', () => {
  it('renders the getting started message', () => {
    const wrapper = mount(Overview)
    expect(wrapper.text()).toContain('Select CardCreation or Image2LaTeX to get started.')
  })
})

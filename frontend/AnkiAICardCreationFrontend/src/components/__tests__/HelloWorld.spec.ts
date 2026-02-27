import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils'
import Overview from '../OverviewComponent.vue'

describe('Overview', () => {
  it('renders properly', () => {
    const wrapper = mount(Overview, { props: { msg: 'Hello Vitest' } })
    expect(wrapper.text()).toContain('Select CardCreation or Image2LaTeX to get started.')
  })
})

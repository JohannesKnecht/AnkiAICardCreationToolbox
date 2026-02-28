import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils'
import MainComponent from '../MainComponent.vue'

describe('MainComponent', () => {
  it('renders the msg prop in an h1', () => {
    const wrapper = mount(MainComponent, { props: { msg: 'TestMessage' } })
    expect(wrapper.find('h1').text()).toBe('TestMessage')
  })

  it('renders the subtitle in an h3', () => {
    const wrapper = mount(MainComponent, { props: { msg: 'TestMessage' } })
    expect(wrapper.find('h3').text()).toBe('Toolbox for creating awesome Anki Cards using AI')
  })

  it('has the .greetings wrapper class', () => {
    const wrapper = mount(MainComponent, { props: { msg: 'TestMessage' } })
    expect(wrapper.find('.greetings').exists()).toBe(true)
  })
})

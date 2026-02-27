import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createMemoryHistory } from 'vue-router'
import App from '../App.vue'
import MainComponent from '../components/MainComponent.vue'

const router = createRouter({
  history: createMemoryHistory(),
  routes: [{ path: '/', component: { template: '<div />' } }],
})

describe('App', () => {
  it('renders navigation links in the header', async () => {
    const wrapper = mount(App, {
      global: { plugins: [router] },
    })
    await router.isReady()

    const nav = wrapper.find('nav')
    expect(nav.text()).toContain('Overview')
    expect(nav.text()).toContain('CardCreation')
    expect(nav.text()).toContain('Image2LaTeX')
  })

  it('renders MainComponent with the correct msg prop', async () => {
    const wrapper = mount(App, {
      global: { plugins: [router] },
    })
    await router.isReady()

    const main = wrapper.findComponent(MainComponent)
    expect(main.exists()).toBe(true)
    expect(main.props('msg')).toBe('AnkiAICardCreationToolbox')
  })
})

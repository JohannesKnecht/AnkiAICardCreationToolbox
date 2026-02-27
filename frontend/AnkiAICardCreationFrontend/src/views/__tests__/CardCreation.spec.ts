import { describe, it, expect } from 'vitest'
import { shallowMount } from '@vue/test-utils'
import CardCreation from '../CardCreation.vue'
import TextInput from '../../components/TextInput.vue'

describe('CardCreation', () => {
  it('renders the TextInput child component', () => {
    const wrapper = shallowMount(CardCreation)
    expect(wrapper.findComponent(TextInput).exists()).toBe(true)
  })
})

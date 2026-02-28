import { describe, it, expect } from 'vitest'
import { shallowMount } from '@vue/test-utils'
import OverviewView from '../OverviewView.vue'
import OverviewComponent from '../../components/OverviewComponent.vue'

describe('OverviewView', () => {
  it('renders the OverviewComponent child', () => {
    const wrapper = shallowMount(OverviewView)
    expect(wrapper.findComponent(OverviewComponent).exists()).toBe(true)
  })
})

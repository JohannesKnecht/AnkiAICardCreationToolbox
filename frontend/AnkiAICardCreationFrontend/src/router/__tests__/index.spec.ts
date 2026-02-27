import { describe, it, expect } from 'vitest'
import router from '../index'

describe('router', () => {
  it('has 3 routes', () => {
    expect(router.getRoutes()).toHaveLength(3)
  })

  it('has a home route at "/"', () => {
    const homeRoute = router.getRoutes().find((r) => r.path === '/')
    expect(homeRoute).toBeDefined()
    expect(homeRoute?.name).toBe('home')
  })

  it('has an /Image2LaTeX route with a lazy-loaded component', () => {
    const route = router.getRoutes().find((r) => r.path === '/Image2LaTeX')
    expect(route).toBeDefined()
    expect(typeof route?.components?.default).toBe('function')
  })

  it('has a /CardCreation route with a lazy-loaded component', () => {
    const route = router.getRoutes().find((r) => r.path === '/CardCreation')
    expect(route).toBeDefined()
    expect(typeof route?.components?.default).toBe('function')
  })
})

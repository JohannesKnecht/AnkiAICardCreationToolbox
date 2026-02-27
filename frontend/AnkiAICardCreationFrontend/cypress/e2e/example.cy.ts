// https://on.cypress.io/api

describe('Overview', () => {
  it('visits the app root url', () => {
    cy.visit('/')
    cy.contains('div', 'Select CardCreation or Image2LaTeX to get started.')
  })
})

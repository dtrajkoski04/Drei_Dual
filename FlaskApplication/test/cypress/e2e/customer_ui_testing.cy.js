// Defines a suite of tests for the Customer Data Dashboard
describe('Customer Data Dashboard Tests', () => {

  // Before each test, navigate to the home page
  beforeEach(() => {
    cy.visit('http://127.0.0.1:5000'); // Visit the base URL of the application
  });

  // Test case for retrieving and displaying the customer list
  it('Customer List Retrieval Test', () => {
    cy.contains('Load Data').click(); // Click on the button that loads the customer data
    cy.get('#customerTable tbody tr').should('have.length.at.least', 1); // Asserts that at least one row exists in the customer table after data load
  });

  // Test case for checking the sorting functionality
  it('Sorting Test', () => {
    cy.get('#sortBy').select('First Name'); // Selects 'First Name' from the sort options
    cy.get('#sortOrder').select('Ascending'); // Sets the sort order to 'Ascending'
    cy.contains('Load Data').click(); // Triggers the data loading process with the specified sort conditions

    // Ensures that the data is sorted alphabetically by first name from the first to the last element
    cy.get('#customerTable tbody tr').first().find('td').eq(2).invoke('text').then((text1) => {
      cy.get('#customerTable tbody tr').last().find('td').eq(2).invoke('text').should((text2) => {
        expect(text1.localeCompare(text2)).to.be.at.most(0); // Checks that the first name in the first row is <= the first name in the last row, confirming sorting order
      });
    });
  });

  // Test case for checking the filtering functionality
  it('Filtering Test', () => {
    cy.get('#filterField').select('City'); // Selects 'City' from the filter options
    cy.get('#filterValue').type('Cindychester'); // Inputs 'Cindychester' as the filter value
    cy.contains('Load Data').click(); // Applies the filter and loads the data

    // Checks every cell in the city column of the table to ensure they all contain 'Cindychester'
    cy.get('#customerTable tbody tr td:nth-child(6)').each(($cell) => {
      cy.wrap($cell).should('contain', 'Cindychester'); // Asserts that each cell in the specified column contains the city 'Cindychester'
    });
  });
});

// Attaches a click event listener to the 'Load Data' button
document.getElementById('loadData').addEventListener('click', function() {
    // Retrieves values for sorting and filtering from the form
    const sortBy = document.getElementById('sortBy').value;
    const sortOrder = document.getElementById('sortOrder').value;
    const filterType = document.getElementById('filterField').value;
    const filterValue = document.getElementById('filterValue').value.trim();

    // Constructs the URL with query parameters for fetching filtered and sorted data
    let url = `http://127.0.0.1:5000/customers?sort_by=${sortBy}&sort_order=${sortOrder}&filter_type=${filterType}&filter_value=${encodeURIComponent(filterValue)}`;

    // Performs the fetch operation to the constructed URL
    fetch(url)
        .then(response => {
            if (!response.ok) { // Checks if the response is successful
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json(); // Parses the JSON data from the response
        })
        .then(data => {
            const tableBody = document.getElementById('customerTable').getElementsByTagName('tbody')[0];
            tableBody.innerHTML = ''; // Clears existing table rows

            // Iterates through each customer data and populates the table
            data.forEach(customer => {
                let row = tableBody.insertRow(); // Inserts a new row
                row.insertCell().textContent = customer.customer_index; // Populates cells with customer data

                // Creates a clickable link for customer ID leading to the customer details page
                let customerLink = document.createElement('a');
                customerLink.href = `details?customer_id=${customer.customer_id}`;
                customerLink.textContent = customer.customer_id;
                customerLink.style.textDecoration = "none"; // Styles the link to not look like a traditional hyperlink
                customerLink.style.color = "black"; // Sets the link color to black

                let cell = row.insertCell();
                cell.appendChild(customerLink); // Appends the link to the table cell

                // Continues populating cells with other customer attributes
                row.insertCell().textContent = customer.first_name;
                row.insertCell().textContent = customer.last_name;
                row.insertCell().textContent = customer.company;
                row.insertCell().textContent = customer.city;
                row.insertCell().textContent = customer.country;
                row.insertCell().textContent = customer.phone1;
                row.insertCell().textContent = customer.phone2;
                row.insertCell().textContent = customer.email;
                row.insertCell().textContent = customer.subscription_date;
                row.insertCell().textContent = customer.website;
                row.insertCell().textContent = customer.sales_2021;
                row.insertCell().textContent = customer.sales_2022;
            });
        })
        .catch(error => { // Catches and logs any errors in the fetch operation
            console.error('There was a problem with the fetch operation: ', error);
        });
});

document.getElementById('loadData').addEventListener('click', function() {
    const sortBy = document.getElementById('sortBy').value;
    const sortOrder = document.getElementById('sortOrder').value;
    const filterValue = document.getElementById('filterValue').value.trim();

    // Constructing the URL with potential sorting and filtering parameters
    let url = `http://127.0.0.1:5000/customers?sort_by=${sortBy}&sort_order=${sortOrder}`;
    if (filterValue) {
        // Appending the filter value to the URL; assuming backend can parse this generic filter
        url += `&filter_value=${encodeURIComponent(filterValue)}`;
    }

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            const tableBody = document.getElementById('customerTable').getElementsByTagName('tbody')[0];
            tableBody.innerHTML = ''; // Clear previous entries

            // Iterating over each customer and appending data to the table
            data.forEach(customer => {
                let row = tableBody.insertRow();
                
                // Inserting customer index, if available
                row.insertCell().textContent = customer.customer_index;
                
                // Creating a button for the Customer ID that redirects to the details page
                let customerIDButton = document.createElement('button');
                customerIDButton.textContent = customer.customer_id;
                customerIDButton.onclick = function() {
                    window.location.href = `details.html?customer_id=${customer.customer_id}`;
                };
                let cell = row.insertCell();
                cell.appendChild(customerIDButton);

                // Inserting other customer details into the table
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
        .catch(error => {
            console.error('There was a problem with the fetch operation: ', error);
        });
});

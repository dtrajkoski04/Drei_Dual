document.getElementById('loadData').addEventListener('click', function() {
    const sortBy = document.getElementById('sortBy').value;
    const sortOrder = document.getElementById('sortOrder').value;
    const filterValue = document.getElementById('filterValue').value;

    let url = `http://127.0.0.1:5000/customers?sort_by=${sortBy}&sort_order=${sortOrder}`;
    if (filterValue) {
        url += `&filter=${filterValue}`;  // Assuming backend can handle a generic filter
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

            data.forEach(customer => {
                let row = tableBody.insertRow();
                
                // Create a button for Customer ID
                let customerIDButton = document.createElement('button');
                customerIDButton.textContent = customer.customer_id;
                customerIDButton.onclick = function() {
                    window.location.href = `details.html?customer_id=${customer.customer_id}`;
                };

                row.insertCell().textContent = customer.customer_index;
                let cell = row.insertCell();
                cell.appendChild(customerIDButton);
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

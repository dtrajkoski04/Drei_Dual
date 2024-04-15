document.getElementById('loadData').addEventListener('click', function() {
    fetch('http://127.0.0.1:5000/customers')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            const tableBody = document.getElementById('customerTable').getElementsByTagName('tbody')[0];
            tableBody.innerHTML = ''; // Clear previous entries

            // Populate table with new entries
            data.forEach(customer => {
                let row = tableBody.insertRow();
                row.insertCell(0).textContent = customer.customer_index;
                row.insertCell(1).textContent = customer.customer_id;
                row.insertCell(2).textContent = customer.first_name;
                row.insertCell(3).textContent = customer.last_name;
                row.insertCell(4).textContent = customer.company;
                row.insertCell(5).textContent = customer.city;
                row.insertCell(6).textContent = customer.country;
                row.insertCell(7).textContent = customer.phone1;
                row.insertCell(8).textContent = customer.phone2;
                row.insertCell(9).textContent = customer.email;
                row.insertCell(10).textContent = customer.subscription_date;
                row.insertCell(11).textContent = customer.website;
                row.insertCell(12).textContent = customer.sales_2021;
                row.insertCell(13).textContent = customer.sales_2022;
            });
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation: ', error);
        });
});

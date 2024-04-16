document.addEventListener('DOMContentLoaded', function() {
    // Function to extract 'customer_id' from the URL query parameters
    function getQueryParam(param) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    }

    const customerId = getQueryParam('customer_id');
    if (!customerId) {
        alert('Customer ID is missing!');
        return;
    }

    fetch(`http://127.0.0.1:5000/sales_data?customer_id=${customerId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch data: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                console.error('Error:', data.error);
                return;
            }
            drawPieChart(data.sales_shares);
            drawLineChart(data.sales_development);
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
});

function drawPieChart(data) {
    const ctx = document.getElementById('pieChart').getContext('2d');
    let chart = Chart.getChart('pieChart'); // Get the chart instance if exists
    if (chart) {
        chart.destroy(); // Destroy the existing chart instance before creating a new one
    }
    chart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.map(item => item.name),
            datasets: [{
                label: 'Sales Share by Year',
                data: data.map(item => item['2021_share']).concat(data.map(item => item['2022_share'])),
                backgroundColor: [
                    'rgba(255, 99, 132, 0.5)', 'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)', 'rgba(75, 192, 192, 0.5)',
                    'rgba(153, 102, 255, 0.5)', 'rgba(255, 159, 64, 0.5)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)', 'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)', 'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            }
        }
    });
}

function drawLineChart(data) {
    const ctx = document.getElementById('lineChart').getContext('2d');
    let chart = Chart.getChart('lineChart'); // Get the chart instance if exists
    if (chart) {
        chart.destroy(); // Destroy the existing chart instance before creating a new one
    }
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['2021', '2022'],
            datasets: data.map((item) => ({
                label: item.name,
                data: [item.sales_over_time['2021'], item.sales_over_time['2022']],
                fill: false,
                borderColor: `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 0.8)`,
                backgroundColor: `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 0.5)`,
                tension: 0.1
            }))
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    position: 'top'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            }
        }
    });
}

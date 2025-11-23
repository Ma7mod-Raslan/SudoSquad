document.addEventListener('DOMContentLoaded', function () {

    // --- NEW: Function to fetch and update stats ---
    const totalUrlsElement = document.getElementById('total-urls-value');

    async function updateStats() {
        try {
            const response = await fetch('/stats');
            if (!response.ok) {
                throw new Error('Failed to fetch stats');
            }
            const data = await response.json();
            totalUrlsElement.textContent = data.total_urls;
        } catch (error) {
            console.error('Error fetching stats:', error);
            totalUrlsElement.textContent = 'N/A';
        }
    }

    // --- Chart Configuration ---

    const chartLabels = ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'];
    const requestRateData = [45, 30, 60, 85, 80, 70];
    const totalUrlsData = [120, 125, 140, 160, 180, 195];

    // Chart.js Global Defaults
    Chart.defaults.font.family = 'Inter, sans-serif';
    Chart.defaults.plugins.legend.display = false;
    Chart.defaults.responsive = true;
    // We removed 'maintainAspectRatio = false' to fix the chart height

    // --- Request Rate Chart ---
    const requestRateCtx = document.getElementById('requestRateChart').getContext('2d');
    const gradient = requestRateCtx.createLinearGradient(0, 0, 0, 200);
    gradient.addColorStop(0, 'rgba(59, 130, 246, 0.2)');
    gradient.addColorStop(1, 'rgba(59, 130, 246, 0)');

    new Chart(requestRateCtx, {
        type: 'line',
        data: {
            labels: chartLabels,
            datasets: [{
                label: 'Request Rate',
                data: requestRateData,
                borderColor: '#3b82f6',
                borderWidth: 2.5,
                pointRadius: 0,
                tension: 0.4,
                fill: true,
                backgroundColor: gradient
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true, ticks: { stepSize: 25 } },
                x: { grid: { display: false } }
            }
        }
    });

    // --- Total URLs Created Chart ---
    const totalUrlsCtx = document.getElementById('totalUrlsChart').getContext('2d');
    new Chart(totalUrlsCtx, {
        type: 'line',
        data: {
            labels: chartLabels,
            datasets: [{
                label: 'Total URLs',
                data: totalUrlsData,
                borderColor: '#10b981',
                borderWidth: 2.5,
                pointBackgroundColor: '#10b981',
                pointBorderColor: '#ffffff',
                pointHoverBorderWidth: 2,
                pointRadius: 5,
                tension: 0.4,
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: false, ticks: { stepSize: 50 } },
                x: { grid: { display: false } }
            }
        }
    });

    // --- Form Submission Logic ---
    const form = document.getElementById('shorten-form');
    const resultDiv = document.getElementById('result');
    const resultLink = resultDiv.querySelector('a');

    form.addEventListener('submit', async function (event) {
        event.preventDefault();
        const longUrl = document.getElementById('long-url').value;

        console.log("Submitting URL:", longUrl);

        try {
            const response = await fetch(`/shorten?long_url=${encodeURIComponent(longUrl)}`, {
                method: 'POST',
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            const shortUrl = `${window.location.host}/${data.short_code}`;

            resultLink.href = `http://${shortUrl}`;
            resultLink.textContent = shortUrl;
            resultDiv.classList.remove('hidden');

            // NEW: Update stats after successfully creating a new URL
            updateStats();

        } catch (error) {
            console.error('Error shortening URL:', error);
            resultLink.textContent = 'Error creating short URL.';
            resultDiv.classList.remove('hidden');
        }
    });

    // NEW: Initial call to load the stats when the page first loads
    updateStats();
});
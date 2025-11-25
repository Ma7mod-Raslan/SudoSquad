document.addEventListener('DOMContentLoaded', function () {

    const form = document.getElementById('shorten-form');
    const resultDiv = document.getElementById('result');
    const resultLink = resultDiv.querySelector('a');

    form.addEventListener('submit', async function (event) {
        event.preventDefault();
        const longUrl = document.getElementById('long-url').value;

        try {
            const response = await fetch(`/shorten?long_url=${encodeURIComponent(longUrl)}`, {
                method: 'POST',
            });

            if (!response.ok) throw new Error('Failed request');

            const data = await response.json();

            // Correct URL format
            const shortUrl = `${window.location.protocol}//${window.location.hostname}:${window.location.port}/${data.short_code}`;

            resultLink.href = shortUrl;
            resultLink.textContent = shortUrl;
            resultDiv.classList.remove('hidden');

            // Update Stats
            updateStats();

            // Refresh Grafana Panels
            document.querySelectorAll("iframe").forEach(frame => {
                frame.src = frame.src;
            });

        } catch (error) {
            console.error('Error:', error);
            resultLink.textContent = "Error creating short URL.";
            resultDiv.classList.remove('hidden');
        }
    });

    // Stats logic
    const totalUrlsElement = document.getElementById('total-urls-value');

    async function updateStats() {
        try {
            const response = await fetch('/stats');
            const data = await response.json();
            totalUrlsElement.textContent = data.total_urls;
        } catch (err) {
            totalUrlsElement.textContent = "N/A";
        }
    }

    updateStats();
});

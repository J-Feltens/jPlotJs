function calc_port(z = 0.001) {
    const url = `/calc_port/${z}`;
    return fetch(url)
        .then(response => {
            if (!response.ok) {
                // HTTP error (404, 500, etc.)
                console.log(`HTTP ${response.status}: ${response.statusText} (${url})`, "warning");
            }
            return response.json();
        });
}

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("network_scanner");
    const resultsContainer = document.getElementById("scan_results");

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent the default form submission

        const formData = new FormData(form);
        const network = formData.get("network");

        resultsContainer.textContent = "Scanning..."; // Show a loading message

        fetch("/netscanner", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({ network: network }),
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error("An error has occured: " + response.statusText);
                }
                return response.json(); // Parse the JSON response
            })
            .then((data) => {
                resultsContainer.textContent = data.message; // Display only the message field
            })
            .catch((error) => {
                resultsContainer.textContent = `Error: ${error.message}`;
            });
    });
});
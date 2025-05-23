document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("network_scanner");
    const resultsContainer = document.getElementById("scan_results");

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData(form);
        const network = formData.get("network");

        resultsContainer.textContent = "Scanning...";

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
            return response.json();
        })
        .then((data) => {
            resultsContainer.textContent = data.message;
        })
        .catch((error) => {
            resultsContainer.textContent = `Error: ${error.message}`;
        });
    });
});
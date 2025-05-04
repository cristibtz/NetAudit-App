document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("port_scanner");
    const resultsContainer = document.getElementById("port_results");

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        
        const formData = new FormData(form);
        const ip =  formData.get("ip");
        const mode = formData.get("mode");

        resultsContainer.textContent = "Scanning ports...";

        fetch("/portscanner", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({ 
                ip: ip,
                mode: mode              
            })
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error("An error has occurred: " + response.statusText);
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
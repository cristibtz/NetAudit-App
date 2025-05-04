document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("web_fuzzer");
    const resultsContainer = document.getElementById("fuzz_results");

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData(form);
        const url = formData.get("url");

        resultsContainer.textContent = "Scanning url...";

        fetch("/webfuzzer", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({ url: url }),
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
document.getElementById("payButton").addEventListener("click", function () {
    let paymentStatus = "success";  // Simulating successful payment (Replace with actual payment gateway response)

    fetch("/checkout/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: new URLSearchParams({ "payment_status": paymentStatus })
    })
    .then(response => response.text())
    .then(data => {
        window.location.href = "/orders/";  // Redirect to orders page
    })
    .catch(error => console.error("Error:", error));
});

// Function to get CSRF token for security
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        let cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

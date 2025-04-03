const API_URL = "http://127.0.0.1:1234";

async function register() {
    let user = {
        username: document.getElementById("regUsername").value,
        password: document.getElementById("regPassword").value,
        security_question: document.getElementById("securityQuestion").value,
        security_answer: document.getElementById("securityAnswer").value
    };
    
    let res = await fetch(`${API_URL}/register/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(user)
    });

    if (res.ok) alert("Registered Successfully!");
}

async function login() {
    let username = document.getElementById("loginUsername").value;
    let password = document.getElementById("loginPassword").value;

    fetch("/login/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.token) {
            localStorage.setItem("token", data.token);
            window.location.href = "/welcome";  // ✅ Redirect to /welcome
        } else {
            alert("Invalid login credentials");
        }
    })
    .catch(error => console.error("Error:", error));
}

async function resetPassword() {
    let user = {
        username: document.getElementById("resetUsername").value,
        security_answer: document.getElementById("resetAnswer").value,
        new_password: document.getElementById("newPassword").value
    };

    let res = await fetch(`${API_URL}/reset-password/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(user)
    });

    if (res.ok) alert("Password Reset Successfully!");
}

async function checkWelcome() {
    let token = localStorage.getItem("token");
    let res = await fetch(`${API_URL}/welcome/`, {
        headers: { "Authorization": `Bearer ${token}` }
    });

    if (res.ok) {
        document.getElementById("welcomeText").innerText = "🎉 Welcome!";
    } else {
        window.location.href = "index.html";
    }
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "index.html";
}

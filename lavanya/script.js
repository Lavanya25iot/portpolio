const visitorsEl = document.getElementById("visitors");
const form = document.getElementById("contactForm");
const statusEl = document.getElementById("formStatus");
const yearEl = document.getElementById("year");

const nameEl = document.getElementById("name");
const roleEl = document.getElementById("role");
const aboutEl = document.getElementById("about");
const skillsEl = document.getElementById("skills");

yearEl.textContent = new Date().getFullYear();

async function loadProfile() {
    try {
        const response = await fetch("/api/profile");
        const data = await response.json();
        if (data?.name) nameEl.textContent = data.name;
        if (data?.role) roleEl.textContent = data.role;
        if (data?.about) aboutEl.textContent = data.about;
        if (Array.isArray(data?.skills)) {
            skillsEl.innerHTML = data.skills.map((skill) => `<li>${skill}</li>`).join("");
        }
    } catch (error) {
        console.error("Failed to load profile:", error);
    }
}

async function loadStats() {
    try {
        const response = await fetch("/api/stats");
        const data = await response.json();
        visitorsEl.textContent = data?.visitors ?? 0;
    } catch (error) {
        visitorsEl.textContent = "0";
        console.error("Failed to load stats:", error);
    }
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    statusEl.textContent = "Sending message...";

    const payload = {
        name: document.getElementById("contactName").value.trim(),
        email: document.getElementById("contactEmail").value.trim(),
        message: document.getElementById("contactMessage").value.trim(),
    };

    try {
        const response = await fetch("/api/contact", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        const data = await response.json();
        if (response.ok && data.success) {
            statusEl.textContent = data.message;
            form.reset();
        } else {
            statusEl.textContent = data.error || "Something went wrong.";
        }
    } catch (error) {
        statusEl.textContent = "Unable to connect to server.";
        console.error("Contact form error:", error);
    }
});

loadProfile();
loadStats();

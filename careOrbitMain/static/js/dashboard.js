// all dashboard features

document.addEventListener("DOMContentLoaded", function () {

    // gets time 
    let currentHour = new Date().getHours();
    const greetingElement = document.getElementById("greet");

    // get users name and formats
    let userName = greetingElement.dataset.name;
    let nameString = userName ? ", " + userName : "";
    let greetingText = "Hello";

    if (currentHour < 12) {
        greetingText = "Good morning";
    } else if (currentHour < 17) {
        greetingText = "Good afternoon";
    } else {
        greetingText = "Good evening";
    }

    greetingElement.textContent = greetingText + nameString;

    // dashboard appointments 
    fetch('/dashboard/appointments-data/')
        .then(res => {
            if (!res.ok) {
                throw new Error("Failed to fetch appointments");
            }
            return res.json();
        })
        .then(data => {
            const container = document.getElementById("appointments-container");

            // no appointments
            if (!data.appointments || data.appointments.length === 0) {
                container.innerHTML = "<p>No upcoming appointments.</p>";
                return;
            }


            let htmlContent = "";

            data.appointments.forEach(appt => {
                let badgeClass = `badge-${appt.status.toLowerCase()}`;


                htmlContent += `
                <div class="appointment-card">
                    <div class="appointment-info">
                        <strong>${appt.doctor_name}</strong>
                        <p>${appt.reason} · ${appt.date}, ${appt.time}</p>
                    </div>
                    <span class="badge ${badgeClass}">${appt.status.toUpperCase()}</span>
                </div>
                `;
            });


            container.innerHTML = htmlContent;
        })
        .catch(error => {
            console.error("Error fetching appointments:", error);
            const container = document.getElementById("appointments-container");
            if (container) {
                container.innerHTML = "<p>There was an error loading appointments.</p>";
            }
        });

    // dashboard updates (medication refills)
    fetch('/dashboard/updates-data/')
        .then(res => {
            if (!res.ok) {
                throw new Error("Failed to fetch updates");
            }
            return res.json();
        })
        .then(data => {
            const container = document.getElementById("updates-container");

            if (!data.medications || data.medications.length === 0) {
                container.innerHTML = `
                <div class="update-card update-success">
                    <span class="update-icon">✅</span>
                    <div class="update-info">
                        <strong>All caught up!</strong>
                        <p>No pending medication refills.</p>
                    </div>
                </div>`;
                return;
            }

            let htmlContent = "";

            data.medications.forEach(med => {
                htmlContent += `
                <div class="update-card update-warning">
                    <span class="update-icon">⚠️</span>
                    <div class="update-info">
                        <strong>${med.name} — Refill Needed</strong>
                        <p>${med.dosage} · ${med.frequency}</p>
                        <a href="/medications/refill/">Request Refill</a>
                    </div>
                </div>`;
            });

            container.innerHTML = htmlContent;
        })
        .catch(error => {
            console.error("Error fetching updates:", error);
            const container = document.getElementById("updates-container");
            if (container) {
                container.innerHTML = "<p>There was an error loading updates.</p>";
            }
        });
});
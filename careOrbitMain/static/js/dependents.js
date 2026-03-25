// all dependent features 

document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('.add-dependent-form form');

    form.addEventListener('submit', function (event) {

        event.preventDefault();
        const token = document.querySelector('[name=csrfmiddlewaretoken]').value;


        // all form data 
        const data = {
            email: document.querySelector('[name="parent_email"]').value,
            dob: document.querySelector('[name="dob"]').value,
            password: document.querySelector('[name="password"]').value,
            relationship: document.querySelector('[name="relationship"]').value,
            name: document.querySelector('[name="dependent"]').value,
            nhs: document.querySelector('[name="nhs"]').value
        };

        fetch("/add-dependent/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': token,
            },
            body: JSON.stringify(data)
        })
            .then(res => {
                if (!res.ok) {
                    throw new Error("Failed to add dependent");
                }
                return res.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    form.reset(); // Clear the form

                    // check for HTML card
                    const name = data.dependent_name || "New Dependent";
                    const initial = name.charAt(0).toUpperCase();

                    // Just displaying the input DOB as the date
                    const d = new Date(document.querySelector('[name="dob"]').value);
                    const formattedDate = d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });

                    // Add dependents to page
                    const newCard = document.createElement('div');
                    newCard.className = 'dependent-card';
                    newCard.innerHTML = `
                        <div class="dependent-card-left">
                            <div class="dependent-avatar">
                                ${initial}
                            </div>
                            <div class="dependent-info">
                                <strong>${name}</strong>
                                <p>Date of birth: ${formattedDate} • NHS No: ${data.nhs_number || "N/A"}</p>
                                <div class="dependent-badges">
                                    <span class="badge-active">ACTIVE</span>
                                </div>
                            </div>
                        </div>
                        <button class="btn-view-profile">View Profile &rarr;</button>
                    `;

                    // remove placeholder 
                    const emptyMessage = document.querySelector('.dependents-list p');
                    if (emptyMessage) emptyMessage.remove();

                    document.querySelector('.dependents-list').prepend(newCard);

                } else {
                    alert("Error: " + data.message);
                }
            })
            .catch(error => {
                console.error("Fetch error:", error);
            });
    });
});

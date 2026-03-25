// edit depdentent profile 

document.addEventListener('DOMContentLoaded', () => {
    const editModal = document.getElementById('editDependentModal');

    editModal.addEventListener('show.bs.modal', e => {
        const btn = e.relatedTarget;
        const id = btn.getAttribute('data-id');

        // edit dependent form
        document.getElementById('edit-dependent-id').value = id;
        document.getElementById('edit-dependent-name').value = btn.getAttribute('data-name');
        document.getElementById('edit-dependent-dob').value = btn.getAttribute('data-dob');
        document.getElementById('edit-dependent-nhs').value = btn.getAttribute('data-nhs');

        const apptList = document.getElementById('dependent-appointments-list');
        const medList = document.getElementById('dependent-medications-list');
        apptList.innerHTML = 'Loading...';
        medList.innerHTML = 'Loading...';

        // get appointments and medication
        fetch(`/dependent-details/?id=${id}`)
            .then(r => r.json())
            .then(data => {
                if (data.status !== 'success') return;

                // appointments 
                apptList.innerHTML = data.appointments.length ? '' : 'No appointments';
                data.appointments.forEach(a => {
                    apptList.innerHTML += `<div class="border p-2 mb-2 bg-light"><strong>${a.date} ${a.time}</strong> - ${a.reason}</div>`;
                });

                // medications
                medList.innerHTML = data.medications.length ? '' : 'No medications';
                data.medications.forEach(m => {
                    medList.innerHTML += `<div class="border p-2 mb-2 bg-light"><strong>${m.name}</strong> - ${m.dosage} (${m.frequency})</div>`;
                });
            });
    });

    // save changes
    document.getElementById('save-edit-btn').addEventListener('click', () => {
        fetch('/edit-dependent/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({
                dependent_id: document.getElementById('edit-dependent-id').value,
                name: document.getElementById('edit-dependent-name').value,
                dob: document.getElementById('edit-dependent-dob').value,
                nhs: document.getElementById('edit-dependent-nhs').value
            })
        }).then(() => window.location.reload()); // Refresh page
    });

    // delete dependent
    document.getElementById('delete-dependent-btn').addEventListener('click', () => {
        if (!confirm("Are you sure you want to permanently delete this dependent?")) return;

        fetch('/delete-dependent/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({
                dependent_id: document.getElementById('edit-dependent-id').value
            })
        }).then(() => window.location.reload());
    });
});

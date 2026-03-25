// cancel and reschedule features 


document.addEventListener('DOMContentLoaded', function () {

    document.querySelectorAll('.reschedule-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const apptId = this.getAttribute('data-id');
            fetch('/appointments/cancel/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
                body: JSON.stringify({ appointment_id: apptId })
            })
                .then(function (r) { return r.json(); })
                .then(function (data) {
                    if (data.status === 'success') window.location.href = '/appointments/book/';
                });
        });
    });

    document.querySelectorAll('.cancel-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const apptId = btn.getAttribute('data-id');
            const title = btn.getAttribute('data-title');

            if (!confirm('Are you sure you want to cancel ?')) return;

            fetch('/appointments/cancel/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
                body: JSON.stringify({ appointment_id: apptId })
            })
                .then(function (r) { return r.json(); })
                .then(function (data) {
                    if (data.status === 'success') {
                        const card = btn.closest('.card');
                        card.style.opacity = '0';
                        card.style.transition = 'opacity 0.3s';
                        setTimeout(function () { card.remove(); }, 300);
                    }
                });
        });
    });

    function getCookie(name) {
        const value = '; ' + document.cookie;
        const parts = value.split('; ' + name + '=');
        if (parts.length === 2) return parts.pop().split(';').shift();
        return '';
    }

});

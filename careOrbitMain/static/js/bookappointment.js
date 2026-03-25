// book appointment features

var time_slots = ['09:00', '10:30', '12:00', '14:00', '15:30', '16:30'];

function toggleOtherBox() {
    var reason = document.getElementById('reason').value;
    document.getElementById('other-box').style.display = (reason === 'other') ? 'block' : 'none';
}

function updateSlots() {
    var date = document.getElementById('preferred-date').value;
    var doctor = document.getElementById('preferred-doctor').value;
    var hint = document.getElementById('slots-hint');
    var container = document.getElementById('slots-container');

    if (!date) {
        hint.style.display = 'block';
        container.innerHTML = '';
        return;
    }

    hint.style.display = 'none';
    container.innerHTML = '<p style="color:grey; font-size:0.9rem">Loading...</p>';

    fetch('/appointments/available-slots/?date=' + date + '&doctor=' + doctor)
        .then(function (r) { return r.json(); })
        .then(function (data) { renderSlots(data.booked_slots || []); })
        .catch(function () {
            container.innerHTML = '<div class="alert alert-danger w-100 py-2">Could not load slots. Please try again.</div>';        });
}

function renderSlots(bookedSlots) {
    var container = document.getElementById('slots-container');
    container.innerHTML = '';

    for (var i = 0; i < time_slots.length; i++) {
        var slot = time_slots[i];
        var taken = bookedSlots.indexOf(slot) !== -1;

        var btn = document.createElement('button');
        btn.type = 'button';
        
        btn.className = 'btn fw-bold py-2 px-4 slot-btn flex-grow-1 ' + (taken ? 'btn-light text-muted border opacity-50' : 'btn-outline-primary shadow-sm');
        btn.disabled = taken; 
        
        btn.innerHTML = taken ? '<s>' + slot + '</s>' : slot;

        if (!taken) {
            btn.setAttribute('data-slot', slot);
            btn.onclick = function () { selectSlot(this); };
        }

        container.appendChild(btn);
    }
}

function selectSlot(el) {
    // 1. Reset all available buttons back to blue outlines and restore their shadow
    document.querySelectorAll('.slot-btn:not(:disabled)').forEach(function (btn) {
        btn.classList.replace('btn-primary', 'btn-outline-primary');
        btn.classList.add('shadow-sm');
    });
    
    el.classList.replace('btn-outline-primary', 'btn-primary');
    el.classList.remove('shadow-sm');
        document.getElementById('selected_slot').value = el.getAttribute('data-slot');
}



// book appointment features 


var time_slots = ['09:00', '10:30', '12:00', '14:00', '15:30', '16:30'];

function toggleOtherBox() {
    var reason = document.getElementById('reason').value;
    document.getElementById('other-box').style.display = (reason === 'other') ? 'block' : 'none';
}

function selectVisitType(type) {
    document.getElementById('visit_type').value = type;
    document.getElementById('btn-inperson').className = (type === 'in_person') ? 'visit-btn visit-btn-active' : 'visit-btn';
    document.getElementById('btn-virtual').className = (type === 'virtual') ? 'visit-btn visit-btn-active' : 'visit-btn';
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
            container.innerHTML = '<p style="color:red; font-size:0.9rem">Could not load slots.</p>';
        });
}

function renderSlots(bookedSlots) {
    var container = document.getElementById('slots-container');
    container.innerHTML = '';

    for (var i = 0; i < time_slots.length; i++) {
        var slot = time_slots[i];
        var taken = bookedSlots.indexOf(slot) !== -1;

        var div = document.createElement('div');
        div.className = 'slot-row' + (taken ? ' slot-unavailable' : '');
        div.innerHTML = '<span class="slot-time">' + slot + '</span><span class="slot-status">' + (taken ? 'Unavailable' : 'Available') + '</span>';

        if (!taken) {
            div.setAttribute('data-slot', slot);
            div.onclick = function () { selectSlot(this); };
        }

        container.appendChild(div);
    }
}

function selectSlot(el) {
    document.querySelectorAll('.slot-row').forEach(function (row) {
        row.classList.remove('slot-selected');
        var s = row.querySelector('.slot-status');
        if (s && !row.classList.contains('slot-unavailable')) s.textContent = 'Available';
    });
    el.classList.add('slot-selected');
    el.querySelector('.slot-status').textContent = 'Selected ✓';
    document.getElementById('selected_slot').value = el.getAttribute('data-slot');
}



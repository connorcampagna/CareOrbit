// search bar functionality for records page and quick links

function filterRecords() {
    const input = document.getElementById('search-input');
    const filter = input.value.trim().toLowerCase(); 
    const activeTab = document.querySelector('.tab-pane.active');
    
    if (!activeTab) return;
    
    const rows = activeTab.querySelectorAll('.list-group-item');
    let visibleCount = 0;

    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        
        if (text.includes(filter)) {
            row.classList.remove('d-none'); 
            visibleCount++;
        } else {
            row.classList.add('d-none'); 
        }
    });

    const countDisplay = document.getElementById('records-count');
    if (countDisplay) {
        if (filter === "") {
            countDisplay.innerText = "Showing All Records";
        } else {
            countDisplay.innerText = `Found ${visibleCount} result${visibleCount !== 1 ? 's' : ''}`;
        }
    }
}

// go to specific tab
document.addEventListener('DOMContentLoaded', function () {
    const hash = window.location.hash;
    if (hash) {
        const tabBtn = document.querySelector('[data-bs-target="' + hash + '"]');
        if (tabBtn) {
            const tab = new bootstrap.Tab(tabBtn);
            tab.show();
        }
    }

    // clear search when switching tabs
    const tabs = document.querySelectorAll('[data-bs-toggle="tab"]');
    tabs.forEach(btn => {
        btn.addEventListener('shown.bs.tab', function () {
            const input = document.getElementById('search-input');
            if (input) {
                input.value = '';
                filterRecords();
            }
        });
    });
});


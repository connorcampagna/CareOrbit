function filterRecords() {
    const input = document.getElementById('search-input');
    const filter = input.value.toLowerCase();
    const rows = document.querySelectorAll('.record-row');
    let visibleCount = 0;

    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        if (text.includes(filter)) {
            row.style.display = "flex";
            visibleCount++;
        } else {
            row.style.display = "none";
        }
    });

    const countDisplay = document.getElementById('records-count');
    if (filter === "") {
        countDisplay.innerText = "Showing All Records";
    } else {
        countDisplay.innerText = `Found ${visibleCount} result${visibleCount !== 1 ? 's' : ''}`;
    }

}

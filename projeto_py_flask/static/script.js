function showSection(sectionId) {
    document.querySelectorAll("section").forEach(section => {
        section.classList.add("hidden");
    });
    document.getElementById(sectionId).classList.remove("hidden");
}

function returnToMenu() {
    showSection('menu');
}

function registerSale() {
    const day = document.getElementById("day").value;
    const time = document.getElementById("time").value;
    const flavor = document.getElementById("flavor").value;
    const quantity = parseInt(document.getElementById("quantity").value);

    fetch("/registrar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ dia: day, hora: time, sabor: flavor, quantidade: quantity })
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message || data.error);
            if (!data.error) returnToMenu(); 
        })
        .catch(err => console.error(err));
}

function loadData(apiEndpoint, sectionId, outputId) {
    fetch(apiEndpoint)
        .then(response => response.json())
        .then(data => {
            const outputDiv = document.getElementById(outputId);
            outputDiv.innerHTML = formatData(data);
            showSection(sectionId);
        })
        .catch(err => console.error(err));
}

function formatData(data) {
    if (typeof data === 'string') return `<p>${data}</p>`;
    if (Array.isArray(data)) {
        return data.map(item => `<p>${item}</p>`).join('');
    }
    if (typeof data === 'object') {
        return Object.entries(data)
            .map(([key, value]) => `<p><strong>${key}:</strong> ${JSON.stringify(value)}</p>`)
            .join('');
    }
    return '<p>Nenhum dado disponível.</p>';
}

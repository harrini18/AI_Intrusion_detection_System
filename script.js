let rssiChart, latencyChart, bandwidthChart;

// Initialize Charts
function initCharts() {
    const ctxRSSI = document.getElementById("rssiChart").getContext("2d");
    const ctxLatency = document.getElementById("latencyChart").getContext("2d");
    constctxBandwidth = document.getElementById("bandwidthChart").getContext("2d");

    const chartOptions = {
        responsive: true,
        animation: {
            duration: 1000,
            easing: "easeOutQuart"
        },
        scales: { x: { beginAtZero: true } }
    };

    rssiChart = new Chart(ctxRSSI, {
        type: "line",
        data: { labels: [], datasets: [{ label: "RSSI (dBm)", data: [], borderColor: "blue", fill: false }] },
        options: chartOptions
    });

    latencyChart = new Chart(ctxLatency, {
        type: "line",
        data: { labels: [], datasets: [{ label: "Latency (ms)", data: [], borderColor: "red", fill: false }] },
        options: chartOptions
    });

    bandwidthChart = new Chart(ctxBandwidth, {
        type: "line",
        data: { labels: [], datasets: [{ label: "Bandwidth (Mbps)", data: [], borderColor: "green", fill: false }] },
        options: chartOptions
    });
}

// Fetch Data from Flask API
async function fetchNetworks() {
    try {
        const response = await fetch("http://192.168.164.15:5000/upload");
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        
        const data = await response.json();
        updateTable(data.networks);
        updateCharts(data.networks);

    } catch (error) {
        console.error("Error fetching networks:", error);
    }
}

// Update Table
function updateTable(networks) {
    const tableBody = document.getElementById("networkTable");
    const alertBox = document.getElementById("alertBox");
    tableBody.innerHTML = "";

    let hasThreat = false;
    networks.forEach(network => {
        let row = document.createElement("tr");
        row.innerHTML = `
            <td>${network.SSID}</td>
            <td>${network.BSSID}</td>
            <td>${network.RSSI} dBm</td>
            <td class="${network.Encryption.includes('Open') ? 'text-danger' : 'text-success'}">
                ${network.Encryption}
            </td>
        `;
        if (network.Encryption.includes('Open')) hasThreat = true;
        tableBody.appendChild(row);
    });

    alertBox.innerHTML = hasThreat ? "⚠️ Rogue network detected!" : "✅ No threats detected";
    alertBox.className = hasThreat ? "alert alert-danger text-center" : "alert alert-success text-center";
}

// Update Charts
function updateCharts(networks) {
    const now = new Date().toLocaleTimeString();
    
    networks.forEach(network => {
        addData(rssiChart, now, network.RSSI);
        addData(latencyChart, now, Math.random() * 50 + 10);
        addData(bandwidthChart, now, Math.random() * 100 + 20);
    });
}

// Add Data to Chart
function addData(chart, label, value) {
    if (chart.data.labels.length > 10) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
    }
    chart.data.labels.push(label);
    chart.data.datasets[0].data.push(value);
    chart.update();
}

initCharts();
setInterval(fetchNetworks, 5000);
fetchNetworks();

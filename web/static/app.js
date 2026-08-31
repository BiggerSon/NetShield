async function loadStats() {

    try {

        const response =
            await fetch("/api/stats");

        const data =
            await response.json();

        document.getElementById("packets")
            .textContent = data.packets;

        document.getElementById("alerts")
            .textContent = data.alerts;

        document.getElementById("hosts")
            .textContent = data.hosts;

        document.getElementById("uptime")
            .textContent =
            formatUptime(data.uptime);

    } catch (error) {

        document.getElementById("status")
            .textContent = "● OFFLINE";
    }
}


function formatUptime(seconds) {

    const hours =
        Math.floor(seconds / 3600);

    const minutes =
        Math.floor((seconds % 3600) / 60);

    const secs =
        seconds % 60;

    return `${hours}h ${minutes}m ${secs}s`;
}


async function loadEvents() {

    try {

        const response =
            await fetch("/api/events");

        const events =
            await response.json();

        const table =
            document.getElementById("events");

        table.innerHTML = "";

        for (const event of events) {

            const row =
                document.createElement("tr");

            row.innerHTML = `
                <td>${escapeHtml(event.timestamp)}</td>

                <td>
                    ${escapeHtml(event.event_type)}
                </td>

                <td class="severity ${event.severity}">
                    ${escapeHtml(event.severity)}
                </td>

                <td>
                    ${event.risk_score}/100
                </td>

                <td>
                    ${escapeHtml(event.source || "-")}
                </td>

                <td>
                    ${escapeHtml(event.destination || "-")}
                </td>

                <td>
                    ${escapeHtml(event.message)}
                </td>
            `;

            table.appendChild(row);
        }

    } catch (error) {

        console.error(error);
    }
}


async function loadRisks() {

    try {

        const response =
            await fetch("/api/risks");

        const risks =
            await response.json();

        const container =
            document.getElementById("risks");

        container.innerHTML = "";

        for (
            const [ip, score]
            of Object.entries(risks)
        ) {

            const row =
                document.createElement("div");

            row.className = "risk-row";

            row.innerHTML = `
                <span>${escapeHtml(ip)}</span>
                <span class="risk-value">
                    ${score}/100
                </span>
            `;

            container.appendChild(row);
        }

    } catch (error) {

        console.error(error);
    }
}


function escapeHtml(value) {

    const div =
        document.createElement("div");

    div.textContent =
        String(value);

    return div.innerHTML;
}


async function refresh() {

    await loadStats();
    await loadEvents();
    await loadRisks();
}


refresh();

setInterval(
    refresh,
    3000
);
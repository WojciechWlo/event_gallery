// static/js/archives.js
import { downloadMedia, downloadAllMedia } from "./download_links.js";

document.addEventListener("DOMContentLoaded", async () => {
    const uploadsTableContainer = document.getElementById("uploads-table-container");

    try {
        const response = await fetch("/list_uploads", {
            method: "POST",
            headers: {
                "Accept": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error("Nie udało się pobrać uploadów.");
        }

        const uploads = (await response.json()).reverse();

        if (uploads.length === 0) {
            uploadsTableContainer.textContent = "Brak uploadów.";
            return;
        }

        // Link "Pobierz wszystko"
        const p = document.createElement("p");
        p.className = "download-all";
        const downloadAllLink = document.createElement("a");
        downloadAllLink.href = "#";
        downloadAllLink.textContent = "Pobierz wszystko";
        downloadAllLink.className = "download-link";
        downloadAllMedia(downloadAllLink);
        p.appendChild(downloadAllLink);
        uploadsTableContainer.appendChild(p);

        // Tabela
        const table = document.createElement("table");
        table.className = "upload-table";

        const thead = document.createElement("thead");
        const headerRow = document.createElement("tr");
        ["Upload", "Nickname", "Data", "Akcja"].forEach(text => {
            const th = document.createElement("th");
            th.textContent = text;
            thead.appendChild(th);
        });
        table.appendChild(thead);

        const tbody = document.createElement("tbody");

        uploads.forEach(upload => {
            const row = document.createElement("tr");

            const tdId = document.createElement("td");
            tdId.textContent = upload.id;

            const tdNickname = document.createElement("td");
            tdNickname.textContent = upload.nickname;

            const tdDate = document.createElement("td");
            tdDate.textContent = new Date(upload.datetime).toLocaleString();

            const tdLink = document.createElement("td");
            const link = document.createElement("a");
            link.href = "#";
            link.textContent = "Pobierz";
            link.className = "download-link";
            downloadMedia(link, upload.id);
            tdLink.appendChild(link);

            row.appendChild(tdId);
            row.appendChild(tdNickname);
            row.appendChild(tdDate);
            row.appendChild(tdLink);

            tbody.appendChild(row);
        });

        table.appendChild(tbody);
        uploadsTableContainer.appendChild(table);

    } catch (error) {
        console.error("Błąd podczas pobierania uploadów:", error);
        uploadsTableContainer.textContent = "Wystąpił błąd podczas ładowania listy.";
    }
});

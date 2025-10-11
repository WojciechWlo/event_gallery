// static/js/archives.js
import { downloadMedia, downloadAllMedia } from "./download_links.js";

const roles = JSON.parse(document.body.dataset.roles);

document.addEventListener("DOMContentLoaded", async () => {
    const uploadsTableContainer = document.getElementById("container");

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
            const downloadLink = document.createElement("a");
            downloadLink.href = "#";
            downloadLink.textContent = "Pobierz";
            downloadLink.className = "download-link";
            downloadMedia(downloadLink, upload.id);
            tdLink.appendChild(downloadLink);

            if(roles.includes("admin"))
            {
                const deleteLink = document.createElement("a");
                deleteLink.href = "#";
                deleteLink.textContent = "Usuń";
                deleteLink.className = "delete-link";
                deleteLink.style.marginLeft = "10px";
                tdLink.appendChild(deleteLink);


                deleteLink.addEventListener("click", async (e) => {
                    e.preventDefault();

                    const confirmed = confirm("Czy na pewno chcesz usunąć?");
                    if (!confirmed) return;

                    const formData = new FormData();
                    formData.append("upload_id", upload.id);

                    const response = await fetch("/delete_upload_by_id", {
                        method: "POST",
                        body: formData
                    });

                    if (response.ok) {
                        alert("Usunięto!");
                        row.parentElement.remove();
                    } else {
                        alert("Błąd podczas usuwania");
                    }
                });            
            }


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

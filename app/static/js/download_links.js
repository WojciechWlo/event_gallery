/*
function getFilenameFromContentDisposition(header) {
    try {
        const parts = header.split(";");
        for (const part of parts) {
            const [key, value] = part.trim().split("=");
            if (key.toLowerCase() === "filename" && value) {
                return value.replace(/^["']|["']$/g, "");
            }
        }
    } catch (e) {
        console.warn("Problem z parsowaniem Content-Disposition:", e);
    }
    return "download.zip";
}

async function fetchDownloadBlob(uploadId) {
    const response = await fetch("/download_media_by_upload_id", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ upload_id: uploadId }),
    });

    if (!response.ok) {
        throw new Error(`Download failed with status ${response.status}`);
    }

    const disposition = response.headers.get("Content-Disposition");
    const filename = disposition
        ? getFilenameFromContentDisposition(disposition)
        : `upload_${uploadId}.zip`;

    const blob = await response.blob();

    return { blob, filename };
}

async function fetchDownloadBlobAll() {
    const response = await fetch("/download_all_media", {
        method: "POST",
    });

    if (!response.ok) {
        throw new Error(`Download failed with status ${response.status}`);
    }

    const disposition = response.headers.get("Content-Disposition");
    const filename = disposition
        ? getFilenameFromContentDisposition(disposition)
        : `all_media.zip`;

    const blob = await response.blob();

    return { blob, filename };
}

function triggerDownloadFromBlob(blob, filename) {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
}

// Przykład użycia:

export function downloadMedia(element, uploadId) {
    element.addEventListener("click", async (event) => {
        event.preventDefault();

        try {
            const { blob, filename } = await fetchDownloadBlob(uploadId);
            triggerDownloadFromBlob(blob, filename);
        } catch (error) {
            console.error("Error downloading ZIP:", error);
            alert("Download failed");
        }
    });
}


export async function downloadAllMedia(element) {
    element.addEventListener("click", async (event) => {
        event.preventDefault();
    try {
        const { blob, filename } = await fetchDownloadBlobAll();
        triggerDownloadFromBlob(blob, filename);
    } catch (error) {
        console.error("Error downloading all media ZIP:", error);
        alert("Download failed");
        }
    });
}
*/

async function fetchDownloadOne(uploadId) {
    const response = await fetch("/download_media_by_upload_id", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ upload_id: uploadId }),
    });

    if (!response.ok) {
        throw new Error("Download preparation failed");
    }

    const data = await response.json();
    if (!data.url) {
        throw new Error("No download URL returned");
    }

    // 🟢 Teraz zamiast fetch() – przekierowujemy do FileResponse
    window.location.href = data.url; // lub window.open(data.url)
}

async function fetchDownloadAll() {
    const response = await fetch("/download_all_media", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        }
    });

    if (!response.ok) {
        throw new Error("Download preparation failed");
    }

    const data = await response.json();
    if (!data.url) {
        throw new Error("No download URL returned");
    }

    window.location.href = data.url;
}

export function downloadMedia(element, uploadId) {
    element.addEventListener("click", (event) => {
        event.preventDefault();

        const form = document.createElement("form");
        form.method = "POST";
        form.action = "/download_media_by_upload_id";
        form.style.display = "none";

        form.enctype = "application/x-www-form-urlencoded";

        const input = document.createElement("input");
        input.type = "hidden";
        input.name = "upload_id";
        input.value = uploadId;

        form.appendChild(input);
        document.body.appendChild(form);

        form.submit();
        document.body.removeChild(form);
    });
}


export function downloadAllMedia(element) {
    element.addEventListener("click", (event) => {
        event.preventDefault();

        const form = document.createElement("form");
        form.method = "POST";
        form.action = "/download_all_media";
        form.style.display = "none";

        document.body.appendChild(form);
        form.submit();
        document.body.removeChild(form);
    });
}
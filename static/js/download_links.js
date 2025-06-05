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
import { ModalGallery } from "./modal_gallery.js";

let modalGallery = new ModalGallery();

let loading = false;
let lastId = null;
let noMoreMedia = false;
let uploads_limit = 3;
let media_limit = 4;

async function loadMedia() {
    if (loading || noMoreMedia) return false;
    loading = true;

    try {
        const res = await fetch("/get_uploads_with_media_part", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ upload_last_id: lastId, uploads_limit: uploads_limit })
        });

        if (!res.ok) {
            console.error("Błąd przy pobieraniu mediów:", res.statusText);
            loading = false;
            return false;
        }
        
        const data = await res.json();
        const container = document.getElementById("all-uploads-container");

        data.uploads.forEach(upload => {
            const uploadContainer = document.createElement("div");
            uploadContainer.classList.add("upload-container");
            uploadContainer.style.marginBottom = "30px";

            const header = document.createElement("h3");
            header.innerHTML = `<a href="#" id="download-link" style="text-decoration: underline; color: blue; cursor: pointer;">
                Upload #${upload.upload_id} by ${upload.nickname} | ${upload.datetime}
            </a>`;
            setDownloadURL(header, upload.upload_id);
            header.style.marginBottom = "10px";
            uploadContainer.appendChild(header);
            
            const uploadMediaContainer = document.createElement("div");
            uploadMediaContainer.classList.add("upload-media-container");
            
            uploadMediaContainer.mediaData = upload.media;
            
            upload.media.slice(0, media_limit).forEach((item,index) => {
                let element;
                if (item.mediatype === "image" || item.mediatype === "img") {
                    element = document.createElement("img");
                    element.classList.add("media-element");
                    element.src = item.filename;
                    element.alt = "";
                } else if (item.mediatype === "video") {
                    element = document.createElement("video");
                    element.classList.add("media-element");
                    element.src = item.filename;
                    element.controls = true;
                    
                }

                element.addEventListener("click", function(event){
                    if (element instanceof HTMLVideoElement) {
                        event.preventDefault();
                        element.pause();

                    }
                    modalGallery.create(uploadMediaContainer.mediaData, index);
                });

                if (element) {
                    // Tworzymy wrapper
                    const wrapper = document.createElement("div");
                    wrapper.classList.add("media-element-wrapper");
                    wrapper.appendChild(element);

                    uploadMediaContainer.appendChild(wrapper);
                }
            });

            // Jeśli przekroczono media_limit, to ostatniemu wrapperowi dajemy przyciemnienie
            if (upload.media.length > media_limit && uploadMediaContainer.lastChild) {
                const lastWrapper = uploadMediaContainer.lastChild;
                lastWrapper.classList.add("media-element-more-wrapper");
                lastWrapper.style.setProperty("--content", `"+${upload.media.length - media_limit+1}"`);

                const mediaElement = lastWrapper.firstChild;
                if (mediaElement) {
                    mediaElement.classList.add("media-element-more");  // przyciemnienie
                }
            }

            if (upload.media.length ==1 && uploadMediaContainer.lastChild){
                uploadMediaContainer.style.justifyContent = "center";
                const lastWrapper = uploadMediaContainer.lastChild;
                lastWrapper.style.width = "65%";
            }

            uploadContainer.appendChild(uploadMediaContainer);
            container.appendChild(uploadContainer);
        });

        lastId = data.last_id;
        if (!lastId || data.uploads.length === 0) {
            noMoreMedia = true;
            window.removeEventListener("scroll", scrollHandler);
        }

        loading = false;
        return true;

    } catch (err) {
        console.error("Błąd:", err);
        loading = false;
        return false;
    }
}

async function autoLoadUntilScrollable() {
    while (
        document.body.scrollHeight <= window.innerHeight &&
        !noMoreMedia
    ) {
        const loaded = await loadMedia();
        if (!loaded) break;
        await new Promise(r => setTimeout(r, 50));
    }
}

function scrollHandler() {
    const containers = document.querySelectorAll(".upload-media-container");
    const lastContainer = containers[containers.length - 1];

    if (!lastContainer) return;

    const rect = lastContainer.getBoundingClientRect();

    // Jeśli dół ostatniego kontenera jest w zasięgu viewportu (np. 500px od dołu)
    if (rect.bottom - 500 <= window.innerHeight) {
        loadMedia();
    }
}


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

function setDownloadURL(element, uploadId) {
    element.addEventListener("click", async (event) => {
        event.preventDefault();

        try {
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
            const url = window.URL.createObjectURL(blob);

            const a = document.createElement("a");
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        } catch (error) {
            console.error("Error downloading ZIP:", error);
            alert("Download failed");
        }
    });
}


autoLoadUntilScrollable();
window.addEventListener("scroll", scrollHandler);

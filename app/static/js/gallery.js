import { ModalGallery } from "./modal_gallery.js";
import {downloadMedia} from "./download_links.js"

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
        const container = document.getElementById("container");

        data.uploads.forEach(upload => {
            const uploadContainer = document.createElement("div");
            uploadContainer.classList.add("upload-container");
            uploadContainer.style.marginBottom = "30px";

            const headerContainer = document.createElement("div");
            headerContainer.style.display = "flex";
            headerContainer.style.alignItems = "center";  // wyrównanie pionowe

            const header = document.createElement("h3");

            header.innerHTML = `Upload #${upload.upload_id} by ${upload.nickname} | ${upload.datetime}`;

            const downloadLink = document.createElement("a");
            downloadLink.href = "#";
            downloadLink.id = "download-link";
            downloadLink.style.textDecoration = "underline";
            downloadLink.style.color = "blue";
            downloadLink.style.cursor = "pointer";
            downloadLink.style.marginLeft = "10px";  // odstęp między headerem a linkiem
            downloadLink.textContent = "Pobierz";

            headerContainer.appendChild(header);
            headerContainer.appendChild(downloadLink);

            uploadContainer.appendChild(headerContainer);

            downloadMedia(downloadLink, upload.upload_id);

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
        document.body.scrollHeight <= window.innerHeight+1 &&
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





autoLoadUntilScrollable();
window.addEventListener("scroll", scrollHandler);

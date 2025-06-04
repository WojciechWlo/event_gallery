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
            body: JSON.stringify({ upload_last_id: lastId, uploads_limit: uploads_limit, media_limit: media_limit })
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
            header.textContent = `Upload #${upload.upload_id}`;
            header.style.marginBottom = "10px";
            uploadContainer.appendChild(header);
            
            const uploadMediaContainer = document.createElement("div");
            uploadMediaContainer.classList.add("upload-media-container");

            upload.media.forEach(item => {
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

                element.addEventListener("click", () => {
                    modalGallery.create();
                    modalGallery.show();
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
            if (upload.media_count > media_limit && uploadMediaContainer.lastChild) {
                const lastWrapper = uploadMediaContainer.lastChild;
                lastWrapper.classList.add("media-element-more-wrapper");
                lastWrapper.style.setProperty("--content", `"+${upload.media_count - media_limit+1}"`);

                const mediaElement = lastWrapper.firstChild;
                if (mediaElement) {
                    mediaElement.classList.add("media-element-more");  // przyciemnienie

                }
            }

            if (upload.media_count ==1 && uploadMediaContainer.lastChild){
                uploadMediaContainer.style.justifyContent = "center";
                const lastWrapper = uploadMediaContainer.lastChild;
                lastWrapper.style.width = "75%";
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

autoLoadUntilScrollable();
window.addEventListener("scroll", scrollHandler);

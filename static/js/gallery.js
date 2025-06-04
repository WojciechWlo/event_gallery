let loading = false;
let lastId = null;
let noMoreMedia = false;

async function loadMedia() {
    if (loading || noMoreMedia) return false;
    loading = true;

    try {
        const res = await fetch("/media", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ last_id: lastId, limit: 5 })
        });

        if (!res.ok) {
            console.error("Błąd przy pobieraniu mediów:", res.statusText);
            loading = false;
            return false;
        }

        const data = await res.json();
        const container = document.getElementById("media-container");

        data.media.forEach(item => {
            let element;
            if (item.mediatype === "image") {
                element = document.createElement("img");
                element.classList.add("media-img");
                element.src = item.filename;
                element.alt = "";
                element.style.maxWidth = "100%";
                element.style.display = "block";
            } else if (item.mediatype === "video") {
                element = document.createElement("video");
                element.src = item.filename;
                element.controls = true;
                element.style.maxWidth = "100%";
                element.style.display = "block";
            }

            if (element) {
                element.style.marginBottom = "10px";
                container.appendChild(element);
            }
        });

        lastId = data.last_id;

        if (!lastId || data.media.length === 0) {
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
    // Dopóki nie ma scrolla i nie skończyły się media — ładuj dalej
    while (
        document.body.scrollHeight <= window.innerHeight &&
        !noMoreMedia
    ) {
        const loaded = await loadMedia();
        if (!loaded) break;  // przerwij jeśli błąd
        // małe opóźnienie, żeby przeglądarka zdążyła renderować
        await new Promise(r => setTimeout(r, 50));
    }
}

function scrollHandler() {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 500) {
        loadMedia();
    }
}

// Inicjalizacja
autoLoadUntilScrollable();
window.addEventListener("scroll", scrollHandler);
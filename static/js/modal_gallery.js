// ModalGallery.js
export class ModalGallery {
    constructor() {
        this.element = null;
        this.leftButton = null;
        this.rightButton = null;
        this.gallery = null;
        this.index = 0;
    }

    create(gallery, start_index = 0) {
        if (this.element) return;

        this.gallery = gallery;
        this.index = start_index;

        this.element = document.createElement("div");
        this.element.classList.add("modal-gallery-overlay");

        // Zamknięcie całego modału kliknięciem
        this.element.addEventListener("click", () => this.remove());

        if(gallery.length >1){

            // Przyciski nawigacji
            this.leftButton = document.createElement("button");
            this.leftButton.textContent = "◀";
            this.leftButton.classList.add("modal-gallery-left");

            this.rightButton = document.createElement("button");
            this.rightButton.textContent = "▶";
            this.rightButton.classList.add("modal-gallery-right");

            // Przyciski NIE zamykają — zatrzymujemy propagację
            this.leftButton.addEventListener("click", e => {
                e.stopPropagation();

                this.index -=1;
                if(this.index <0){
                    this.index = this.gallery.length-1;
                }

                this.update();
            });

            this.rightButton.addEventListener("click", e => {
                e.stopPropagation();

                this.index +=1;
                if(this.index >=this.gallery.length){
                    this.index = 0;
                }

                this.update();
            });

            this.element.appendChild(this.leftButton);
            this.element.appendChild(this.rightButton);

        }

        document.body.appendChild(this.element);
        
        this.update()
    }

    update() {
        if (this.mediaElement) {
            this.mediaElement.remove();
            this.mediaElement = null;
        }

        if (this.gallery[this.index].mediatype === "image") {
            this.mediaElement = document.createElement("img");
            this.mediaElement.src = this.gallery[this.index].filename;
        } else if (this.gallery[this.index].mediatype === "video") {
            this.mediaElement = document.createElement("video");
            this.mediaElement.src = this.gallery[this.index].filename;
            this.mediaElement.controls = true;
            this.mediaElement.autoplay = true;
            this.mediaElement.loop = true;
        }

        if (this.mediaElement) {
            this.mediaElement.classList.add("modal-gallery-media");
            this.element.appendChild(this.mediaElement);
        }
    }

    remove() {
        this.element.remove();
        this.element = null;
        this.leftButton = null;
        this.rightButton = null;
        this.gallery = null;
    }
}
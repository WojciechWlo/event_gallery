// ModalGallery.js
export class ModalGallery {
    constructor() {
        this.element = null;
    }

    create() {
        if (this.element) return;

        this.element = document.createElement("div");
        this.element.classList.add("modal-gallery-overlay");
        this.element.addEventListener("click", () => this.hide()); // klik = zamknięcie
        document.body.appendChild(this.element);
    }

    show() {
        if (!this.element) this.create();
        this.element.style.display = "block";
    }

    hide() {
        if (this.element) {
            this.element.style.display = "none";
        }
    }

    remove() {
        if (this.element) {
            this.element.remove();
            this.element = null;
        }
    }
}

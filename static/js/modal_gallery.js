// ModalGallery.js
export class ModalGallery {
    constructor() {
        this.element = null;
        this.leftButton = null;
        this.rightButton = null;
    }

    create() {
        if (this.element) return;

        this.element = document.createElement("div");
        this.element.classList.add("modal-gallery-overlay");

        // Zamknięcie całego modału kliknięciem
        this.element.addEventListener("click", () => this.remove());

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
            console.log("← LEFT");
        });

        this.rightButton.addEventListener("click", e => {
            e.stopPropagation();
            console.log("→ RIGHT");
        });

        this.element.appendChild(this.leftButton);
        this.element.appendChild(this.rightButton);

        document.body.appendChild(this.element);
    }

    show() {
        if (!this.element) this.create();
        this.element.style.display = "flex";
    }

    remove() {
        if (this.element) {
            this.element.remove();
            this.element = null;
            this.leftButton = null;
            this.rightButton = null;
        }
    }
}
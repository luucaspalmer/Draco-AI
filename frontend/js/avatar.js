/**
 * ==========================================
 * DRACO AI - Avatar Controller
 * ==========================================
 * Controla os estados visuais do avatar.
 */

const DracoAvatar = {

    estadoAtual: "idle",

    elemento: null,

    iniciar() {

        this.elemento = document.getElementById("draco-avatar-container");

        if (!this.elemento) {
            console.error("Avatar do Draco não encontrado.");
            return;
        }

        this.setState("idle");
    },

    setState(novoEstado) {

        if (!this.elemento) return;

        this.estadoAtual = novoEstado;

        this.elemento.setAttribute("data-mode", novoEstado);

        console.log("Avatar:", novoEstado);

    }

};

// Inicializa automaticamente quando a página carregar
document.addEventListener("DOMContentLoaded", () => {
    DracoAvatar.iniciar();
});
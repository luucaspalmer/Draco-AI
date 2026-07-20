/**
 * Draco AI - Núcleo Visual
 *
 * Controla o avatar e os estados visuais do Draco.
 */



const Draco = {



    // ==========================
    // Estado atual
    // ==========================

    estadoAtual: "IDLE",



    // ==========================
    // Elementos interface
    // ==========================

    elemento: null,

    status: null,

    avatar: null,



    // ==========================
    // Inicialização
    // ==========================

    iniciar() {



        this.elemento =
            document.getElementById(
                "draco-core"
            );



        this.status =
            document.getElementById(
                "draco-status"
            );



        this.avatar =
            document.getElementById(
                "draco-avatar-container"
            );



        if (!this.elemento) {



            console.error(
                "Elemento #draco-core não encontrado."
            );



            return;



        }



        this.mudarEstado(
            "IDLE"
        );



        console.log(
            "Draco visual iniciado."
        );



    },



    // ==========================
    // Alterar estado
    // ==========================

    mudarEstado(novoEstado) {



        this.estadoAtual =
            novoEstado.toUpperCase();



        console.log(
            "Estado Draco:",
            this.estadoAtual
        );



        if (!this.elemento) {

            return;

        }



        this.elemento.classList.remove(


            "draco-idle",

            "draco-listening",

            "draco-thinking",

            "draco-searching_memory",

            "draco-speaking",

            "draco-answering",

            "draco-error"


        );



        this.elemento.classList.add(


            "draco-" +

            this.estadoAtual.toLowerCase()


        );



        this.atualizarStatus();



    },



    // ==========================
    // Atualizar status
    // ==========================

    atualizarStatus() {



        const mensagens = {



            IDLE:

            "Draco Online",



            LISTENING:

            "Ouvindo...",



            THINKING:

            "Pensando...",



            SEARCHING_MEMORY:

            "Consultando memória...",



            SPEAKING:

            "Falando...",



            ANSWERING:

            "Respondendo...",



            ERROR:

            "Erro interno"



        };



        if(this.status) {



            this.status.textContent =

                mensagens[this.estadoAtual] ||

                "Draco ativo";



        }



    },



    // ==========================
    // Estados públicos
    // ==========================



    descansar(){


        this.mudarEstado(

            "IDLE"

        );


    },



    ouvir(){


        this.mudarEstado(

            "LISTENING"

        );


    },



    pensar(){


        this.mudarEstado(

            "THINKING"

        );


    },



    buscarMemoria(){


        this.mudarEstado(

            "SEARCHING_MEMORY"

        );


    },



    falar(){


        this.mudarEstado(

            "SPEAKING"

        );


    },



    responder(){


        this.mudarEstado(

            "ANSWERING"

        );


    },



    erro(){



        this.mudarEstado(

            "ERROR"

        );



        setTimeout(()=>{


            this.descansar();



        },3000);



    }


};




// ==========================
// Inicialização automática
// ==========================

document.addEventListener(


    "DOMContentLoaded",


    ()=>{


        Draco.iniciar();


    }


);
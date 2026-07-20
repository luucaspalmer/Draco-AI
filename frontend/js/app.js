/**
 * Draco AI
 * Aplicação Principal
 *
 * Responsável por iniciar
 * todos os módulos do frontend.
 */


const App = {


    iniciado: false,



    iniciar() {



        console.log(
            "Inicializando Draco AI..."
        );




        /*
         * Inicializa núcleo visual
         */

        Draco.iniciar();





        /*
         * Inicializa sistema de chat
         */

        Chat.iniciar();





        /*
         * Sistema carregado
         */

        this.iniciado = true;



        console.log(
            "Draco AI iniciado com sucesso."
        );



    }


};





/*
 * Aguarda carregamento completo
 * da página
 */


window.addEventListener(

    "DOMContentLoaded",

    () => {


        App.iniciar();


    }

);
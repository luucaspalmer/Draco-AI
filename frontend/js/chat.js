/**
 * Draco AI
 * Sistema de Chat
 *
 * Responsável pela interação
 * entre usuário e Draco.
 *
 * Comunicação real através
 * do api.js
 */


const Chat = {



    input: null,


    messages: null,




    // Inicializar chat

    iniciar() {



        this.input =
            document.getElementById(
                "user-input"
            );



        this.messages =
            document.getElementById(
                "messages"
            );





        if(
            !this.input ||
            !this.messages
        ){


            console.error(
                "Elementos do chat não encontrados."
            );


            return;


        }






        const botao =
            document.getElementById(
                "send-button"
            );






        botao.addEventListener(

            "click",

            () => {

                this.enviar();

            }

        );







        this.input.addEventListener(

            "keypress",

            (evento)=>{


                if(
                    evento.key === "Enter"
                ){

                    this.enviar();

                }


            }


        );






        console.log(
            "Chat iniciado."
        );



    },







    // Enviar mensagem

    async enviar(){



        const texto =

        this.input.value.trim();






        if(
            texto === ""
        ){

            return;

        }







        this.adicionarMensagem(

            texto,

            "usuario"

        );







        this.input.value = "";






        await this.processarMensagem(

            texto

        );




    },








    // Adiciona mensagem na tela

    adicionarMensagem(

        texto,

        tipo

    ){



        const div =

        document.createElement(
            "div"
        );




        div.classList.add(

            "message",

            tipo

        );





        div.innerText = texto;





        this.messages.appendChild(
            div
        );





        this.messages.scrollTop =

        this.messages.scrollHeight;



    },









    // Comunicação com Draco

    async processarMensagem(

        texto

    ){





        /*
         * Draco começa pensando
         */


        Draco.pensar();






        /*
         * Aguarda um pouco
         * simulando processamento
         */


        await this.esperar(

            1000

        );






        /*
         * Busca memória
         */


        Draco.buscarMemoria();






        /*
         * Envia para backend
         */


        const resposta =

        await API.enviarMensagem(

            texto

        );







        /*
         * Draco responde
         */


        Draco.responder();








        let mensagemDraco =

        resposta.resposta;







        if(
            !mensagemDraco
        ){


            mensagemDraco =

            "Não recebi uma resposta do meu núcleo.";


        }







        this.adicionarMensagem(

            mensagemDraco,

            "draco"

        );








        /*
         * Volta ao estado normal
         */


        setTimeout(

            ()=>{


                Draco.descansar();


            },

            1000


        );




    },









    // Pequeno temporizador auxiliar

    esperar(

        tempo

    ){



        return new Promise(

            resolver =>

            setTimeout(

                resolver,

                tempo

            )

        );


    }





};
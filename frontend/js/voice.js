/**
 * =====================================
 * Draco AI
 * Voice Module
 * =====================================
 *
 * Controle de comunicação por voz.
 *
 * Microfone
 * ↓
 * MediaRecorder
 * ↓
 * /voice
 * ↓
 * Draco
 * ↓
 * Piper
 * ↓
 * Áudio
 *
 */


const Voice = {



    stream: null,

    recorder: null,

    chunks: [],

    recording: false,

    button: null,



    // =====================================
    // Inicialização
    // =====================================

    init() {


        this.button =
            document.getElementById(
                "voice-button"
            );



        if (!this.button) {


            console.warn(
                "Botão de voz não encontrado."
            );


            return;


        }



        this.button.addEventListener(

            "click",

            () => this.toggleRecording()

        );


    },



    // =====================================
    // Comunicação com Draco.js
    // =====================================

    mudarEstadoDraco(estado) {


        if (
            typeof Draco === "undefined"
        ) {


            console.warn(
                "Draco.js não carregado."
            );


            return;


        }



        switch(estado) {


            case "LISTENING":


                Draco.ouvir();

                break;



            case "THINKING":


                Draco.pensar();

                break;



            case "SPEAKING":


                Draco.falar();

                break;



            case "IDLE":


                Draco.descansar();

                break;



        }


    },



    // =====================================
    // Alternar gravação
    // =====================================

    async toggleRecording() {


        if(this.recording) {


            this.stopRecording();


        }

        else {


            await this.startRecording();


        }


    },



    // =====================================
    // Iniciar gravação
    // =====================================

    async startRecording() {


        try {



            this.mudarEstadoDraco(
                "LISTENING"
            );



            this.stream =
                await navigator.mediaDevices.getUserMedia({

                    audio:true

                });



            this.chunks = [];



            this.recorder =
                new MediaRecorder(

                    this.stream

                );



            this.recorder.ondataavailable =
            (event)=>{


                if(event.data.size > 0){


                    this.chunks.push(

                        event.data

                    );


                }


            };



            this.recorder.onstop =
            ()=>{


                this.finishRecording();


            };



            this.recorder.start();



            this.recording = true;



            if(this.button){

                this.button.classList.add("recording");

            }



            console.log(
                "Gravação iniciada."
            );



        }


        catch(error){


            this.mudarEstadoDraco(
                "IDLE"
            );


            console.error(
                error
            );


        }


    },



    // =====================================
    // Parar gravação
    // =====================================

    stopRecording(){


        if(!this.recording){

            return;

        }



        this.recorder.stop();



        this.recording = false;



        if(this.button){

            this.button.classList.remove("recording");

        }



        this.mudarEstadoDraco(
            "THINKING"
        );


    },



    // =====================================
    // Finalizar gravação
    // =====================================

    async finishRecording(){


        const blob =
            new Blob(

                this.chunks,

                {

                    type:"audio/webm"

                }

            );



        if(this.stream){


            this.stream
                .getTracks()
                .forEach(

                    track=>track.stop()

                );


        }



        await this.sendAudio(
            blob
        );


    },



    // =====================================
    // Enviar para backend
    // =====================================

    async sendAudio(audioBlob){



        const formData =
            new FormData();



        formData.append(

            "audio",

            audioBlob,

            "input.webm"

        );



        try {



            const response =
                await fetch(

                    "http://127.0.0.1:8000/voice",

                    {

                        method:"POST",

                        body:formData

                    }

                );



            const data =
                await response.json();



            console.log(
                data
            );



            if(!data.success){


                this.mudarEstadoDraco(
                    "IDLE"
                );


                // O backend já pausou o detector de wake
                // word antes de responder. Como o áudio não
                // vai ser reproduzido neste caso, notificamos
                // o fim do "playback" imediatamente, para não
                // deixar o detector pausado sem necessidade.
                await this.notifyPlaybackFinished();


                return;


            }



            this.showUserMessage(
                data.user_text
            );



            this.showResponse(
                data
            );



            await this.playAudio();



        }


        catch(error){


            this.mudarEstadoDraco(
                "IDLE"
            );


            console.error(
                error
            );


            // Se a chamada falhou depois que o backend já
            // processou e pausou o detector (ex.: erro de
            // rede na resposta), garantimos que o Wake
            // Assistant não fique pausado indefinidamente.
            await this.notifyPlaybackFinished();


        }



    },



    // =====================================
    // Mensagem usuário
    // =====================================

    showUserMessage(text){


        const messages =
            document.getElementById(
                "messages"
            );



        if(!messages){

            return;

        }



        const div =
            document.createElement(
                "div"
            );



        div.className =
            "message usuario";



        div.textContent =
            text;



        messages.appendChild(div);



        messages.scrollTop =
            messages.scrollHeight;



    },



    // =====================================
    // Resposta Draco
    // =====================================

    showResponse(data){


        const messages =
            document.getElementById(
                "messages"
            );



        if(!messages){

            return;

        }



        const div =
            document.createElement(
                "div"
            );



        div.className =
            "message draco";



        div.textContent =
            data.response;



        messages.appendChild(div);



        messages.scrollTop =
            messages.scrollHeight;



    },



    // =====================================
    // Notificar backend: playback terminado
    //
    // Chamado sempre que um áudio do Draco termina de tocar
    // (com sucesso ou erro), para reativar o detector de
    // wake word no backend (que foi pausado antes da resposta
    // ser enviada, em /voice).
    //
    // Serve para QUALQUER reprodução de áudio feita pelo
    // frontend, não apenas a deste botão.
    // =====================================

    async notifyPlaybackFinished(){


        try {


            await fetch(

                "http://127.0.0.1:8000/voice/playback-finished",

                {

                    method:"POST"

                }

            );


        }


        catch(error){


            console.error(

                "Erro ao notificar fim de playback:",

                error

            );


        }


    },



    // =====================================
    // Áudio Draco
    // =====================================

    async playAudio(){



        this.mudarEstadoDraco(
            "SPEAKING"
        );



        await new Promise(

            r=>setTimeout(r,500)

        );



        const audio =
            new Audio(

                "http://127.0.0.1:8000/audio?t="
                +
                Date.now()

            );



        audio.onended = async ()=>{


            this.mudarEstadoDraco(
                "IDLE"
            );


            await this.notifyPlaybackFinished();


        };



        audio.onerror = async ()=>{


            this.mudarEstadoDraco(
                "IDLE"
            );


            // Mesmo em erro de reprodução, o backend já
            // pausou o detector antes de enviar a resposta —
            // precisamos reativar para não travar a wake
            // word.
            await this.notifyPlaybackFinished();


        };



        await audio.play();



    }



};



// =====================================
// Inicialização
// =====================================

document.addEventListener(

"DOMContentLoaded",

()=>{


    Voice.init();


}

);
/**
 * Draco AI
 * Comunicação com Backend
 *
 * Responsável pela ligação entre
 * frontend e cérebro do Draco.
 */


const API = {



    // Endereço da API Draco

    baseURL:

    "http://127.0.0.1:8000",







    /*
     * Verificar se Draco está online
     */

    async verificarStatus(){



        try{


            const resposta = await fetch(

                this.baseURL

            );



            return await resposta.json();



        }

        catch(erro){



            console.error(

                "Draco offline:",
                erro

            );



            return null;


        }


    },









    /*
     * Enviar mensagem para o cérebro
     */

    async enviarMensagem(

        mensagem

    ){



        try{



            const resposta = await fetch(



                this.baseURL + "/chat",



                {


                    method:"POST",



                    headers:{



                        "Content-Type":

                        "application/json"



                    },



                    body: JSON.stringify({



                        mensagem:

                        mensagem



                    })



                }


            );







            if(!resposta.ok){



                throw new Error(

                    "Erro ao comunicar com Draco."

                );


            }








            const dados = await resposta.json();




            return dados;



        }

        catch(erro){



            console.error(

                "Falha na comunicação:",

                erro

            );





            return {



                resposta:

                "Meu núcleo não está disponível no momento."



            };


        }


    }





};
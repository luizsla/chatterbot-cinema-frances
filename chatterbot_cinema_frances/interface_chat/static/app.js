const app = (() => {
    const templatesMensagens = {
        chat: $("#mensagem-chat-template"),
        user: $("#mensagem-user-template")
    }
    const containerConversa = $("#conversa-chatterbot");
    const inputConversa = $("#conversa-input");
    const botaoEnviar = $("#conversa-enviar-btn");
    const botaoBuscar = $("#buscar-roteiros-btn");
    const Toast = Swal.mixin({
        toast: true,
        position: "top-end",
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toast) => {
            toast.onmouseenter = Swal.stopTimer;
            toast.onmouseleave = Swal.resumeTimer;
        }
    });

    const perguntarRobo = pergunta => {
        const urlPergunta = botaoEnviar.data("url-perguntar");

        return $.get(urlPergunta, {pergunta})
            .then(resposta => {
                console.log(resposta);

                return resposta.resposta; 
            })
            .fail(() => {
                Toast.fire({
                    icon: "error",
                    title: "Houve um erro inesperado ao estabelecer à conversa",
                    text: "Por favor, tente novamente."
                });

                return null;
            }); 
    }

    const processarFala = (mensagemContainer, fala) => {
        mensagemContainer.find(".texto-fala").text(fala);
        containerConversa.append(mensagemContainer);
    }

    const processarDialogo = async (fala = null) => {
        const falaEnviar = fala == null ? inputConversa.val() : fala;
        processarFala(templatesMensagens.user.clone(), falaEnviar);
        const resposta = await perguntarRobo(falaEnviar);
        if (resposta == null) return;

        processarFala(templatesMensagens.chat.clone(), resposta);
        inputConversa.val("");
    }

    return {
        init() {
            inputConversa.on("keyup", event => {
                if (event.which != 13) return;

                processarDialogo();
            });

            botaoEnviar.on("click", processarDialogo);
            botaoBuscar.on("click", () => processarDialogo("quero roteiros"));
        }
    }
})();

$(app.init);
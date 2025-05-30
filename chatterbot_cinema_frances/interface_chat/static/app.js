const app = (() => {
    const templatesMensagens = {
        chat: $("#mensagem-chat-template"),
        user: $("#mensagem-user-template")
    }
    const containerConversa = $("#conversa-chatterbot");
    const inputConversa = $("#conversa-input");
    const botaoEnviar = $("#conversa-enviar-btn");

    const perguntarRobo = pergunta => {
        const urlPergunta = botaoEnviar.data("url-perguntar");

        return $.get(urlPergunta, {pergunta})
            .then(resposta => {
                return "A pergunta é: " + resposta.resposta; 
            });
    }

    const processarFala = (mensagemContainer, fala) => {
        mensagemContainer.find(".texto-fala").text(fala);
        containerConversa.append(mensagemContainer);
    }

    const processarDialogo = async () => {
        processarFala(templatesMensagens.user.clone(), inputConversa.val());
        const resposta = await perguntarRobo(inputConversa.val());
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
        }
    }
})();

$(app.init);
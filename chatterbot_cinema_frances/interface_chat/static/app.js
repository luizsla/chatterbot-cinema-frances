const app = (() => {
    const templatesMensagens = {
        chat: $("#mensagem-chat-template"),
        user: $("#mensagem-user-template")
    }
    const containerConversa = $("#conversa-chatterbot");
    const inputConversa = $("#conversa-input");
    const botaoEnviar = $("#conversa-enviar-btn");

    const perguntarRobo = pergunta => {
        console.log("A pergunta é: ", pergunta);

        return "A pergunta é: " + pergunta;
    }

    const processarFala = (mensagemContainer, fala) => {
        mensagemContainer.find(".texto-fala").text(fala);
        containerConversa.append(mensagemContainer);
    }

    const processarDialogo = () => {
        processarFala(templatesMensagens.user.clone(), inputConversa.val());
        const resposta = perguntarRobo(inputConversa.val());
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
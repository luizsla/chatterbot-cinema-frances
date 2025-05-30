const app = (() => {
    const templatesMensagens = {
        chat: $("#mensagem-chat-template"),
        user: $("#mensagem-user-template")
    }
    const inputConversa = $("#conversa-input");
    const botaoEnviar = $("#conversa-enviar-btn");

    const perguntarRobo = pergunta => {
        console.log("A pergunta é: ", pergunta);
    }

    return {
        init() {
            inputConversa.on("keyup", event => {
                if (event.which != 13) return;

                perguntarRobo(inputConversa.val());
            });

            botaoEnviar.on("click", () => {
                perguntarRobo(inputConversa.val());
            });
        }
    }
})();

$(app.init);
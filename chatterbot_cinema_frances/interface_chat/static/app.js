const app = (() => {
    const templatesMensagens = {
        chat: $("#mensagem-chat-template"),
        user: $("#mensagem-user-template"),
        pesquisa: $("#mensagem-pesquisa-template")
    }
    const containerConversa = $("#conversa-chatterbot");
    const inputConversa = $("#conversa-input");
    const botaoEnviar = $("#conversa-enviar-btn");
    const botaoBuscar = $("#buscar-sinopses-btn");
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
            .then(resposta => resposta)
            .fail(resposta => {
                if (resposta.status = 400) {
                    processarFala(templatesMensagens.chat.clone(), resposta.responseJSON.erro);
                } else {
                    Toast.fire({
                        icon: "error",
                        title: "Houve um erro inesperado ao estabelecer à conversa",
                        text: "Por favor, tente novamente."
                    });
                }

                return null;
            }); 
    }

    const processarFala = (mensagemContainer, fala) => {
        mensagemContainer.find(".texto-fala").text(fala);
        containerConversa.append(mensagemContainer);
    }

    const postar_resultados_pesquisa = (mensagemContainer, resultados) => {
        if (resultados) {
            resultados.forEach(el => {
                const sinopseHTML = $(`<li class="list-group-item">
                    <strong>Título:</strong> ${el.titulo}<br>
                    <strong>Informações adicionais:</strong> ${el.info_adicional}<br>
                    <strong>Sinopse:</strong> ${el.sinopse.slice(0, 100)}...<br>
                    <strong>Download:</strong> <a href="#">AQUI</a>
                </li>`);

                mensagemContainer.find(".list-group").append(sinopseHTML);
            });
        } else {
            mensagemContainer.find(".list-group").append(
                `<li class="list-group-item">
                    Infelizmente não houve resultado para a busca realizada. Por favor, tente novamente.
                </li>`
            );
        }

        containerConversa.append(mensagemContainer);
    }

    const processarDialogo = async (fala = null) => {
        const falaEnviar = fala == null ? inputConversa.val() : fala;
        processarFala(templatesMensagens.user.clone(), falaEnviar);
        const resposta = await perguntarRobo(falaEnviar);
        if (resposta == null) return;

        if (resposta.modo == "chat") {
            processarFala(templatesMensagens.chat.clone(), resposta.resposta);
        } else {
            postar_resultados_pesquisa(templatesMensagens.pesquisa.clone(), resposta.sinopses);
        }
        
        inputConversa.val("");
    }

    return {
        init() {
            inputConversa.on("keyup", event => {
                if (event.which != 13) return;

                processarDialogo();
            });

            botaoEnviar.on("click", processarDialogo);
            botaoBuscar.on("click", () => processarDialogo("quero sinopses"));
        }
    }
})();

$(app.init);
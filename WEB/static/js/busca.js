$(document).ready(function () {
    $('.slider').slick({
        dots: true, // exibe as bolinhas de navegação
        arrows: false, // esconde as setas de navegação
        autoplay: true, // ativa o modo autoplay
        autoplaySpeed: 2000 // define a velocidade de transição das imagens
    });



});

function naoApresentar(encontrarPetId, encontrarTutorId) {

    fetch('/nao_apresentar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            encontrar_pet_id: encontrarPetId,
            encontrar_tutor_id: encontrarTutorId
        })
    })
        .then(response => {
            const meuElemento = document.getElementById('card_tutor_'+encontrarTutorId);
            meuElemento.remove();
        })
        .catch(error => {
            console.log("erro");
            // Esconder mensagem de processamento
            modalProcessing.style.display = 'none';


            const modalErro = new bootstrap.Modal(document.getElementById('modalErro'));
            modalErro.show(); // Exibe o modal de erro
        });
}
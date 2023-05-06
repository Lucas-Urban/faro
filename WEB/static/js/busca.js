$(document).ready(function () {
    $('.slider').slick({
        dots: true, // exibe as bolinhas de navegação
        arrows: false, // esconde as setas de navegação
        autoplay: true, // ativa o modo autoplay
        autoplaySpeed: 2000 // define a velocidade de transição das imagens
    });

    window.addEventListener('beforeunload', function () {

        deletarFotos();

    });

});

function deletarFotos() {
    const fotos = document.querySelectorAll(".foto");
    var filesToDelete = [];

    // Itera sobre a lista de imagens e adiciona o atributo 'src' de cada uma ao array
    fotos.forEach((img) => {
        filesToDelete.push(img.getAttribute('src'));
    });

    fetch('/delete_files', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ filesToDelete: filesToDelete })
    });
}

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
            const meuElemento = document.getElementById('card_tutor_' + encontrarTutorId);
            meuElemento.remove();
        })
        .catch(error => {
            console.log("erro");

            const modalErro = new bootstrap.Modal(document.getElementById('modalErro'));
            modalErro.show(); // Exibe o modal de erro
        });
}

function Encontrado(encontrarPetId, encontrarTutorId) {

    fetch('/encontrado', {
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
            location.reload();
        })
        .catch(error => {
            console.log("erro");

            const modalErro = new bootstrap.Modal(document.getElementById('modalErro'));
            modalErro.show(); // Exibe o modal de erro
        });
}


function RemoverEncontrado(encontrarPetId, encontrarTutorId) {

    fetch('/remover_encontrado', {
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
            location.reload();
        })
        .catch(error => {
            console.log("erro");

            const modalErro = new bootstrap.Modal(document.getElementById('modalErro'));
            modalErro.show(); // Exibe o modal de erro
        });
}
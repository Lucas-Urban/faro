$(document).ready(function () {

  // Navbar shrink function
  var navbarShrink = function () {
    const navbarCollapsible = $('body').find('#mainNav');
    if (!navbarCollapsible.length) {
      return;
    }
    if (window.scrollY === 0) {
      navbarCollapsible.removeClass('navbar-shrink')
    } else {
      navbarCollapsible.addClass('navbar-shrink')
    }

  };

  // Shrink the navbar
  navbarShrink();

  // Shrink the navbar when page is scrolled
  $(document).scroll(navbarShrink);

  // Activate Bootstrap scrollspy on the main nav element
  const mainNav = $('body').find('#mainNav');
  if (mainNav.length) {
    new bootstrap.ScrollSpy($('body')[0], {
      target: '#mainNav',
      rootMargin: '0px 0px -40%',
    });
  };

  // Collapse responsive navbar when toggler is visible
  const navbarToggler = $('body').find('.navbar-toggler');
  const responsiveNavItems = $('#navbarResponsive').find('.nav-link');
  responsiveNavItems.each(function () {
    $(this).on('click', () => {
      if (navbarToggler.css('display') !== 'none') {
        navbarToggler.click();
      }
    });
  });

  $('#botaoEncontrarPet').on('click', function () {
    const cadastrarPetModal = new bootstrap.Modal($('#modalEncontrarPet')[0]);
    cadastrarPetModal.show();
  });

  $('#enviarPet').on('click', function () {

    // Verifica se os campos obrigatórios foram preenchidos
    if (!$('#inputLocalPet').val() || !$('#inputNomeTutor').val() || !$('#inputEmailTutor').val() || !$('#inputTelefoneTutor').val()) {
      // Exibe mensagem de erro e sai da função
      alert('Por favor, preencha todos os campos obrigatórios.');
      return;
    }

    const formData = new FormData();
    formData.append('inputNomePet', $('#inputNomePet').val());
    formData.append('inputLocalPet', $('#inputLocalPet').val());

    // Loop através dos arquivos selecionados e adiciona-los ao formData
    const files = $('#inputFotoPet')[0].files;
    for (var i = 0; i < files.length; i++) {
      formData.append('inputFotoPet[]', files[i]);
    }

    formData.append('inputNomeTutor', $('#inputNomeTutor').val());
    formData.append('inputEmailTutor', $('#inputEmailTutor').val());
    formData.append('inputTelefoneTutor', $('#inputTelefoneTutor').val());

    // Mostrar mensagem de processamento
    $('.modal-processing').show();

    fetch('encontrar_pet', {
      method: 'POST',
      body: formData
    })
      .then(response => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error('Erro ao enviar requisição');
        }
      })
      .then(data => {
        // Esconder mensagem de processamento
        $('.modal-processing').hide();

        // Exibe a mensagem de sucesso na tela
        $('#mensagemSucesso').text(data['mensagem']);
        $('[data-bs-dismiss="modal"]').closest('.modal').modal('hide');
        const modalSucesso = new bootstrap.Modal($('#modalSucesso')[0])
        modalSucesso.show()
      })
      .catch(error => {
        // Esconder mensagem de processamento
        $('.modal-processing').hide();

        // Exibe a mensagem de erro na tela
        $('#mensagemErro').text(error['mensagem']);
        $('#modalEncontrarPet').show();
        $('#modalErro').addClass('show');
      });
  });

});
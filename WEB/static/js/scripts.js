document.addEventListener("DOMContentLoaded", function () {

  // Navbar shrink function
  var navbarShrink = function () {
    const navbarCollapsible = document.querySelector('#mainNav');
    if (!navbarCollapsible) {
      return;
    }
    if (window.scrollY === 0) {
      navbarCollapsible.classList.remove('navbar-shrink');
    } else {
      navbarCollapsible.classList.add('navbar-shrink');
    }

  };

  // Shrink the navbar
  navbarShrink();

  // Shrink the navbar when page is scrolled
  document.addEventListener('scroll', navbarShrink);

  // Activate Bootstrap scrollspy on the main nav element
  const mainNav = document.querySelector('#mainNav');
  if (mainNav) {
    new bootstrap.ScrollSpy(document.body, {
      target: '#mainNav',
      rootMargin: '0px 0px -40%',
    });
  }

  const botaoEncontrarPet = document.getElementById('botaoEncontrarPet');
  const encontrarPetModal = document.getElementById('modalEncontrarPet');

  botaoEncontrarPet.addEventListener('click', function () {
    const modal = new bootstrap.Modal(encontrarPetModal);
    modal.show();
  });

  const botaoPetEncontrado = document.getElementById('botaoPetEncontrado');
  const petEncontradoModal = document.getElementById('modalPetEncontrado');

  botaoPetEncontrado.addEventListener('click', function () {
    const modal = new bootstrap.Modal(petEncontradoModal);
    modal.show();
  });

  // Collapse responsive navbar when toggler is visible
  const navbarToggler = document.querySelector('.navbar-toggler');
  const responsiveNavItems = document.querySelectorAll('#navbarResponsive .nav-link');
  responsiveNavItems.forEach(function (item) {
    item.addEventListener('click', () => {
      if (navbarToggler.style.display !== 'none') {
        navbarToggler.click();
      }
    });
  });


  const enviarPetButton = document.getElementById('enviarPet');
  enviarPetButton.addEventListener('click', function () {
    encontrarPet();
  });


});


function initMap() {
  // Cria um novo objeto autocomplete para cada campo de endereço
  const inputLocalPet = document.getElementById('inputLocalPet');
  const autocompleteLocalPet = new google.maps.places.Autocomplete(inputLocalPet, {
    componentRestrictions: { country: 'BR' } // restringe as sugestões de endereços para o Brasil
  });

  // Adiciona um listener para atualizar a latitude e longitude do pet quando o endereço é selecionado
  autocompleteLocalPet.addListener('place_changed', () => {
    const place = autocompleteLocalPet.getPlace();
    const latLocalPet = document.getElementById('latLocalPet');
    const longLocalPet = document.getElementById('longLocalPet');

    // Define os valores dos campos latLocalPet e longLocalPet
    if (place.geometry) {
      latLocalPet.value = place.geometry.location.lat();
      longLocalPet.value = place.geometry.location.lng();
    }
  });

  inputLocalPet.setAttribute("autocomplete", "new-password");

  // Cria um novo objeto autocomplete para cada campo de endereço
  const inputLocalPetEncontrado = document.getElementById('inputLocalPetEncontrado');
  const autocompleteLocalPetEncontrado = new google.maps.places.Autocomplete(inputLocalPetEncontrado, {
    componentRestrictions: { country: 'BR' } // restringe as sugestões de endereços para o Brasil
  });

  // Adiciona um listener para atualizar a latitude e longitude do pet quando o endereço é selecionado
  autocompleteLocalPetEncontrado.addListener('place_changed', () => {
    const place = autocompleteLocalPetEncontrado.getPlace();
    const latLocalPetEncontrado = document.getElementById('latLocalPetEncontrado');
    const longLocalPetEncontrado = document.getElementById('longLocalPetEncontrado');

    // Define os valores dos campos latLocalPetEncontrado e longLocalPetEncontrado
    if (place.geometry) {
      latLocalPetEncontrado.value = place.geometry.location.lat();
      longLocalPetEncontrado.value = place.geometry.location.lng();
    }
  });

  inputLocalPetEncontrado.setAttribute("autocomplete", "new-password");

}


function encontrarPet() {

  const inputLocalPet = document.getElementById('inputLocalPet').value;
  const inputNomeTutor = document.getElementById('inputNomeTutor').value;
  const inputEmailTutor = document.getElementById('inputEmailTutor').value;
  const inputTelefoneTutor = document.getElementById('inputTelefoneTutor').value;
  const inputFotoPet = document.getElementById('inputFotoPet').value;

  if (!inputLocalPet || !inputNomeTutor || !inputEmailTutor || !inputTelefoneTutor || !inputFotoPet) {
    // Exibe mensagem de erro e sai da função
    alert('Por favor, preencha todos os campos obrigatórios.');
    return;
  }

  const formData = new FormData();
  formData.append('inputNomePet', document.getElementById('inputNomePet').value);
  formData.append('inputLocalPet', inputLocalPet);

  // Loop através dos arquivos selecionados e adiciona-los ao formData
  const files = document.getElementById('inputFotoPet').files;
  for (var i = 0; i < files.length; i++) {
    formData.append('inputFotoPet[]', files[i]);
  }

  formData.append('inputNomeTutor', inputNomeTutor);
  formData.append('inputEmailTutor', inputEmailTutor);
  formData.append('inputTelefoneTutor', inputTelefoneTutor);

  // Mostrar mensagem de processamento
  const modalProcessing = document.querySelector('.modal-processing');
  modalProcessing.style.display = 'block';

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
      // Limpar campos do formulário
      document.getElementById('inputNomePet').value = '';
      document.getElementById('inputLocalPet').value = '';
      document.getElementById('inputNomeTutor').value = '';
      document.getElementById('inputEmailTutor').value = '';
      document.getElementById('inputTelefoneTutor').value = '';
      document.getElementById('inputFotoPet').value = '';
 
      // Esconder mensagem de processamento
      modalProcessing.style.display = 'none';

      // Exibe a mensagem de sucesso na tela
      const mensagemSucesso = document.getElementById('mensagemSucesso');
      mensagemSucesso.textContent = data['mensagem'];
      const modalEncontrarPet = document.getElementById('modalEncontrarPet');
      modalEncontrarPet.querySelector('[data-bs-dismiss="modal"]').click();
      const modalSucesso = new bootstrap.Modal(document.getElementById('modalSucesso'));
      modalSucesso.show();
    })
    .catch(error => {
      console.log("erro");
      // Esconder mensagem de processamento
      modalProcessing.style.display = 'none';


      const modalErro = new bootstrap.Modal(document.getElementById('modalErro'));
      modalErro.show(); // Exibe o modal de erro
    });
}
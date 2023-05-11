obj = document.querySelector('span[class="cross noselect"]')
wrapper = obj.closest('[id=share_success]')

function share_success_hidden() {
    wrapper.style.display = 'none'
}

obj.addEventListener('click', share_success_hidden)
let comment_message_set = document.querySelectorAll(".comment_message")
let comment_message_less_set = document.querySelectorAll(".comment_message_less")

for (let comment_message of comment_message_set) {
    comment_message.addEventListener('click', read_more_handler)
}
for (let comment_message_less of comment_message_less_set) {
    comment_message_less.addEventListener('click', show_less_handler)
}

function read_more_handler() {
    // no display
    this.closest("[class=comment_item__content]").classList.add('no_display')
    // display
    this.parentNode.parentNode.querySelector('.comment_item__full_content')
        .classList.remove('no_display')
}
function show_less_handler() {
    // no display
    this.closest(".comment_item__full_content").classList.add('no_display')
    // display
    this.parentNode.parentNode.querySelector(".comment_item__content")
        .classList.remove('no_display')
}
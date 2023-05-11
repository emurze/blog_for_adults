let comment_form = document.querySelector(".comment_form")
let comment_form_link_below = document.getElementById("id_comment_form")
let comment_form_link_above = document.querySelector(".comment_form_link")

comment_form_link_below.addEventListener('click', comment_drag_below)
comment_form_link_above.addEventListener('click', comment_drag_above)

function comment_drag_above() {
    comment_form.classList.remove("no_display")
    comment_form.scrollIntoView(false)
    window.scrollBy(0, 480)
}

function comment_drag_below() {
    comment_form.classList.toggle("no_display")
}
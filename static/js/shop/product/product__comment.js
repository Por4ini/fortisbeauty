function radioShowBlock(object) {
    let radio = document.querySelectorAll('input[type="radio"][name="comments"]')
    for (let i = 0; i < radio.length; i++) {
        let el = radio[i];
        let block = document.getElementById(el.dataset.block)
        if (el.id == object.id) {
            block.classList.add('active')
        } else {
            block.classList.remove('active')
        }
    }
}
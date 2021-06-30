function DropDownWithImgs(select) {
    let options = select.querySelector('.options')
    let title = select.querySelector('.title')
    let li = select.querySelectorAll('li')
    
    title.addEventListener('click', function() {
        if (options.style.visibility == 'visible') {
            options.style.visibility = 'hidden'
        } else if (options.style.visibility == 'hidden') {
            options.style.visibility = 'visible'
        } else {
            options.style.visibility = 'visible'
        } 
    })
    
    for (let i = 0; i < li.length; i++) {
        // IMG
        let img = document.createElement("img");
        img.setAttribute("src", li[i].dataset.img);
        // SPAN
        let span = document.createElement("span");
        span.innerHTML = li[i].dataset.text
        // ADD
        li[i].appendChild(img)
        li[i].appendChild(span)
        if (li[i].dataset.selected == 'true') {
            title.innerHTML = li[i].innerHTML
        }
        // 
        li[i].addEventListener('click', function() {
            let el = li[i]
            title.innerHTML = el.innerHTML
            options.style.visibility = 'hidden'
            // SET ONE SELECTED
            for (let j = 0; j < li.length; j++) {
                if (li[j].dataset.value == li[i].dataset.value) {
                    li[j].dataset.selected == 'true'
                } else {
                    li[j].dataset.selected == 'false'
                }
            }
            // SHOW DIVS
            let id = el.dataset.div
            select.querySelector('input.hidden').value = id
            let div = document.getElementById(id) 
            if (div != null) {
                let divs = document.getElementsByClassName(div.classList[0]) 
                for (let j = 0; j < divs.length; j++) {
                    if (divs[j].id == id) {
                        divs[j].style.display = 'block'
                        divs[j].dataset.selected = 'true'
                    } else {
                        divs[j].style.display = 'none'
                        divs[j].dataset.selected = 'false'
                    }
                }
            }

            



        })
    }
}
let select = document.querySelectorAll('.select')
for (let i = 0; i < select.length; i++) {
    DropDownWithImgs(select[i])
}
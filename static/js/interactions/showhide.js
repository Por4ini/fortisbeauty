for (let showhide of document.querySelectorAll('.showhide__button')) {
    showhide.onchange = (e) => {
        if (showhide.checked) {
            let listener = (e) => {
                let block = document.querySelector(showhide.dataset.for)
                let nodes = Array.from(block.querySelectorAll("*"))
                    nodes.push(block)
                if (!nodes.includes(e.target)) {
                    document.removeEventListener('click', listener, false);
                    showhide.checked = false
                }
            }
            document.addEventListener('click', listener, false)
        }
        
    }
}
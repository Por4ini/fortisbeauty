var timeout = null;

function Counter() {
    for (let counter of document.querySelectorAll('.counter')) {
       
        let actions = counter.querySelectorAll('.action')
        let input = counter.querySelector('input')

        function multiplyPrice(quantity) {

            if (quantity <= input.max && quantity >= input.min) {
                input.value = quantity
                
                if (input.dataset.priceClass) {
                    for (let price of document.getElementsByClassName(input.dataset.priceClass)) {
                        price.innerHTML = parseInt(price.dataset.value) * parseInt(quantity)
                    }
                }
            } 
            else if (quantity > input.max) { input.value = input.max } 
            else { input.value = 1 }

            // Add to cart
            if (input.dataset.cart == 'true') {
                let data = {
                    'id' :       input.dataset.variantId, 
                    'quantity' : input.value,
                }
                if (timeout !== null) {
                    clearTimeout(timeout);
                }
                timeout = setTimeout(function () { addToCartRequest(data) }, 350);
            }

           
        } 

        for (let action of actions) {
            action.onclick = () => {
                if (action.classList.contains('plus'))  { multiplyPrice(parseInt(input.value) + 1) }
                if (action.classList.contains('minus')) { multiplyPrice(parseInt(input.value) - 1) }
            }
        }
        input.oninput = () => { multiplyPrice(parseInt(input.value)) }

        input.onchange = () => {}
    }
} Counter()



var timer


function CartRender(data) {
    for (let productsList of side_cart_products) {
        productsList.innerHTML = data['html']
    }
    for (let total of document.querySelectorAll('.cart_total')) {
        total.innerHTML = data['total']
    }
    for (let quantity of document.querySelectorAll('.cart_quantity')) {
        let qty = parseInt(data['quantity']) 
        if (qty < 1000) {
            quantity.innerHTML = qty
        } else {
            quantity.innerHTML = '1000+'
        }
        
    }
    
  
    if (data['quantity'] == 0) {
        closeCart()
        if (curentPage.includes('order')) {
            window.location.href = cartUrls['home']
        }
    } else {
        if (!curentPage.includes('order')) {
            openCart()
        }
    }
    Counter()
    
}


function CartAdd(input) {
    let url = cartUrls['cart_add']
    data = {
        product_id : input.dataset.product_id,
        quantity :   input.value,
        update:     false,
    }
    data = JSON.stringify(data)
    XHR('POST', url, data, func=CartRender)
}
function CartAddID(id) {
    let url = cartUrls['cart_add']
    data = {
        product_id : id,
        quantity :   1,
        update:     false,
    }
    data = JSON.stringify(data)
    popupClose()
    XHR('POST', url, data, func=CartRender)
}
function CartRemoveID(id) {
    let url = cartUrls['cart_remove']
    data = {
        product_id : id,
    }
    data = JSON.stringify(data)
    XHR('POST', url, data, func=CartRender)
}

function CartUpdate(input) {
    let url = cartUrls['cart_add']
    data = {
        product_id : input.dataset.product_id,
        quantity :   input.value,
        update:     true,
    }
    data = JSON.stringify(data)
    XHR('POST', url, data, func=CartRender)
}
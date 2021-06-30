var timer_wishlist
function CartUpdateQuntity(product_id, variant_id, quantity, update=true) {
    url = baseUrl + '/wishlist/update'
    data = {
        'product_id' : product_id,
        'variant_id' : variant_id,
        'quantity' : quantity,
        'update'   : update,
    }
    method = 'POST'
    // TIMER
    window.clearTimeout(timer_wishlist)
    timer_wishlist = window.setTimeout(XHR, 500, method, url, data);
}

function WishlistRemoveItem(object) {
    item = GetItem(object)
    url = baseUrl + '/wishlist/delete'
    data = {
        'variant_id' : item.dataset.variant_id,
    }
    method = 'POST'
    CartRequest(method, url, data)
}


function CartClear(object) {
    url = baseUrl + '/wishlist/clear'
    data = ''
    method = 'POST'
    CartRequest(method, url, data)
}




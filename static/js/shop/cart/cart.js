function cartUpdater(data) {
    let cartSidebar = document.getElementById('sidebar_cart') 
    let main = cartSidebar.querySelector('.main')
    // Set products
    let ul = main.querySelector('ul')
        ul.innerHTML = data.items
    // Set actions
    let actions = cartSidebar.querySelector('.actions') 
        actions.innerHTML = data.total
    // Set quntity
    let quantity = document.querySelector('.cart__quantity')
    data.quantity < 100 ? 
    quantity.innerHTML = data.quantity :
    quantity.innerHTML = ':D'


    if (data.order_items) {
        const orderProductsList = document.querySelector('.products__list')
        if (orderProductsList) {
            orderProductsList.innerHTML = data.order_items
        }
        const orderTotalNum = document.querySelector('.order__total__num')
        if (orderTotalNum) {
            orderTotalNum.innerHTML = data.amount
        }
    }
    Counter()
    try {
        calculateDelivery()
    } catch {}
    
}


function cartRequest(url, data) {
    const isOrderPage = window.location.pathname.includes('/order')
    fetch(url, {
        method : 'POST',
        headers : {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrf.value,
        },
        body : JSON.stringify(data) 
    })
    .then(res => res.json())
    .then(json => {
        cartUpdater(json)
        if (!isOrderPage) {
            SidebarOpen('sidebar_cart')
        }
        
    })
}


const addToCartRequest = (data) => {
    if (window.location.pathname.includes('/order')) {
        data.order = true
    }
    cartRequest(url_cart_add, data)
}


function removeFromCart(obj) {
    const data = {id : obj.dataset.id}
    if (window.location.pathname.includes('/order')) {
        data.order = true
    }
    cartRequest(url_cart_delete, data)
}


const getCartData = () => {
    let url = url_cart_data
    if (window.location.pathname.includes('/order')) {
        url += "?order=true"
    }
    fetch(url, {method : 'GET'})
    .then(res => res.json())
    .then(json => cartUpdater(json))
}
getCartData()

function addToCart(obj) {
    data = {id: parseInt(obj.dataset.id)}
    cartRequest(url_cart_add, data)
}


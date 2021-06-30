function updateWishlist(wishlist) {
    if (wishlist.html) {
        for (let productsList of document.querySelectorAll('.wishlist__products')) {
            productsList.innerHTML = wishlist.html
        }
    }
    if (wishlist.total) {
        for (const wishlistQty of document.querySelectorAll('.header__wishlist-qty')) {
            wishlistQty.innerHTML = wishlist.total
        }

    }
}

const WishlistToCart = (obj) => {
    SidebarClose('sidebar_wishlist')
    addToCart(obj)
}

const AddToWishlist = (obj) => {
    const id = obj.dataset.id
    fetch(`${WishlistUrl}add/${id}/`, {method : 'GET'})
    .then(res => res.json())
    .then(json => {
        json.wishlist && updateWishlist(json.wishlist)
        SidebarOpen('sidebar_wishlist')
    })
}

const RemoveFromWishlist = (id) => {
    fetch(`${WishlistUrl}delete/${id}/`, {method : 'GET'})
    .then(res => res.json())
    .then(json => {
        json.wishlist && updateWishlist(json.wishlist)
        SidebarOpen('sidebar_wishlist')
    })
}


// const InitWishlist = () => {
//     for (let wishButton of document.querySelectorAll('.add-to-wishlist')) {
//         wishButton.onclick = (e) => {
//             e.preventDefault()
//             const wishId = wishButton.dataset.id
//             AddToWishlist(wishId)
//         }
//     }
// } 
// InitWishlist()



const GetWishlistData = () => {
    fetch(WishlistUrl, {method : 'GET'})
    .then(res => res.json())
    .then(json => {
        if (json.wishlist) {
            updateWishlist(json.wishlist)
        }
    })
}
GetWishlistData()

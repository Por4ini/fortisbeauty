const watchlist = document.querySelector('.watchlist')

fetch(WatchlistUrl, {method : 'GET'})
.then(res => res.json())
.then(json => {
    if (json.watchlist) {
        watchlist.innerHTML = json.watchlist
        initSwiperProductList(watchlist)
        new LazyLoad({container: watchlist});
    }
})
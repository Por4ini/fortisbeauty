function initSwiperProductList(productList)  {
    let slider = productList.querySelector('.swiper-container')
        let buttonPrev = productList.querySelector('.button_prev')
        let buttonNext = productList.querySelector('.button_next')

        if (slider) {
            new Swiper(slider, {
                slidesPerView: 6,
                spaceBetween: 32,
                slidesPerGroup: 5,
                // centerInsufficientSlides: true,
                observer : true,
                observeParents: true,
                observeSlideChildren: true,
                loop: false,
                loopFillGroupWithBlank: true,
                breakpointsInverse: true,
                breakpoints: {
                    0 :    { slidesPerView: 2, slidesPerGroup: 2, spaceBetween: 16},
                    640 :  { slidesPerView: 3, slidesPerGroup: 3, spaceBetween: 24},
                    960 :  { slidesPerView: 4, slidesPerGroup: 4, spaceBetween: 24},
                    1200 :  { slidesPerView: 5, slidesPerGroup: 5, spaceBetween: 32},
                    1600 : { slidesPerView: 6, slidesPerGroup: 6, spaceBetween: 32 },
                },
                navigation: { 
                    prevEl: buttonPrev, 
                    nextEl: buttonNext, 
                },
            });
        }
}



 for (let productList of document.querySelectorAll('.home__products')) {
    initSwiperProductList(productList)
}
    

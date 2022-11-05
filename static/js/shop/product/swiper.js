
const productGalerySwiper = () => {
  const productGalery = document.querySelector('.product__galery')
  // new LazyLoad({container: productGalery});

  new Swiper(productGalery, {
    pagination: {
      el: '.swiper-pagination',
    },
    navigation: {
      nextEl:  productGalery.querySelector('.swiper-button-next'),
      prevEl:  productGalery.querySelector('.swiper-button-prev'),
    },
    scrollbar: {
      el: '.swiper-scrollbar',
    },
  });
} 
productGalerySwiper()
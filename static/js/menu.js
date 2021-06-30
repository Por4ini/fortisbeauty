var menu = new MmenuLight( document.querySelector('#menu'), {
    title: 'Каталог',
    theme: 'light',// 'dark'
    slidingSubmenus: true,// false
    selected: 'Selected'
});
menu.enable( 'all' ); // '(max-width: 900px)'
menu.offcanvas({
    position: 'left',
    // move: true,// false
    // blockPage: true,// false / 'modal'
});

//	Open the menu.
document.querySelector( 'a[href="#menu"]' )
    .addEventListener( 'click', ( evnt ) => {
        menu.open();
        alert(0)
        //	Don't forget to "preventDefault" and to "stopPropagation".
        evnt.preventDefault();
        evnt.stopPropagation();
    });



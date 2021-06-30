const popupWrapper = document.querySelector('.popup__wrapper')
const popup = popupWrapper.querySelector('.popup')
const popupHeading = popup.querySelector('.heading')
const popupContent = popup.querySelector('.data')


const openPopUp = () => {
    popupWrapper.classList.add('active')
}


const cloesPopUp = () => {
    popupWrapper.classList.remove('active')
    popupHeading.innerHTML = ''
    popupContent.innerHTML = ''
}


for (let closeBtn of document.querySelectorAll('.close__popup')) {
    closeBtn.onclick = () => {
        cloesPopUp()
    }
}


popupWrapper.onclick = (e) => {
    const target = e.target
    if (! popup.contains(target)) {
        popupWrapper.classList.remove('active')
    }  
}
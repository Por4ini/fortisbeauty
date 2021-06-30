const popupOuter = document.querySelector('.outer')

// CLICK ON CLOSE
function SidebarClose() {
    let objectId = popupOuter.dataset.objectId
    let object = document.getElementById(objectId)
    if (object) {
        object.classList.remove('active')
        popupOuter.classList.remove('active')
    }
}
// OPEN SIDEBAR
function SidebarOpen(id) {
    let sidebar = document.getElementById(id)
    sidebar.classList.add('active')
    popupOuter.dataset.objectId = sidebar.id
    popupOuter.classList.add('active')
    
}

// CLICK ON OUTER

popupOuter.addEventListener('click', function(event) {
    SidebarClose()
})

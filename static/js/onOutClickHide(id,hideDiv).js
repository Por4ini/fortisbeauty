// OUT CLICK HIDE
function onOutClickHide(id,hideDiv) {
    document.addEventListener("click", (evt) => {
    const flyoutElement = document.getElementById(id);
    let targetElement = evt.target; // clicked element

    do {
        if (targetElement == flyoutElement) {
            // Do nothing, just return.
            return;
        }
        // Go up the DOM.
        targetElement = targetElement.parentNode;
    } while (targetElement);

    // Do something useful here.
    document.getElementById(hideDiv).style.display = 'none'
    });
}

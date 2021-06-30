function GetParentByClassName(object, parent_name) {
    let parent = object.parentElement
    while (true) {
        if (parent.classList.contains(parent_name)) {
            return parent
        }
        parent = parent.parentElement
    }
}
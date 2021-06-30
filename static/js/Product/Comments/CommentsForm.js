const addComment =   document.querySelector('.add-comment')
const addQuestion =  document.querySelector('.add-question')
const commentsList = document.querySelector('.comments')
const questionsList = document.querySelector('.questions')
const replyLink =    document.querySelectorAll('.reply_comment') 



const initReply = () => {
    for (let link of document.querySelectorAll('.reply_comment') ) {
        link.onclick = (e) => {
            e.preventDefault()
            openCommentForm(link.href);
        }
    }
}
initReply()



const activateCommentForm = (form) => {
    const isLogin = form.action.includes('/login/')
    if (!isLogin) {
        form.onsubmit = (e) => {
            e.preventDefault()
            const formData = new FormData(form)
            fetch(form.action, {
                method : "POST",
                body : formData
            })
            .then(res => res.json())
            .then(json => {
                if (json.comments) {
                    commentsList.outerHTML = json.comments
                }
                if (json.questions) {
                    questionsList.outerHTML = json.questions
                }
                initReply()
            })
            .catch(err => {alert('Что-то пошло не так. Ошибка ' + err.status)})
            cloesPopUp()
            
        } 
    }
   
}





const openCommentForm = (url) => {
    openPopUp()
    popupContent.innerHTML = ''
    fetch(url, {method : 'GET'})
    .then(res => res.json())
    .then(json => {
        if (json.form) {
            popupContent.innerHTML = json.form
            
            let form = popupContent.querySelector('form')
            activateCommentForm(addCSRF(form))
        }
        if (json.heading) {
            popupHeading.innerHTML = json.heading
        }
        initReply()
    })
}

addComment.onclick = () => {
    openCommentForm(commentFomtFetchUrl)
}
addQuestion.onclick = () => {
    openCommentForm(questionsFomtFetchUrl)
}



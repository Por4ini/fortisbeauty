var currnetForm = null


validation = {
    email :{
        errors : {
            re : /^[-!#$%&'*+/0-9=?A-Z^_a-z{|}~](\.?[-!#$%&'*+/0-9=?A-Z^_a-z{|}~])*@[a-zA-Z](-?[a-zA-Z0-9])*(\.[a-zA-Z](-?[a-zA-Z0-9])*)+$/,
            length : 0,
        },
        msg : {
            re : 'Email має невірний формат',
            length : 'Введіть ваш Email', 
        },
        replace : /[^0-9a-zA-Z._@-]/g,
    },
    text : {
        errors : {
            re : (http|https):\/\/,
            length : 0,
        },
        msg : {
            re : ''
            length : 'Це поле не може бути порожнім', 
        },
    },
    text_only : {
        errors : {
            re : (http|https):\/\/,
            length : 0,
        },
        msg : {
            re : ''
            length : 'Це поле не може бути порожнім',
        },
        replace : /[^a-zA-ZА-Яа-яіїє]/g
    },
    number : {
        errors : {
            length : 0,
        },
        msg : {
            length : 'Це поле не може бути порожнім', 
        },
        replace : /[^0-9.]/g
    },
    phone : {
        errors : {
            length : 7,
        },
        msg : {
            length : 'Це поле не може бути порожнім', 
        },
        replace : /[^+ 0-9.]/g
    },
   
    password : {
        errors : {
            re : /^[0-9a-zA-Z]{6,}$/,
            length : 6,
        },
        msg : {
            re : 'Пароль має неправильний формат',
            length : 'Пароль не може бути менше 6-ти символів латиниці та цифр', 
        },
        replace : /[^0-9a-zA-ZА]/g
    },
    password2 : {
        errors : {
            func : inputTypePassvord2Valid,
        },
        msg : {
            func : 'Паролі не співпадають', 
        },
        replace : /[^0-9a-zA-ZА]/g
    },
    radio : {
        errors : {
            func : inputTypeRadioValid,
        },
        msg : {
            func : 'Виберіть один із варіантів.'
        }
    }
}


function inputTypeRadioValid(input) {
    let name = input.name
    let inputs = document.querySelectorAll('input[type=radio][name=' + name + ']')
    for (let input of inputs) {
        if (input.checked) {
            return true
        }
    }
    return false
}


function inputTypePassvord2Valid(input) {
    let input1 = document.querySelector('#'+input.dataset.parent)
    let input2 = input
    if (input1.value == input2.value) {
        return true
    } 
    return false
}

function showMsg(input, errors=[]) {
    let parent = input.parentElement
    let msg = parent.querySelector('.msg')

    if (errors.length == 0) {
        msg.innerHTML = ''
        msg.classList.remove('active')
    } else {
        msg.innerHTML = ''
        for (let i = 0; i < errors.length; i++) {
            let err = errors[i];
            msg.innerHTML += err
            if (i < errors.length - 1) {
                msg.innerHTML += ', '
            }
        }
        msg.classList.add('active')
    }
    
}


function fieldValidate(input) {
    errors = []
    err_keys = []
    let validator = validation[input.dataset.type]
    
    // LENGTH
    if ('length' in validator['errors']) {
        let length = validator['errors']['length']
        if (input.value.length <= length) {
            if (input.dataset.empty) {
                errors.push(input.dataset.empty)
            } else {
                errors.push(validator['msg']['length'])
            }
            err_keys.push('length')
        }
    }
    // RE
    if (err_keys.includes('length') == false) {
        if ('re' in validator['errors']) {
            let re = validator['errors']['re']
            if (re.test(input.value) == false) {
                errors.push(validator['msg']['re'])
            }
        }
    }
   
    // FUNCTION
    if ('func' in validator['errors']) {
        let func = validator['errors']['func']
        if (func(input) == false) {
            errors.push(validator['msg']['func'])
        }
    }
    // REPLACE
    if ('replace' in validator) {
        let re = validator['replace']
        let value = input.value.replace(re, '');
        input.value = value
    }
    showMsg(input, errors)
    const parentNode = input.parentNode

    if (errors.length > 0) {
        currnetForm.dataset.valid = false
        input.dataset.valid = false
        input.classList.add('err')
        return false
    } else {
        currnetForm.dataset.valid = true
        input.classList.remove('err')
        input.dataset.valid = true
        return true
    }
}




function checkInputType(input) {
    let type = input.dataset.type
    if (type in validation && input.required == true) {
        validation[type]
        return fieldValidate(input)
    } 
    return true
}





function formResponse(form, data) {
    let submitBtn = form.querySelector('button[type=submit]')
    submitBtn.classList.add('load')
    const formData = new FormData(form)

    fetch(form.action, {
        method : "POST", 
        body : formData
    })
    .then(res => res.json())
    .then(json => {
        console.log(json);
    })


    submitBtn.classList.remove('load')
   
    if ('update_func' in form.dataset && response['data'] !== undefined ) {
        if (response['success'] == true) {
            let data = response['data']
            form = this[form.dataset.update_func](data, true)
        }
    }

    if (form != undefined) {
        message = form.querySelector('.message')
        if (message) {
            message.classList.add('active')
            message.innerHTML = response['msg']
            if (response['success'] == true) {
                message.classList.add('success')
            } else {
                message.classList.remove('success')
            }
        }
        if (response['success'] == true && form.dataset.redirect !== undefined) {
            window.location.href = form.dataset.redirect
        }
    }

    
    
    
}

function AjaxFieldChanged(data, field=undefined) {
    data = JSON.parse(data)['data']['list']
    if (data.length == 1) {
        field.value = data[0]
        document.querySelector('.ajax_input_values_list').remove()
    } else if (data.includes(field.value) == false) {
        field.value = ''
        alert('Виберіть значення зі списку доступних')
    }
}

function AjaxFieldOnChange(e) {
    input = e.target
    xhrOnLoad('POST', input.dataset.ajax, data, AjaxFieldChanged, input)
}


function AjaxFieldUpdate(data, field=undefined) {
    data = JSON.parse(data)['data']
    if (field) {
        parent = field.parentElement
        ul = parent.querySelector('ul')
        if (ul == undefined) {
            ul = document.createElement('ul')
            parent.appendChild(ul)
        } 
        ul.innerHTML = ''
        ul.classList.add('ajax_input_values_list')
        for (let item of data['list']) {
            li = document.createElement('li')
            li.innerHTML = item
            ul.appendChild(li)
        }
        let list = ul.querySelectorAll('li')
        function set_value(value) {
            field.removeEventListener('change', AjaxFieldOnChange, false)
            field.value = value
            checkInputType(field)
            ul.remove()
        }

        for (let li of list) {
            li.addEventListener('mousedown',  function () { set_value(li.innerHTML) }, false )
        }
        field.removeEventListener('change', AjaxFieldOnChange, false)
        field.addEventListener('change', AjaxFieldOnChange, false)

        function set_active(n, enter=false) {
            if (n == -1 && enter==true && list.length > 0) {
                set_value(list[0].innerHTML)
            }
            for (let i = 0; i < list.length; i++) {
                let li = list[i];
                if (i == n) { 
                    li.classList.add('active') 
                    if (enter == true) {
                        set_value(li.innerHTML)
                    }
                }
                else {li.classList.remove('active') }
            }
        }
    
        let num = -1
        let max_num = list.length - 1

        function keyDown(e) {
            if (e.key == 'ArrowDown') { 
                if (num + 1 <= max_num) { num += 1; set_active(num) } }
            if (e.key == 'ArrowUp') { 
                if (num - 1 >= 0)       { num -= 1; set_active(num) } }
            if (e.key === "Enter") {
                e.preventDefault();
                set_active(num , true);
                document.removeEventListener('keydown', keyDown, false);
            }
        }
        document.addEventListener('keydown', keyDown, false);
    }
}


function formToDict(form) {
    let data = {}
   
    for (let input of form.fields) {
        if (input.required && input.dataset.valid == 'false') {
            errs.push(input.name)
        } 
        if (input.type == 'radio') {
            if (input.checked) {
                data[input.name] = input.value
            }
        } else {
            data[input.name] = input.value
        }
    }
    return data
}

function formOnSubmit(form) {
    errs = 0
    
    for (let input of form.querySelectorAll('input')) {
        input.classList.remove('virgin')
        if (checkInputType(input) == false) {
            errs += 1
        }
    }
    
    let message = form.querySelector('.message')
    if (message) {
        message.innerHTML = ""
        if (errs == 0) {
            form.valid = true
            message.innerHTML = ""
            message.classList.remove('active')
        } else {
            message.innerHTML = "Заповніть форму коректно"
            message.classList.add('active')
        }
    }
    if (errs == 0) {
        return true
    }
    return false
}



function formInputsValidate(form) {
    form.valid = false
    form.active = false

    for (let input of form.querySelectorAll('input')) {
       
        if (!['search','radio','checkbox','hidden'].includes(input.type) && !input.classList.contains('hidden')) {
            
            if (input.dataset.type == undefined) {
                console.log('No dataset type: ',input);
                input.style.backgroundColor = 'red'
            } 

            if (input.name == "" || input.name == undefined) {
                console.log('No name attr: ',input);
                input.style.backgroundColor = 'red'
            } 
            input.dataset.valid = false
            input.classList.add('virgin')

            if (input.required) {
                let msg = document.createElement('p')
                msg.classList.add('msg')
                msg.innerHTML = ''
                input.after(msg)
            }

            input.onchange = (e) => { 
                checkInputType(input) 
                input.classList.remove('virgin')
                if ('ajax' in input.dataset) {
                    input.addEventListener('change', AjaxFieldOnChange, false)
                }
            }

          
            input.oninput = (e) =>  { 
                checkInputType(input) 
                if ('ajax' in input.dataset) {
                    data = JSON.stringify({'name' : input.value})
                    xhrOnLoad('POST', input.dataset.ajax, data, AjaxFieldUpdate, input)
                  
                }
            }
        }
    }


}





function formValidate(form) {
    form.valid = false
    form.active = false

    form.onclick = () => { 
        if (currnetForm != form) {
            currnetForm = form
            formInputsValidate(form) 
        }
        
    }
    form.onsubmit = (e) => { 
        if (!formOnSubmit(form)) {
            e.preventDefault()
        } else {
            if (form.dataset.onsubmit) {
                e.preventDefault()
                if (window.hasOwnProperty(form.dataset.onsubmit)) {
                    const Func = window[form.dataset.onsubmit]
                    Func(form)
                } else {
                    alert('Submit function is undefined')
                }
            }
        }
        
    }

    
}
    

// GET ALL FORMS ON PAGE
const FormValidation = () => {
    for (let form of document.querySelectorAll('form.validate')) {
        if (form) {
         formValidate(form)
         form.noValidate = true
        }
     }
} 
FormValidation()


// SHOW PASSWORD
for (let obj of document.querySelectorAll('.show_password')) {
    obj.onclick = () => {
        let parent = obj.parentElement
        let passField = parent.querySelector('input[data-type=password]')
        if (passField.type === "password") {
            passField.type = "text";
        } else {
            passField.type = "password";
        }
    }
    
}


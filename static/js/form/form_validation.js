function validateEmail(email) {
  var re = /^(?:[a-z0-9!#$%&amp;'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&amp;'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$/;
  return re.test(email);
};

function validatePassword(password) {
    function PassLetters(password) {
        var lowerCaseLetters = /[a-z]/g;
        var upperCaseLetters = /[A-Z]/g;
        if (password.match(lowerCaseLetters) || password.match(upperCaseLetters)) {
            return true;
        } else {
            return false;
        };
    }
    function PassNumbers(password) {
        var numbers = /[0-9]/g;
        if (password.match(numbers)) {
          return true;
        } else {
          return false;
        };
    }
    function PassLength(password) {
        if (password.length >= 8) {
          return true;
        } else {
          return false;
        };
    }
    if (PassNumbers(password)==false || PassLetters(password)==false || PassLength(password)==false) {
        return false
    } else {
        return true
    }
}

function AllDone(form_id) {
    var formValid = true
    form = document.getElementById(form_id)
    inputs = form .elements
    passwords = []
    for (let ii = 0; ii < inputs.length; ii++) {
       if (inputs[ii].required == true && inputs[ii].value.length == 0) {
           return false
       }
       if (inputs[ii].required == true && inputs[ii].value.length > 0) {
           if (inputs[ii].type == 'email' && validateEmail(inputs[ii].value)==false) {
               return false
           }
           if (inputs[ii].type == 'password') {
               passwords.push(inputs[ii].value)
               if (passwords.length == 2 && passwords[0] != passwords[1]) {
                   return false
               }
               if (validatePassword(inputs[ii].value) == false) {
                   return false
               }
           }
           if (inputs[ii].type == 'file') {

           }
       }
       if (inputs[ii].required == true && inputs[ii].nodeName === "SELECT" ) {
           options = inputs[ii].querySelectorAll('option')
           for (var i = 0; i < options.length; i++) {
               if (options[i].selected && options[i].value.length == 0 ) {
                return false
               }
           }
       }
    }

    if (formValid == true) {
        form.dataset.valid = "True"
        return true
    }
    return false
}


function IsEmpty(form_id) {
    inputs = document.getElementById(form_id).elements
    form = document.getElementById(form_id)
    for (let ii = 0; ii < inputs.length; ii++) {
       if (inputs[ii].value.length != 0) {
           return false
       }
    }
    return true
}

function delAlerts(form_id) {
    inputs = document.getElementById(form_id).elements
    form = document.getElementById(form_id)
    for (let ii = 0; ii < inputs.length; ii++) {
        if ( document.getElementById("alert_" + inputs[ii].id) != null ) {
            document.getElementById("alert_" + inputs[ii].id).remove()
            inputs[ii].classList.remove("border-invalid");
        }
    }

}



function FieldValidate(input) {
    function add_p(input, alert_type) {
       
        
        if (alert_type == 'alert') {
            if ( document.getElementById("alert_" + input.id) == null ) {
                var p = document.createElement("p");
                p.className = "color-alert"
                p.setAttribute("id", "alert_" + input.id);
                p.innerHTML = input.dataset.alert;
                input.before(p)
                input.classList.remove("border-valid");
                input.classList.add("border-invalid");
            }
        }
        if (alert_type == 'error') {
            if ( document.getElementById("error_" + input.id) == null ) {
                var p = document.createElement("p");
                p.className = "color-alert"
                p.setAttribute("id", "error_" + input.id);
                p.innerHTML = input.dataset.error;
                input.before(p)
                input.classList.remove("border-valid");
                input.classList.add("border-invalid");
            }
        }
    }

    if (input.required == true) {
        if (input.value == "") {
            if ( document.getElementById("error_" + input.id) != null ) {
                document.getElementById("error_" + input.id).remove()
            } add_p(input, 'alert')
        } else if (input.value != "" && input.type == 'email' && validateEmail(input.value) == false) {
            if ( document.getElementById("alert_" + input.id) != null ) {
                    document.getElementById("alert_" + input.id).remove()
            } add_p(input, 'error')
        } else {
            input.classList.remove("border-invalid");
            input.classList.add("border-valid");
            if ( document.getElementById("alert_" + input.id) != null ) {
                    document.getElementById("alert_" + input.id).remove()
            }
            if ( document.getElementById("error_" + input.id) != null ) {
                    document.getElementById("error_" + input.id).remove()
            }
           
        }
    }
}




function InputCheck(input) {
    if (input.type != 'hidden' && (input.nodeName === "INPUT" || input.nodeName === "TEXTAREA" || input.nodeName === "SELECT")) {
         FieldValidate(input)
    }
}

function formFieldsValidation(form_id) {

    form = document.getElementById(form_id)
    inputs = form.elements
    for (let i = 0; i < inputs.length; i++) {
        // if (inputs[i].type == 'file') {
        //     FileFieldValidate(field)
        // }
        InputCheck(inputs[i])
    }
}
function FormToJSON(form_id) {
    form = document.getElementById(form_id)
    var obj = {};
    var elements = form.querySelectorAll( "input, select, textarea, select" );
    for( var i = 0; i < elements.length; ++i ) {
        var element = elements[i];
        var name = element.name;
        var value = element.value;
        if( name ) {
            obj[ name ] = value;

        }
    }
    return JSON.stringify( obj );
}

function ValidateFormOninput(form) {
    let form_elements = form.querySelectorAll('input, select, textarea, select')
    for (let j = 0; j < form_elements.length; j++) {
        let el = form_elements[j]
        el.onblur =  function() { FieldValidate(this) }
        el.oninput = function() { FieldValidate(this) }
    }
}

function ValidateForm(form) {
    let form_elements = form.querySelectorAll('input, select, textarea, select')
    for (let j = 0; j < form_elements.length; j++) {
        let el = form_elements[j]
        FieldValidate(el)
        
    }
}

forms = document.querySelectorAll('form')
for (let i = 0; i < forms.length; i++) {
    let form = forms[i]
    form.onclick = function() {
        ValidateFormOninput(form)
    }
}

//// GET VARS
let userForm = document.getElementById('userForm').elements;
// ADD DATA AFTER PASSWORD-1
let password1 = document.getElementById('password1');
let password1After = document.createElement('div')
password1After.id = 'password1-after'
password1.parentNode.insertBefore( password1After, password1.nextSibling );
// ADD DATA AFTER PASSWORD-2
let password2 = document.getElementById('password2');
let password2After = document.createElement('div')
password2After.id = 'password2-after'
password2.parentNode.insertBefore(password2After, password2.nextSibling );

// PASSWORD VALIDATE
let Pass1 = document.getElementById("password1");
let Pass2 = document.getElementById("password2");
let passEqual  = document.getElementById("pass-equal");
let letter  = document.getElementById("letter");
let number  = document.getElementById("number");
let length  = document.getElementById("length");
let letter_bool = false;
let number_bool = false;
let length_bool = false;
let pass_equal  = false;

Pass1.onfocus = function() {
  document.getElementById("PassMessage").style.display = "block";
  document.getElementById("password1-after").style.display = "block";
}

function PasswordEqual() {
  passEqual.style.display = "block";
  if (Pass1.value === Pass2.value) {
    ColorValidate(passEqual, true);
    ColorValidate(Pass2, true);
    passEqual.innerHTML = "Парои совпадают"
  } else {
    ColorValidate(passEqual, false);
    ColorValidate(Pass2, false);
    passEqual.innerHTML = "Парои не совпадают"
  };
}

function Password1() {
  var lowerCaseLetters = /[a-z]/g;
  var upperCaseLetters = /[A-Z]/g;
  var numbers = /[0-9]/g;
  // CHECK FOR LATIN LETTERS
  if (Pass1.value.match(lowerCaseLetters) || Pass1.value.match(upperCaseLetters)) {
    letter_bool = true;
    ColorValidate(letter, letter_bool);
  } else {
    letter_bool = false;
    ColorValidate(letter, letter_bool);
  };
  // CHECK FOR LATIN NUMBERS
  if (Pass1.value.match(numbers)) {
    number_bool = true;
    ColorValidate(number, number_bool);
  } else {
    number_bool = false;
    ColorValidate(number, number_bool);
  };
  // CHECK FOR LENGTH
  if(Pass1.value.length >= 8) {
    length_bool = true;
    ColorValidate(length, length_bool);
  } else {
    length_bool = false;
    ColorValidate(length, length_bool);
  };
  // CHECK FOR ALL
  if (letter_bool == true && number_bool == true && length_bool == true) {
    ColorValidate(Pass1, true);
  } else {
    ColorValidate(Pass1, false);
  };

  if (Pass2.value != '') {
    PasswordEqual();
    document.getElementById("password2-after").style.display = "block";
  }
}

Pass1.onkeyup  = function() { Password1() }
Pass1.onchange = function() { Password1() }
Pass2.onkeyup  = function() { PasswordEqual(); document.getElementById("password2-after").style.display = "block"; }
Pass2.onchange = function() { PasswordEqual(); document.getElementById("password2-after").style.display = "block"; }

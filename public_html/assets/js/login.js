let loginbutton = document.getElementById("submit")
let logged_in = false;
var form = document.getElementById("myform");
function handleForm(event) { event.preventDefault(); } 
form.addEventListener('submit', handleForm);
function stopsubmit(){
    return false;
}

let Username = document.getElementById("email");
let user = "";
let password = document.getElementById("password");
let pass = "";
Username.addEventListener("input", updateValue1)
password.addEventListener("input", updateValue2)
function updateValue1(e) {
    user = e.target.value;
  }
  function updateValue2(e) {
    pass = e.target.value;
  }

loginbutton.addEventListener('click', function(){
    let Username = document.getElementById("email").value;
    let password = document.getElementById("password").value;
  //  password = encrypt(password);
    //remove salt from AES, for repeatablility
    //const iv = { words: [ 0, 0, 0, 0 ], sigBytes: 16 }
    //password = CryptoJS.AES.encrypt(password, CryptoJS.enc.Utf8.parse('your secret key'), { iv }).toString();
    //password = password.toString();


    const userpass = new FormData();
    //userpass.append('username',Username);
    //userpass.append('pass', password)
    userpass.append("username",user)
    userpass.append("pass", pass)

    console.log(userpass);
    fetch(("http://localhost:3000/login.html"), {
        method: "POST",
        body: userpass
    }).then(function (response){
        if (response.status == 200){
            console.log("LOGGED IN");
            logged_in = true;
            window.location.pathname = '/upload.html'
            return true
        }
        else{
            window.location.reload()
            return false
        }
    
    })
});

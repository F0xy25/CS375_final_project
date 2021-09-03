//const bcrypt = require("bcrypt");

//const encrypt = async (password) => {
//    await bcrypt.hash(password)
//}

let submitbutton = document.getElementById("submit");

let loginbutton = document.getElementById("login")
let logged_in = false;
loginbutton.addEventListener("click", function(){
    let Username = document.getElementById("user").value;
    let password = document.getElementById("pass").value;
  //  password = encrypt(password);
    //remove salt from AES, for repeatablility
    //const iv = { words: [ 0, 0, 0, 0 ], sigBytes: 16 }
    //password = CryptoJS.AES.encrypt(password, CryptoJS.enc.Utf8.parse('your secret key'), { iv }).toString();
    //password = password.toString();


    const userpass = new FormData();
    userpass.append('username',Username);
    userpass.append('pass', password)

    console.log(userpass);
    fetch(("http://localhost:3000/login"), {
        method: "POST",
        body: userpass
    }).then(function (response){
        if (response.status == 200){
            console.log("LOGGED IN");
            logged_in = true;
        }
    });
});

submitbutton.addEventListener("click", function (){
    let reqURL = "http://localhost:3000/predict"

    let file_elem = document.getElementById("file");
    let model_elem = document.getElementById("model");

    console.log(file_elem.files[0])
    
    let File = file_elem.files[0];
    let Model = model_elem.value;

    let Username = document.getElementById("user").value;
    //check the value of the radio buttons, if one is clicked, that is text

    let radios = document.getElementsByName("Verbose");

    let Verbose = "";

    for (var i =0, length = radios.length; i < length; i++){
        if(radios[i].checked){
            Verbose = radios[i].value;
        }
    }
    //password code, for any implementation

    //let logged_in = false;

    //password = await bcrypt.hash(password);

    //const userpass = new FormData();
    //userpass.append('username',Username);
    //userpass.append('pass', password)
    //for new users, create folder and file
    //fetch(("http://localhost:3000/login"), {
    //    method: "POST",
    //    body = userpass
    //}).then(function (response){
    //    if (response.status == 200){
    //        logged_in = true;
    //    }
    //});

    //add code to check if all values are there, if not, change message body
    //to bad request

    //const jsondata = {file: File, model: Model, verbose: Verbose}
    //console.log(jsondata)

    //upload user selected file
    if (logged_in == false){
        console.log("CAN'T PROCEED, LOGIN FIRST");
        let returndiv = document.getElementById("message");
        returndiv.textContent = "CAN'T PROCEED, LOGIN FIRST";
    }
    else{
    const formData = new FormData();
    formData.append('file', File);
    formData.append('model', Model);
    formData.append('verbose', Verbose);
    formData.append('username',Username)
    console.log(formData);
    fetch(("http://localhost:3000/upload"), {
        method: "POST",
        body: formData
    });

    //if file successfully uploaded, run next request
    //edit to send both file and json when post request is made
    fetch((reqURL), {
        method: 'POST',
        body: formData
    }).then(function (response){
        let returndiv = document.getElementById("message");
        console.log(response)
        if (response.status == 200){
            returndiv.textContent = "Success";

            //load all images from temp
            //for each function, process response differently, as output
            //will be different

        }
        else{
            returndiv.textContent = "Bad Request";
        }
    });
    }
});
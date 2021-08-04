let submitbutton = document.getElementById("submit");

submitbutton.addEventListener("click", function (){
    let reqURL = "http://127.0.01:5000/predict"

    let file_elem = document.getElementById("file");
    let model_elem = document.getElementById("model");

    console.log(file_elem.files)
    
    let File = file_elem.value;
    let Model = model_elem.value;

    //check the value of the radio buttons, if one is clicked, that is text

    let radios = document.getElementsByName("Verbose");

    let Verbose = "";

    for (var i =0, length = radios.length; i < length; i++){
        if(radios[i].checked){
            Verbose = radios[i].value;
        }
    }

    //add code to check if all values are there, if not, change message body
    //to bad request

    const jsondata = {file: File, model: Model, verbose: Verbose}
    console.log(jsondata)


    //edit to send both file and json when post request is made
    fetch((reqURL), {
        method: 'POST',
        headers: {
            "Content-Type": 'application/json',
        },
        body: JSON.stringify(jsondata)
    }).then(function (response){
        let returndiv = document.getElementById("message");
        if (response.status == 200){
            returndiv.textContent = "Success";
        }
        else{
            returndiv.textContent = "Bad Request";
        }
    });

});
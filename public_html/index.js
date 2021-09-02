let submitbutton = document.getElementById("submit");

submitbutton.addEventListener("click", function (){
    let reqURL = "http://localhost:3000/predict"

    let file_elem = document.getElementById("file");
    let model_elem = document.getElementById("model");

    console.log(file_elem.files[0])
    
    let File = file_elem.files[0];
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

    //upload user selected file
    const formData = new FormData();
    formData.append('file', File);
    formData.append('model', Model);
    formData.append('verbose', Verbose);
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
        if (response.status == 200){
            returndiv.textContent = "Success";

            //for each function, process response differently, as output
            //will be different

        }
        else{
            returndiv.textContent = "Bad Request";
        }
    });

});
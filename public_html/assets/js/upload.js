let login_y = document.getElementById("login_y")
let login_n = document.getElementById("login_n")

login_y.style.display = "none";
login_n.style.display = "none";
console.log("Invisible")
let submitbutton = document.getElementById("submit")
document.getElementById("img_table").style.display = "none"
let user = "";
let logged_in = false;

window.onload = function(){
    console.log("Onload")
    document.getElementById("login_y").style.display = "none"
    document.getElementById("login_n").style.display = "none"
    let usr_request = "http://localhost:3000/user"
    fetch(usr_request, {
        method: "POST"
    }).then(function (response){
        console.log("RESPONSE",response)
        username = response.statusText

        if (username.trim() === "none"){
            logged_in = false;
            login_n.style.display = "inline";
        }else{
            user = username;
            logged_in = true;
            login_y.textContent = "You are currently signed in as "+user
            login_y.style.display = "inline";
        }
    })
}

let history_button = document.getElementById("hist")

history_button.addEventListener("click", function(){
    window.location.pathname = "/history.html"
})

submitbutton.addEventListener("click", function (){
    let reqURL = "http://localhost:3000/upload.html"
    let predict = 'http://localhost:3000/predict'
    let file_elem = document.getElementById("file");
    let model_elem = document.getElementById("model");

    console.log(file_elem.files[0])
    
    let File = file_elem.files[0];
    let Model = model_elem.value;

    //let Username = document.getElementById("user").value;
    //check the value of the radio buttons, if one is clicked, that is text

    let radios = document.getElementsByName("Verbose");

    let Verbose = "";

    for (var i =0, length = radios.length; i < length; i++){
        if(radios[i].checked){
            Verbose = radios[i].value;
        }
    }

    const formData = new FormData();
    formData.append('file', File);
    formData.append('model', Model);
    formData.append('verbose', Verbose);
    formData.append('username',user)
    console.log(formData);
    let spinner = document.createElement("")
    //upload user selected file
    if (logged_in == false){
        fetch((reqURL), {
        method: "POST",
        body: formData
    });
        fetch((predict), {
            method: 'POST',
            body: formData
        }).then(function (response){
            let returndiv = document.getElementById("message");
            console.log(response)
            if (response.status == 200){
                document.getElementById("img_table").style.display = "inline"
                //returndiv.textContent = "Success";
                //let image_div = document.createElement("div");
                let image_table = document.getElementById('img_table');
                let img_label = document.createElement("label");
                var row1 = document.createElement("tr")
                var row2 = document.createElement("tr")
                img_label.textContent = response.statusText
                img_elem = document.createElement("img")
                img_elem.src = response.statusText
                row1.appendChild(img_label)
                row2.appendChild(img_elem)
                image_table.appendChild(row1)
                image_table.appendChild(row2)
                //document.body.append(image_div)
            }
                //load all images from temp
                //for each function, process response differently, as output
                //will be different
    
            
            else{
                returndiv.textContent = "Bad Request";
            }
        });
    }
    else{
    
    fetch((reqURL), {
        method: "POST",
        body: formData
    });

    //if file successfully uploaded, run next request
    //edit to send both file and json when post request is made
    fetch((predict), {
        method: 'POST',
        body: formData
    }).then(function (response){
        let returndiv = document.getElementById("message");
        console.log(response)
        if (response.status == 200){
            document.getElementById("img_table").style.display = "inline"
                //returndiv.textContent = "Success";
                //let image_div = document.createElement("div");
                let image_table = document.getElementById('img_table');
                let img_label = document.createElement("label");
                var row1 = document.createElement("tr")
                var row2 = document.createElement("tr")
                img_label.textContent = response.statusText
                img_elem = document.createElement("img")
                img_elem.src = response.statusText
                row1.appendChild(img_label)
                row2.appendChild(img_elem)
                image_table.appendChild(row1)
                image_table.appendChild(row2)

            
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
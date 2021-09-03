let logged_in = false;
let user = "";
window.onload = function(){
    console.log("Onload")
    //document.getElementById("login_y").style.display = "none"
    //document.getElementById("login_n").style.display = "none"
    let usr_request = "http://localhost:3000/user"
    fetch(usr_request, {
        method: "POST"
    }).then(function (response){
        console.log("RESPONSE",response)
        username = response.statusText

        if (username.trim() === "none"){
            logged_in = false;
            //login_n.style.display = "inline";
        }else{
            user = username;
            let header = document.createElement("h3")
            header.textContent = username
            let header_section = document.getElementById("history")
            header_section.appendChild(header)
            logged_in = true;
            //login_y.textContent = "You are currently signed in as "+user
            //login_y.style.display = "inline";
        }
    
    if (logged_in ==true){
        const formData = new FormData();
        formData.append('user', username);
        fetch("http://localhost:3000/upload",{
            method: "POST",
            body: formData
        }).then(function (response){
            //download all processed files into 
            console.log(response)
            let header_section = document.getElementById("history")
            let table = document.createElement("table");
            if (response.status == 200){
                files = response.statusText.split(",")
                for (var i=0; i < files.length; i++){
                    //returndiv.textContent = "Success";
                    //let image_div = document.createElement("div");
                    //let image_table = document.getElementById('img_table');
                    let img_label = document.createElement("label");
                    var row1 = document.createElement("tr")
                    var row2 = document.createElement("tr")
                    img_label.textContent = files[i]
                    img_elem = document.createElement("img")
                    img_elem.src = files[i]
                    row1.appendChild(img_label);
                    row2.appendChild(img_elem);
                    table.appendChild(row1);
                    table.appendChild(row2);
                }
                header_section.appendChild(table);
        }
    })
}
});
}
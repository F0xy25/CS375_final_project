const exp = require("constants");
const express = require("express");
const bcrypt = require("bcrypt")
const app = express();
//let ajax = require("ajax");
const port = 3000;
const hostname = "localhost";

const fs = require("fs")
const spawn = require('child_process').spawn;

const fileupload = require('express-fileupload')

app.use(express.static("public_html"))
app.use(express.json())
app.use(fileupload());

//const encrypt = async (password) => {
//    await bcrypt.hash(password)
//}

app.get("/login", function(req, res){
    let user = req.body.username;
    let pass = req.body.pass;

    //CryptoJS.AES.decrypt(code, CryptoJS.enc.Utf8.parse('your secret key'), { iv }).toString(CryptoJS.enc.Utf8)
    //pass = encrypt(pass);
    let new_user = false

    let login = spawn('python', ['./aws.py', user, pass, new_user])

    login.stdout.on("data", function(data){
        console.log("Printing from Python...");
        console.log(data.toString());
        res.status(200)
        res.send()
    });
    

});

app.post("/login", function(req,res){
    //add new user password to 
    let user = req.body.username
    let pass = req.body.pass

    //pass = encrypt(pass);
    let new_user = true;
    let login = spawn('python', ['./aws.py', user, pass, new_user])

    login.stdout.on("data", function(data){
        console.log("Printing from Python...");
        console.log(data.toString());
        res.status(200)
        res.send()
    });
    
});

app.post("/upload", function(req,res){
    console.log("Upload File");
    console.log(req.files.file);
    let username = req.body.username
    const path = __dirname + '/temp_img/' + req.files.file.name

    req.files.file.mv(path, (error) => {
        if (error) {
            console.error(error);
        }
    })

    let s3 = spawn('python', ['./aws.py', username, req.files.file.name, true])
    //Take file saved locally
    //add file to s3 under a specific file structure and username
    //delete temp image from temp folder
});

app.get("/upload", function(req,res){
    console.log("Getting Files")

    let s3 = spawn('python', ['./aws.py', req.body.username, "", false])
})

app.post("/predict", function(req, res){
    //make ajax request to python script,
    console.log("ENTER PREDICT")
    console.log(req.body)
    let model = req.body.model;
    let image_src = req.files.file
    let image_filepath = __dirname+'/temp_img/' + req.files.file.name
    let new_filepath = "new_"+req.files.file.name
    let username = req.body.username
    console.log(model);
    console.log(image_src);
    console.log(image_filepath)
    //kick of child process that runs python script
    console.log("Starting Python script...");
    let ml_data = spawn('python', ['./model-predict.py', model, image_filepath, new_filepath]);

    //collect data from script
    ml_data.stdout.on("data", function(data){
        console.log("Printing from Python...");
        console.log(data.toString());
    
    //look at results files from temp_img and upload to s3 for the user
    let processed_img_file = __dirname+'/temp_img/' + new_filepath
    let upload_results = spawn('python', ['./results_upload.py',username, new_filepath, req.files.file.name])
    //console.log("Python process terminated.");

    //put response within console output in order to function as delay
    upload_results.stdout.on("data", function(data){
        console.log("Printing from Python...");
        console.log(data.toString());
    //Send file back to client
    fs.readFile((processed_img_file), function(err, content){
        if (err){
            res.writeHead(404, {"Content-type": "text/html"});
            res.end("<h1> No image found <h1>");
        } else {
            res.writeHead(200, {"Content-type": "image/jpg"});
            res.send(content);
        }
    })
    })
    });
});

app.get("/predict", function(req, res){



});

app.listen(port, hostname, () => {
    console.log(`Listening at: http://${hostname}:${port}`);
});
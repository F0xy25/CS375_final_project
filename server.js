const exp = require("constants");
const express = require("express");
const bcrypt = require("bcrypt")
const app = express();
//let ajax = require("ajax");
const port = 3000;
const hostname = "localhost";
var logged_in_user = "none";
const fs = require("fs")
const spawn = require('child_process').spawn;
const path = require("path")
const fileupload = require('express-fileupload')

app.use(express.static("public_html"))
app.use(express.json())
app.use(fileupload());

app.use("/temp_img", express.static('temp_img'));

//empty temp_img on startup
let img_path = __dirname+"/temp_img"
fs.readdir(img_path, (err, files) => {
    if (err) throw err;
  
    for (const file of files) {
      fs.unlink(path.join(img_path, file), err => {
        if (err) throw err;
      });
    }
  });

app.post("/login.html", function(req, res){
    let user = req.body.username;
    let pass = req.body.pass;
    

    let new_user = "login"
    
    if (typeof user === "undefined" || typeof pass === "undefined"){
        console.log("UNDEFINED")
        //res.status(400);
        //res.redirect("/login.html")
        //res.end()
    }
    else{
    let login = spawn('python', ['./aws.py', user, pass, new_user])

    login.stdout.on("data", function(data){
        console.log("Printing from Python...");
        console.log(data.toString());
        let output = data.toString();
        output = output.split("\n")
        let truth = output[output.length -2]
        let already_user = output[output.length -3]
        console.log("TRUTH",truth)
        console.log(typeof truth)
        if (truth.trim() === "True" && already_user.trim() === "True"){
        console.log("Passed")
        res.status(200);
        logged_in_user = user;
        //res.redirect('/upload.html')
        res.send()
        }else{
            console.log("Failed")
            res.status(400);
            //res.redirect('/login.html')
            res.send()
        }
    });
}
});


app.post("/register.html", function(req, res){
    let user = req.body.username;
    let pass = req.body.pass;
    


    let new_user = "register"
    
    if (typeof user === "undefined" || typeof pass === "undefined"){
        console.log("UNDEFINED")
        //res.status(400);
        //res.redirect("/login.html")
        //res.end()
    }
    else{
    let login = spawn('python', ['./aws.py', user, pass, new_user])

    login.stdout.on("data", function(data){
        console.log("Printing from Python...");
        console.log(data.toString());
        let output = data.toString();
        output = output.split("\n")
        let truth = output[output.length -2]
        let already_user = output[output.length -3]
        console.log("TRUTH",truth)
        console.log(typeof truth)
        if (truth.trim() === "True" && already_user.trim() === "False"){
        console.log("Passed")
        res.status(200);
        logged_in_user = user;
        //res.redirect('/upload.html')
        res.send()
        }else{
            console.log("Failed")
            res.status(400);
            //res.redirect('/login.html')
            res.send()
        }
    });
}
});


app.post("/user", function(req, res){
    console.log("User:", logged_in_user)
    res.status(200)
    res.statusMessage = logged_in_user
    res.send()
});


app.post("/upload.html", function(req,res){
    console.log("Upload File");
    console.log(req.files.file);
    let username = req.body.username
    const path = __dirname + '/temp_img/' + req.files.file.name

    req.files.file.mv(path, (error) => {
        if (error) {
            console.error(error);
        }
    })
    let upload = "upload"
    if (username.trim() === ""){
        console.log("NOT SIGNED IN USER")
    }else{
    let s3 = spawn('python', ['./aws.py', username, req.files.file.name, upload])
    }
});

//clear temp_img
//download all processed files into temp_img
//return list of filenames
app.post("/upload", function(req,res){
    console.log("BODY",req.body)
    let s3 = spawn('python', ['./fetch.py', req.body.user])

    var hist_files = []
    i = 2;
    s3.stdout.on("data", function(data){
        console.log("Printing from Python...");
        console.log(data.toString());

        let files = data.toString();
        files = files.split("\n")
        while (files[files.length-i].trim() !== "poss_files"){
            hist_files.push(files[files.length-i])
            i = i+1;
        }
        res.statusMessage = hist_files
        res.status(200);
        res.send()
    })
});

app.post("/predict", function(req, res){
    //make ajax request to python script,
    console.log("ENTER PREDICT")
    console.log(req.body)
    let model = req.body.model;
    let image_src = req.files.file
    let image_filepath = __dirname+'/temp_img/' + req.files.file.name
    let new_filepath = "new_"+model+"_"+req.files.file.name
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
    let processed_img_file = '/temp_img/' + new_filepath
    if (username.trim() === ""){
        res.status(200)
        res.statusMessage = processed_img_file
        res.send()
    }else{
    let upload_results = spawn('python', ['./results_upload.py',username, new_filepath, req.files.file.name])
    //console.log("Python process terminated.");

    //put response within console output in order to function as delay
    upload_results.stdout.on("data", function(data){
        console.log("Printing from Python...");
        console.log(data.toString());
    //Send file back to client
    //fs.readFile((processed_img_file), function(err, content){
    //    if (err){
    //        res.writeHead(404, {"Content-type": "text/html"});
    //        res.end("<h1> No image found <h1>");
    //    } else {
    //        res.writeHead(200, {"Content-type": "image/jpg"});
    //        res.end(content);
    //    }
        res.status(200)
        res.statusMessage = processed_img_file
        res.send()
    })
    }
    })
    });



app.listen(port, hostname, () => {
    console.log(`Listening at: http://${hostname}:${port}`);
});
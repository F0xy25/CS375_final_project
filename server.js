const exp = require("constants");
const express = require("express");
const app = express();
//let ajax = require("ajax");
const port = 3000;
const hostname = "localhost";

const spawn = require('child_process').spawn;

const fileupload = require('express-fileupload')

app.use(express.static("public_html"))
app.use(express.json())
app.use(fileupload());


app.post("/upload", function(req,res){
    console.log("Upload File");
    console.log(req.files.file);
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
    console.log(model);
    console.log(image_src);
    console.log(image_filepath)
    //kick of child process that runs python script
    console.log("Starting Python script...");
    let ml_data = spawn('python', ['./model-predict.py', model, image_filepath]);

    //collect data from script
    ml_data.stdout.on("data", function(data){
        console.log("Printing from Python...");
        console.log(data.toString());
    });
    //console.log("Python process terminated.");
});

app.get("/predict", function(req, res){



});

app.listen(port, hostname, () => {
    console.log(`Listening at: http://${hostname}:${port}`);
});
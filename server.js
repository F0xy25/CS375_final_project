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
});



app.post("/predict", function(req, res){
    //make ajax request to python script,
    console.log(req.body)
    let model = req.body.model;
    let image_src = req.body.file
    console.log(model);
    console.log(image_src);
    //kick of child process that runs python script
    console.log("Starting Python script...");
    let ml_data = spawn('python', ['./model-predict.py', model, image_src]);

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
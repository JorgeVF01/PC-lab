var mariadb = require('mariadb');
const express = require("express");
const bodyParser = require("body-parser");
const ejs = require("ejs");
const fs = require('fs');
const { spawnSync } = require('child_process');


const usuario = {user:'',pass:''};
const PORT = process.env.PORT || 3000;

var auth = false;
const app = express();
app.use(bodyParser.urlencoded({
  extended: true
}));
app.use(bodyParser.json());
app.use(express.static("public"));
app.set("view engine", "ejs");

const names = {"Pw":"Fuente de Poder","Gpu":"GPU","MB":"Placa Madre","Core":"Procesador","C":"Sistema de Enfriamiento"}



async function insert(user,data){

}

app.get("/", function(req, res) {
res.render('gallery');
});


app.post("/", async (req,res)=> {
  console.log(req.body);
  data = JSON.stringify(req.body);
  console.log(typeof(data));

  fs.writeFileSync('request.txt', data);
  console.log('file created');
  const pythonProcess = spawnSync('python3', [
    'NB.py',

  ]);
 let result = pythonProcess.stdout.toString().split("\n");
 result = result.slice(0,result.length-1)
 const bug = pythonProcess.stderr?.toString()?.trim();
 console.log(result);
 console.log(bug);
 let result_object = {};
 result.forEach((obj)=>{
  const comp_object = JSON.parse(obj)
  const key = Object.keys(comp_object)[0]
  result_object[names[key]] = comp_object[key]
 })

 res.render("results",{results: result_object});
});





app.listen(PORT, function() {
  console.log("Server running");
});

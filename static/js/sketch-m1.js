// Jaacript Code Goes here
let pic;

function setup(){
    let c = createCanvas(600,600);
    c.parent('canvas-div');

    divData = document.querySelector('#canvas-div');
    imgURL = divData.getAttribute('data-generated-img');

    // pic = createImage(imgURL);
    if(imgURL){
        loadImage(imgURL, (loadImage)=>{
            pic = loadedImage;
        },(error)=>{
            console.error("Error is: ", error);
        });
    }else{
        console.log("No image URL found.");
    }
}

function draw(){
    background(33,33,33);
    // console.log(imgURL);
    if(pic){
        image(pic,0,0,width,height);
    }else{
        fill(33,33,33);
        textAlign(CENTER);
        textSize(32);
        text("Loading iamge...", width/2, height/2);
    }
}
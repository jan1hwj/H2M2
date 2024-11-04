// Jaacript Code Goes here
let pic;
let displayMode = 'story';

function setup(){
    let c = createCanvas(600,600);
    c.parent('canvas-div');

    divData = document.querySelector('#canvas-div');
    imgURL = divData.getAttribute('data-generated-img');
    storyText = divData.getAttribute('data-story');

    // pic = createImage(imgURL);
    if(imgURL){
        loadImage(imgURL, (loadImage)=>{
            pic = loadImage;
        },(error)=>{
            console.error("Error is: ", error);
        });
    }else{
        console.log("No image URL found.");
    }

    document.getElementById('showStoryBtn').addEventListener('click', ()=>{
        displayMode = 'story';
    });

    document.getElementById('showImageBtn').addEventListener('click', ()=>{
        displayMode = 'image';
    });

    displayStory(storyText);
}

function draw(){
    background(33,33,33);
    
    if(displayMode == 'image' && pic){
        image(pic, 0, 0, width, height);
    }else{
        divData = document.querySelector('#canvas-div');
        storyText = divData.getAttribute('data-story');
        displayStory(storyText);
    }

}

function displayStory(story){
    fill(255);
    textAlign(CENTER, CENTER);
    textSize(20);
    textWrap(WORD);

    textX = width/2;
    textY = height/2;
    textWidth = width*0.8;

    text(story, textX-textWidth/2, textY, textWidth);
}
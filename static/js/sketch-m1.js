// Jaacript Code Goes here
function setup(){
    let c = createCanvas(600,600);
    c.parent('canvas-div');

    divData = document.querySelector('#canvas-div');
}

function draw(){
    background(33,33,33);
    fill(255);
    rectMode(CENTER);
    
    story_text = divData.dataset.story;

    textSize(18);
    textWrap(WORD);
    text(story_text, width/2, height/2, width-100, height-100);
}
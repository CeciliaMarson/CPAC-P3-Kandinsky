class Circle{
  //Data
  float x;
  float y;
  float diameter;
  //float colour;
  float strokeW;
  float try1;
  float try2;
  
  //Constructor 
  Circle(){
    try1 = width;
    try2 = height;
    x = random(0,width);
    y = random(0,height);
    diameter = random(100);
    //colour = random(255);
    strokeW = random(10);
    
    
  }
      
      
  //Functionalities
  void display(color example){
    stroke(0);
    strokeWeight(strokeW);
    fill(example);
    circle(x,y,diameter);
  }
  
  
}

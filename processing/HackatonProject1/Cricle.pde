class Circle{
  //Data
  float x;
  float y;
  float diameter;
  float strokeW;
  
  //Constructor 
  Circle(float wid,float hei,float diameter,float strokeW){
    x = random(0,wid);
    y = random(0,hei);
    this.diameter = diameter;
    this.strokeW = strokeW; 
    
  }
      
      
  //Functionalities
  void display(color example){
    stroke(0);
    strokeWeight(strokeW);
    fill(example);
    circle(x,y,diameter); //check if this.stuff or variable_in_class
    
  }
  
}

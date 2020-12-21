class Square{
  //Data
  Point p1;
  float extent;
  float strokeW;
  
  //Constructor 
  Square(Point p1, float extent, float strokeW){
    this.p1 = p1;
    this.extent = extent;
    this.strokeW = strokeW;
    
  }
      
  //Functionalities
  void display(color example){
    stroke(0);
    strokeWeight(strokeW);
    fill(example);
    square(this.p1.x,this.p1.y,this.extent); //check if this.stuff or variable_in_class
  
  }
}

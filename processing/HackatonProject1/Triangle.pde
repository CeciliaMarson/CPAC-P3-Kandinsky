class Triangle{
  //Data
  Point p1;
  Point p2;
  Point p3;
  float strokeW;
  
  //Constructor 
  Triangle(Point p1, Point p2,Point p3,float strokeW){
    this.p1 = p1;
    this.p2 = p2;
    this.p3 = p3;
    this.strokeW = strokeW;
    
  }
      
  //Functionalities
  void display(color example){
    stroke(0);
    strokeWeight(strokeW);
    fill(example);
    triangle(this.p1.x,this.p1.y,this.p2.x,this.p2.y,this.p3.x,this.p3.y); //check if this.stuff or variable_in_class
  
  }
}

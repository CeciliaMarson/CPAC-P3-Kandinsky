class Rectangle{
  //Data
  Point p1;
  float wid;
  float heig;
  float strokeW;
  
  //Constructor 
  Rectangle(Point p1, float wid, float heig, float strokeW){
    this.p1 = p1;
    this.wid = wid;
    this.heig = heig;
    this.strokeW = strokeW;
    
  }
      
  //Functionalities
  void display(color example){
    stroke(0);
    strokeWeight(strokeW);
    fill(example);
    rect(this.p1.x,this.p1.y,wid,heig); //check if this.stuff or variable_in_class
  
  }
}

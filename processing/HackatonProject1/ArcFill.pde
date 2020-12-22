class ArcFill{
  //Data
  Point p1;
  float wid;
  float heig;
  float strokeW;
  float start_rad;
  float stop_rad;
  
  //Constructor 
  ArcFill(Point p1, float wid, float heig, float strokeW, float start_rad, float stop_rad){
    this.p1 = p1;
    this.wid = wid;
    this.heig = heig;
    this.strokeW = strokeW;
    this.start_rad = start_rad;
    this.stop_rad = stop_rad;
    
  }
      
  //Functionalities
  void display(color example){
    stroke(0);
    strokeWeight(strokeW);
    fill(example);
    arc(this.p1.x,this.p1.y,this.wid,this.heig,this.start_rad,this.stop_rad, CHORD); //check if this.stuff or variable_in_class
  
  }
}

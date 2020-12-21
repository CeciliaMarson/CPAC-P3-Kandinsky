class Arc{
  //Data
  Point p1;
  float wid;
  float heig;
  float strokeW;
  float start_rad;
  float stop_rad;
  
  //Constructor 
  Arc(Point p1, float wid, float heig, float strokeW, float start_rad, float stop_rad){
    this.p1 = p1;
    this.wid = wid;
    this.heig = heig;
    this.strokeW = strokeW;
    this.start_rad = start_rad;
    this.stop_rad = stop_rad;
    
  }
      
  //Functionalities
  void display(){
    stroke(0);
    strokeWeight(strokeW);
    noFill();
    arc(this.p1.x,this.p1.y,this.wid,this.heig,this.start_rad,this.stop_rad); //check if this.stuff or variable_in_class
  
  }
}

class Line extends Figure {
  //Data
  //(none)
  
    //Constructor 
  Line(Pair p1, Pair p2, Pair p3, color c){
    this.p1 = p1; // position first point
    this.p2 = p2; // position second point
    this.p3 = p3; // useless data 
    this.c = c; // color stroke
    
  }
      
  //Functionalities
  void display(){
    stroke(this.c, random(255));
    strokeWeight(random(5));
    line(this.p1.x,this.p1.y,this.p2.x,this.p2.y); //check if this.stuff or variable_in_class
  
  }
}

class ArcFill extends Figure {
  //Data
  //(none)
  
  //Constructor 
  ArcFill(Pair p1, Pair p2, Pair p3, color c){
    this.p1 = p1; // position
    this.p2 = p2; // w and h
    this.p3 = p3; // start and stop 
    this.c = c; // color fill
    
  }
      
  //Functionalities
  void display(){
    stroke(0);
    strokeWeight(random(5));
    fill(this.c, random(255));
    arc(this.p1.x,this.p1.y,this.p2.x,this.p2.y,this.p3.x,this.p3.y, CHORD); //check if this.stuff or variable_in_class
  
  }
}

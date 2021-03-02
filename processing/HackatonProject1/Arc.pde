class Arc extends Figure {
  /*
  p1 -> position
  p2 -> w and h
  p3 -> start and stop
  c -> color stroke
  opacity -> alpha
  */
  
  //Constructor 
  Arc(Pair p1, Pair p2, Pair p3, color c, float opacity, int stroke, int fill){
    super(p1, p2, p3, c, opacity, stroke, fill);
  }
      
  //Functionalities
  void display(){
    stroke(this.c, this.opacity);
    strokeWeight(this.strokeWeight);
    noFill();
    arc(this.p1.x,this.p1.y,this.p2.x,this.p2.y,this.p3.x,this.p3.y); //check if this.stuff or variable_in_class
  
  }
  
}

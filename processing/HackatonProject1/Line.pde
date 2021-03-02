class Line extends Figure {
  /*
  p1 -> position first point
  p2 -> position second point
  p3 -> useless
  c -> color stroke
  opacity -> alpha
  */
  
  //Constructor 
  Line(Pair p1, Pair p2, Pair p3, color c, float opacity, int stroke, int fill){
    super(p1, p2, p3, c, opacity, stroke, fill);
  }
      
  //Functionalities
  void display(){
    stroke(this.c, this.opacity);
    strokeWeight(this.strokeWeight);
    line(this.p1.x,this.p1.y,this.p2.x,this.p2.y); //check if this.stuff or variable_in_class
  
  }
}

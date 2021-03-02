class Triangle extends Figure {
  /*
  p1 -> position first point
  p2 -> position second point
  p3 -> position third point
  c -> color stroke
  opacity -> alpha
  */
  
  //Constructor 
  Triangle(Pair p1, Pair p2, Pair p3, color c, float opacity, int stroke, int fill){
    super(p1, p2, p3, c, opacity, stroke, fill);
  }
      
  //Functionalities
  void display(){
    stroke(0);
    strokeWeight(this.strokeWeight);
    //fill only if the flag is set to 1
    if (this.fill == 1)
      fill(this.c, this.opacity);
    triangle(this.p1.x,this.p1.y,this.p2.x,this.p2.y,this.p3.x,this.p3.y); //check if this.stuff or variable_in_class
  
  }
}

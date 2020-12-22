class Triangle extends Figure {
  //Data
  //(none)
  
  //Constructor 
  Triangle(Pair p1, Pair p2, Pair p3, color c){
    this.p1 = p1; // position first point
    this.p2 = p2; // position second point
    this.p3 = p3; // position third point
    this.c = c; // color 
    
  }
      
  //Functionalities
  void display(){
    stroke(0);
    strokeWeight(random(5));
    fill(this.c);
    triangle(this.p1.x,this.p1.y,this.p2.x,this.p2.y,this.p3.x,this.p3.y); //check if this.stuff or variable_in_class
  
  }
}

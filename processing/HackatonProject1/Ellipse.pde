// WE ARE NOT USING IT RIGHT NOW

class Ellipse extends Figure {
  //Data
  //(none)
   
  //Constructor 
  Ellipse(Pair p1, Pair p2, Pair p3, color c){
    this.p1 = p1; // position
    this.p2 = p2; // w and h 
    this.p3 = p3; // useless data 
    this.c = c; // color 
    
  }
      
  //Functionalities
  void display(){
    stroke(0);
    strokeWeight(random(5));
    fill(this.c);
    ellipse(this.p1.x,this.p1.y,this.p2.x,this.p2.y); //check if this.stuff or variable_in_class
    
  }
  
}

class Square extends Figure {
  //Data
  //(none)
  
  //Pair p1;
  //float extent;
  //float strokeW;
  
  //Constructor 
  Square(Pair p1, Pair p2, Pair p3, color c){
    this.p1 = p1; // position first point
    this.p2 = p2; // p2.x --> extent | p2.y --> useless
    this.p3 = p3; // useless data 
    this.c = c; // color 
    
  }
      
  //Functionalities
  void display(){
    stroke(0);
    strokeWeight(random(5));
    fill(this.c);
    square(this.p1.x,this.p1.y,this.p2.x); //check if this.stuff or variable_in_class
  
  }
}

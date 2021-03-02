class Figure{
  //Data
  /*
  int selector;

  Ellipse e1;
  Triangle t1;
  Rectangle r1;
  Arc a1;
  ArcFill af1;
  Square sq1;
  Line l1;
  */
  
  Pair p1;
  Pair p2;
  Pair p3;
  color c;
  float opacity;
  int strokeWeight;
  int fill;
  
  //empty constructor 
  Figure(){
  }
  
  //constructor
  Figure(Pair p1, Pair p2, Pair p3, color c, float opacity, int stroke, int fill){
      this.p1 = p1;
      this.p2 = p2;
      this.p3 = p3;
      this.c = c;
      this.opacity = opacity;
      this.strokeWeight = stroke;
      this.fill = fill;
    }
      
  ////Functionalities
  void display(){
  }

}

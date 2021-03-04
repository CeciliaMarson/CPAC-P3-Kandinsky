class TriangleDrawable extends Figure {
  
  //the length of each side
  int sideLength;
  //rotation
  float rotation;
  
  //Constructor 
  TriangleDrawable(Pair p1, Pair p2, Pair p3, color c, float opacity, int stroke){
    super(p1, c, opacity, stroke, 0);
    this.fill = true;
    
    //shape creation
    this.shape = createShape();
    this.shape.beginShape();
    this.shape.fill(this.c, this.opacity);
    this.shape.vertex(this.p1.x, this.p1.y);
    this.shape.vertex(p2.x, p2.y);
    this.shape.vertex(p3.x, p3.y);
    this.shape.endShape(CLOSE);
  }
      
  //Functionalities
  void display(){
    shape(this.shape);
  }
}

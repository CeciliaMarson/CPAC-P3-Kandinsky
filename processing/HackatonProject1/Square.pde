class Square extends Figure {
  //the length of each side
  int sideLength;
  //rotation
  float rotation;
  
  //Constructor 
  Square(Pair p1, int side, color c, float opacity, int stroke, float rotation){
    super(p1, c, opacity, stroke, 0);
    this.sideLength = side;
    this.rotation = rotation;
    this.fill = true;
    
    //shape creation
    this.shape = createShape();
    this.shape.beginShape();
    this.shape.fill(this.c, this.opacity);
    this.shape.vertex(this.p1.x, this.p1.y);
    this.shape.vertex(this.p1.x+side, this.p1.y);
    this.shape.vertex(this.p1.x+side, this.p1.y+side);
    this.shape.vertex(this.p1.x, this.p1.y+side);
    this.shape.endShape(CLOSE);
  }
      
  //Functionalities
  void display(){
    shape(this.shape);
  }
}

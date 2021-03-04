class Rectangle extends Figure {
  //the length of each side
  float a;
  float b;
  //rotation
  float rotation;
  
  //Constructor 
  Rectangle(Pair p1, float a, float b, color c, float opacity, int stroke, float rotation){
    super(p1, c, opacity, stroke, 0);
    this.rotation = rotation;
    this.fill = true;
    
    //shape creation
    this.shape = createShape();
    this.shape.beginShape();
    this.shape.fill(this.c, this.opacity);
    this.shape.vertex(this.p1.x, this.p1.y);
    this.shape.vertex(this.p1.x+a, this.p1.y);
    this.shape.vertex(this.p1.x+a, this.p1.y+b);
    this.shape.vertex(this.p1.x, this.p1.y+b);
    this.shape.endShape(CLOSE);
  }
      
  //Functionalities
  void display(){
    shape(this.shape);
  }
}

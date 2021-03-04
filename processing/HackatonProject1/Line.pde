class Line extends Figure {
  
  //Constructor 
  Line(Pair p1, Pair p2, color c, float opacity, int stroke){
    super(p1, c, opacity, stroke, c);
    this.fill = false;
    
    //shape creation
    this.shape = createShape();
    this.shape.beginShape();
    this.shape.noFill();
    this.shape.vertex(this.p1.x, this.p1.y);
    this.shape.vertex(p2.x, p2.y);
    this.shape.endShape();
  }
      
  //Functionalities
  void display(){
     shape(this.shape);
  }
}

Circle c1;
Triangle t1;
Rectangle r1;
Arc a1;
ArcFill af1;
Square sq1;

color c = color(10,10,10);
int bpm = int(random(90,140));

void setup(){
  size(700,700);
  c1 = new Circle(width,height, 15.00, 5.00);
  t1 = new Triangle(new Point(10.0,200.0),new Point(347.0,212.0),new Point(463.0,285.0),2.00);
  r1 = new Rectangle(new Point(500.0,500.0), 120.0, 47.0, 2.0);
  a1 = new Arc(new Point(300.0,300.0), 100.0, 100.0, 10.0, 1.56, 5.63); 
  af1 = new ArcFill(new Point(200.0,200.0), 100.0, 100.0, 10.0, 1.56, 5.63);
  sq1 = new Square(new Point(600.0,200.0), 123.0, 3.0);
  
  background(255,245,184);
  
}



void draw(){
  t1.display(c);
  c1.display(c);
  r1.display(c);
  a1.display();
  af1.display(c);
  sq1.display(c);
  
  
}

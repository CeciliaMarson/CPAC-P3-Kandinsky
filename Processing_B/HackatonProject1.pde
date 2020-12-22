//Circle c1;
//Triangle t1;
//Rectangle r1;
//Arc a1;
//ArcFill af1;
//Square sq1;
Figure f1;
//Line l1;

color c = color(0,0,0);
int bpm = int(random(90,140));

void setup(){
  size(700,700);

//  l1 = new Line();
  f1 = new Triangle(new Pair(300.0,200.0), new Pair(100.0,600.0), new Pair(400.0,500.0), c);
//  f1 = new Figure(1, 10.0,10.0,10.0,10.0,10.0,10.0,10.0);
  //c1 = new Circle(width,height, 15.00, 5.00);
  //t1 = new Triangle(new Pair(10.0,200.0),new Pair(347.0,212.0),new Pair(463.0,285.0),2.00);
  //r1 = new Rectangle(new Pair(500.0,500.0), 120.0, 47.0, 2.0);
  //a1 = new Arc(new Pair(300.0,300.0), 100.0, 100.0, 10.0, 1.56, 5.63); 
  //af1 = new ArcFill(new Pair(200.0,200.0), 100.0, 100.0, 10.0, 1.56, 5.63);
  //sq1 = new Square(new Pair(600.0,200.0), 123.0, 3.0);
  
  background(255,245,184);
  
}



void draw(){
  f1.display();
  //t1.display(c);
  //c1.display(c);
  //r1.display(c);
  //a1.display();
  //af1.display(c);
  //sq1.display(c);
  
  
}

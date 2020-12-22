String jsonPath;
String[] filenames;
ArrayList<Info> song_color;

Circle c1;
Triangle t1;
Rectangle r1;
Arc a1;
ArcFill af1;
Square sq1;

color c = color(10,10,10);
int bpm = int(random(90,140));

void setup(){
  //the json file are in the data folder 
  jsonPath = sketchPath() + "/data";
  filenames = listFileNames(jsonPath);
  
  //TODO: read all the json files of the songs and store the rgb array
  //song color is an array list of colors for the first song only
  song_color = readJson(filenames[0]);
  
  size(700,700);
  c1 = new Circle(width,height, 15.00, 5.00);
  t1 = new Triangle(new Point(10.0,200.0),new Point(347.0,212.0),new Point(463.0,285.0),2.00);
  r1 = new Rectangle(new Point(500.0,500.0), 120.0, 47.0, 2.0);
  a1 = new Arc(new Point(300.0,300.0), 100.0, 100.0, 10.0, 1.56, 5.63); 
  af1 = new ArcFill(new Point(200.0,200.0), 100.0, 100.0, 10.0, 1.56, 5.63);
  sq1 = new Square(new Point(600.0,200.0), 123.0, 3.0);
  
  background(255,245,184);
}

//function used to read a single json file
//return an arraylist of Color
ArrayList<Info> readJson(String path){
  JSONArray values = loadJSONArray(path);
  ArrayList<Info> colorlist = new ArrayList<Info>();
  JSONObject rgb;
  color c;
  
  for (int i = 0; i < values.size(); i++) {
     rgb = values.getJSONObject(i); 
     c = color(rgb.getInt("R"), rgb.getInt("G"), rgb.getInt("B"));
     colorlist.add(new Info(c, rgb.getInt("Shape")));
  }
  
  return colorlist;
}

String[] listFileNames(String dir) {
  File file = new File(dir);
  if (file.isDirectory()) {
    String names[] = file.list();
    return names;
  } else {
    // If it's not a directory
    return null;
  }
}

void draw(){
  t1.display(c);
  c1.display(c);
  r1.display(c);
  a1.display();
  af1.display(c);
  sq1.display(c);
}

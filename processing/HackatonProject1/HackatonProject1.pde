import processing.sound.*;
String jsonPath;
String[] filenames;
ArrayList<Info> song_color;

int n=0;
//int bpm = int(random(90,140));
int size;
ArrayList<Figure> f1;
SoundFile sample;



void setup(){
  size(900,600);
  jsonPath = sketchPath() + "/data";
  filenames = listFileNames(jsonPath);
  ArrayList<Info> list=readJson(jsonPath+"/"+filenames[2]);
  String name="data/audio/The Kandinsky Effect/Defective Bleeding.wav";
  f1=get_figure(list);
  sample = new SoundFile(this,(name));
  background(255,245,184);
  frameRate(30.0/size);
}

//function used to read a single json file
//return an arraylist of Color
ArrayList<Info> readJson(String path){
  JSONArray values = loadJSONArray(path);
  ArrayList<Info> colorlist = new ArrayList<Info>();
  JSONObject rgb;
  color c;
  size=values.size();
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

ArrayList<Figure> get_figure(ArrayList<Info> info){
  ArrayList<Figure> figure= new ArrayList<Figure>();
  for(int i=0;i<info.size();i++){
    Figure fig;
    Info d=info.get(i);
    int s=d.shape;
    color c=d.col;
    Pair p1=new Pair(random(width/4,(3*width/4)),random(height/4,(3*height/4)));
    Pair p2=new Pair(random(width/5), random(height/5));
    Pair p3=new Pair(random(width), random(height)); 
    switch(s){
      case 0:
      fig=new Arc(p1,p2,p3,c);
      figure.add(fig);
      break;
      case 1:
      fig=new ArcFill(p1,p2,p3,c);
      figure.add(fig);
      break;
      case 2:
      fig=new Circle(p1,p2,p3,c);
      figure.add(fig);
      break;
      case 3:
      fig=new Rectangle(p1,p2,p3,c);
      figure.add(fig);
      break;
      case 4:
      fig=new Square(p1,p2,p3,c);
      figure.add(fig);
      break;
      case 5:
      fig=new Triangle(p1,p2,p3,c);
      figure.add(fig);
      break;
      case 6:
      fig=new Line(p1,p2,p3,c);
      figure.add(fig);
      break;
    }
    
  }
  return figure;
}



void draw(){
 if(n==0){
    sample.play();
 }
  int s=f1.size();
  if(n<s){
  Figure g1=f1.get(n);
  g1.display();
  n++;
  
  }
  
  
}

import processing.sound.*;

//global variables
String jsonPath;
String[] filenames;
ArrayList<Figure> figure_list;
SoundFile sample;
int n;
color backgroundColor;

void setup(){
  size(900,600);
  
  n = 0;
  //set json path and song path
  jsonPath = sketchPath() + "/data";
  String song_name="data/audio/The Kandinsky Effect/WeMakeOurOwnHolidays.wav";
  
  //get all the filenames in the jsonPath folder
  filenames = listFileNames(jsonPath);
  print(filenames[10]);
  //get the figure list
  figure_list = get_figure(readJson(jsonPath+"/"+filenames[10]));
  //create the sound file to be played in background
  sample = new SoundFile(this,(song_name));
  //set frame rate, 30.0 is the length in seconds of the spotify previews
  frameRate(figure_list.size()/30.0);
  //set the background based on the instrument
  background(backgroundColor);
}

//function used to read a single json file
//return an arraylist of Color
ArrayList<Info> readJson(String path){
  JSONArray values = loadJSONArray(path);
  ArrayList<Info> colorlist = new ArrayList<Info>();
  JSONObject json;
  Info info;
  
  for (int i = 0; i < values.size(); i++) {
     json = values.getJSONObject(i);
     //create info object
     info = new Info(color(json.getInt("R"), json.getInt("G"), json.getInt("B")), 
                     json.getInt("Shape"), 
                     json.getFloat("Transparency"),
                     new Pair(float(json.getInt("X_dim")), float(json.getInt("Y_dim"))),
                     json.getInt("Stroke"),
                     json.getInt("Figure fill"));
                     
     colorlist.add(info);
     backgroundColor = color(json.getInt("Back_R"), json.getInt("Back_G"), json.getInt("Back_B"));
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
  ArrayList<Figure> figures = new ArrayList<Figure>();
  Figure fig;
  Info d;
  Pair p1, p2, p3;
  
  for(int i=0;i<info.size();i++){
    //get current info
    d=info.get(i);
    
    p1=new Pair(random(width/4,(3*width/4)),random(height/4,(3*height/4)));
    p2=new Pair(random(width/5), random(height/5));
    p3=new Pair(random(width), random(height)); 
    
    //creation of the figure for the current info
    switch(d.shape){
      case 0:
      fig=new Arc(p1, p2, p3, d.col, d.opacity, d.strokeWeight, d.fill);
      figures.add(fig);
      break;
      
      case 1:
      fig=new ArcFill(p1, p2, p3, d.col, d.opacity, d.strokeWeight, d.fill);
      figures.add(fig);
      break;
      
      case 2:
      fig=new Circle(p1, p2, p3, d.col, d.opacity, d.strokeWeight, d.fill);
      figures.add(fig);
      break;
      
      case 3:
      fig=new Rectangle(p1, p2, p3, d.col, d.opacity, d.strokeWeight, d.fill);
      figures.add(fig);
      break;
      
      case 4:
      fig=new Square(p1, p2, p3, d.col, d.opacity, d.strokeWeight, d.fill);
      figures.add(fig);
      break;
      
      case 5:
      fig=new Triangle(p1, p2, p3, d.col, d.opacity, d.strokeWeight, d.fill);
      figures.add(fig);
      break;
      
      case 6:
      fig=new Line(p1, p2, p3, d.col, d.opacity, d.strokeWeight, d.fill);
      figures.add(fig);
      break;
    }
  }
  
  return figures;
}


void draw(){
  
  if(n==0){
    sample.play();
  }
  
  if(n < figure_list.size()){
    //get the current figure and display it
    figure_list.get(n).display();
    n++;
  }
}

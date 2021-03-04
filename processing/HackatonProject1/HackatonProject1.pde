import processing.sound.*;

//file path
String jsonPath;
String songPath;
//json and song names
String[] filenames;
String[] songNames;
//arraylist of figures and songs
ArrayList<SoundFile> audioFiles;
ArrayList<Figure> figures;
//audio file that is currently playing
SoundFile sample;
//index for the figure
int n;
//color for the background
color backgroundColor;

//brush
Brush brush;
int vertexIndex;
Figure currentFigure;
int songNumber=2, songIndex;
//back colors
color b1, b2;
//flags
boolean stop, backgroundDone;
int startTime;

void setup(){
  size(1900,900);
  //set frame rate
  frameRate(240);
  //set the background based on the instrument
  background(backgroundColor);
  
  //inizialize arraylist
  audioFiles = new ArrayList<SoundFile>();
  figures = new ArrayList<Figure>();
  
  //set json path and song path
  jsonPath = sketchPath() + "/data";
  songPath = "/data/audio";
  
  //get all the filenames in the jsonPath folder
  filenames = listFileNames(jsonPath);
  //get all the filesname in the audio folder
  songNames = listFileNames(sketchPath() + songPath);
  
  for (int i =0; i<songNumber; i++){
    //get the figure list
    get_figure(readJson(jsonPath+"/"+ ((filenames[i].equals("audio")) ? filenames[i+1] : filenames[i])), figures, i);
    //get the song to be played in background
    audioFiles.add(new SoundFile(this,(songPath+"/"+songNames[i])));
  }
  
  //PARAMETERS
  //set the initial position of the brush at random
  brush = new Brush(random(width/4), random(height/4));
  //set vertex index to the first vertex
  vertexIndex = 0;
  //start seeking from the beginnig
  stop = false;
  //set the first figure
  currentFigure = figures.get(0);
  //set the first song
  songIndex = 0;
  sample = audioFiles.get(songIndex);
  //set figure index to the first figure
  n = 0;
  //background
  backgroundDone = false;
  b1 = color(#264653);
  b2 = color(#e9c46a);
  //play the first song
  startTime = millis();
  sample.play();
  sample.amp(0.5);
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
                     new Pair(float(json.getInt("X_dim")/2), float(json.getInt("Y_dim")/2)),
                     json.getInt("Stroke"));
                     
     colorlist.add(info);
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

void get_figure(ArrayList<Info> info, ArrayList<Figure> figures, int index){
  Figure fig;
  Info d;
  Pair p1, p2, p3;
  int offset = (width/(info.size()*songNumber));
  
  for(int i=0;i<info.size();i++){
    //get current info
    d=info.get(i);
    
    p1 = new Pair(offset*i + index*width/2 + random(-offset*5, offset*10), d.position.y + random(-height/20, height/2));
    p2 = d.position;
    p3=new Pair(HALF_PI, PI); 
    
    //creation of the figure for the current info
    switch(d.shape){
      //line
      case 0:
      fig=new Arc(p1, d.col, d.opacity, d.strokeWeight);
      figures.add(fig);
      break;
      
      case 1:
      Pair secondPoint = new Pair(p1.x + random(-width/4, width/4), p1.y + random(0, height/4));
      fig=new Line(p1, secondPoint, d.col, d.opacity, d.strokeWeight);
      figures.add(fig);
      break;
      
      case 2:
      fig = new Wave(p1, d.col, d.opacity, d.strokeWeight);
      figures.add(fig);
      break;
      
      //fill
      case 3:
      fig=new Rectangle(p1, p2.x, p2.y, d.col, d.opacity, d.strokeWeight, 0);
      figures.add(fig);
      break;
      
      case 4:
      fig=new Square(p1, int(p2.x), d.col, d.opacity, d.strokeWeight, 0);
      figures.add(fig);
      break;
      
      case 5:
      Pair thirdPoint = new Pair(p1.x + random(-offset*10, offset*5), p1.y + random(-offset*5, offset*5));
      Pair secondPointT = new Pair(p1.x + random(-offset*10, offset*5), p1.y + random(-offset*5, offset*5));
      
      int drawable = int(random(2));
      if (drawable == 0)
        fig=new Triangle(p1, secondPointT, thirdPoint, d.col, d.opacity, d.strokeWeight);
      else fig=new TriangleDrawable(p1, secondPointT, thirdPoint, d.col, d.opacity, d.strokeWeight);
      figures.add(fig);
      break;
      
      case 6:
      fig=new ArcFill(p1, d.col, d.opacity, d.strokeWeight);
      figures.add(fig);
      break;
      
      case 7:
      fig=new Circle(p1, p2.x, d.col, d.opacity, d.strokeWeight);
      figures.add(fig);
      break;
      
      case 8:
      fig=new Ellipse(p1, random(d.position.x), random(d.position.y/4), d.col, d.opacity, d.strokeWeight);
      figures.add(fig);
      break;
      
      case 9:
      fig = new Grid(new Pair(random(width/2), random(height/2)), p2, p3, d.col, d.opacity);
      figures.add(fig);
      break;
    }
  }
}

//used for seeking and drawing with the brush
void brushDraw(int index, int stroke, color strokeColor){
  brush.currentStroke = stroke;
  brush.currentStrokeColor = strokeColor;
  brush.seek(currentFigure.getVertex(index));
  brush.update();
  brush.display();
}

void fetchNextFigure() {
  try {
      n++;
      currentFigure = figures.get(n);
      stop = false;
      vertexIndex = 0;
  } catch (IndexOutOfBoundsException e){
      filter(BLUR);
      noLoop();
  }
}

void setGradient(int x, int y, float w, float h, color c1, color c2, int axis ) {
  noFill();

  if (axis == 1) {  // Top to bottom gradient
    for (int i = y; i <= y+h; i++) {
      float inter = map(i, y, y+h, 0, 1);
      color c = lerpColor(c1, c2, inter);
      stroke(c);
      line(x, i, x+w, i);
    }
  }  
  else if (axis == 2) {  // Left to right gradient
    for (int i = x; i <= x+w; i++) {
      float inter = map(i, x, x+w, 0, 1);
      color c = lerpColor(c1, c2, inter);
      stroke(c);
      line(i, y, i, y+h);
    }
  }
}

void draw(){
  if (backgroundDone){
      if (millis() - startTime > 1000) {
          if ( currentFigure.isDrawable ) {
          
              brushDraw(vertexIndex, currentFigure.strokeWeight, currentFigure.strokeColor);
              if (abs(brush.location.x - currentFigure.getVertex(vertexIndex).x) < 4 && abs(brush.location.y - currentFigure.getVertex(vertexIndex).y) < 4 ){
                  if (vertexIndex < currentFigure.vertexNumber() -1 && !stop){
                    brush.drawing = true;
                    vertexIndex++;
                    
                  } else if ( vertexIndex == currentFigure.vertexNumber() -1 && !stop) {
                    if (currentFigure.fill)
                      vertexIndex = 0;
                 
                    stop = true;
                  } else if (stop) {
                    //stop the brush from drawing
                    brush.drawing = false;
                    //fill the shape
                    currentFigure.display();
                    
                    //fetch the next figure
                    if (sample.isPlaying())
                        fetchNextFigure();
                    else n = int(figures.size()/songNumber);
                    
                    if ( n == int(figures.size()/songNumber)){
                        try {
                            songIndex++;
                            sample = audioFiles.get(songIndex);
                            sample.amp(0.5);
                            sample.play();
                        } catch (IndexOutOfBoundsException e){
                            filter(BLUR);
                            noLoop();
                        }
                    }
                 }
              } 
         } else {
             currentFigure.display();
             fetchNextFigure();
         }
      }
  }else {
      setGradient(0, 0, width, height, b1, b2, 1);
      setGradient(width, 0, width, height, b2, b1, 1);
      backgroundDone = true;
  }
}

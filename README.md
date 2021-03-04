# CPAC-P3-Kandinsky

## Installation

You can use either venv or conda to create a virtual environment and install all the packages required in the requirements.txt file.
Important: right now tensorflow 2.4.1 require python 3.5-3.8.
Important: ffmpeg is required.

### Conda 

Create the environment.

```bash
conda create --name testenv python=3.8.0 pip
conda activate testenv
```

Install requirements in the requirements.txt

```bash
pip install -r requirements.txt
```

Also we need ffmpeg, in conda simply type

```bash 
conda install -c main ffmpeg
```

## Usage

Firstly, we have to run the feature_extraction.py script and type in the artist name.

```bash
python3 feature_extraction.py
```

This will download and extract instruments and features from the songs of the selected artist. After that open the HackatonProject1.pde file and play start. Enjoy!

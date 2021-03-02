# CPAC-P3-Kandinsky

## Installation

You can use either venv or conda to create a virtual environment and install all the packages required.
Important: right now tensorflow 2.4.1 require python 3.5-3.8

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

## Virtual env

Create the environment.

On linux or macOs:

```bash
python3 -m venv env 
```

On Windows:

```bash
py -m venv env 
```

Activate the environment.

```bash
source env/bin/activate
```

Install requirements in the requirements.txt

On linux or macOs:

```bash
python3 -m pip -r requirements.txt
```

On Windows:

```bash
py -m pip -r requirements.txt
```

Important: ffmpeg is required.

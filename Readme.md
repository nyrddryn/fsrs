


# FSRS
The FSRS (Free Spaced Repetition Scheduler) algorithm is based on a variant of the DSR (Difficulty, Stability, Retrievability) model, which is used to predict memory states.
In this project, we will rely on the user's learning habits and use FSRS to create the most optimal learning plan.
### Clone repos
```
git clone https://github.com/Luvannie/FSRS.git
```
### Flask
```
$ pip install -U flask flask-cors
```
### Run
File input: test.json
```
$ python main.py
```

### Docker
```
$ docker build -t my-flask-app .
$ docker run -p 5001:5001 my-flask-app
```


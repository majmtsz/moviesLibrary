import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True

class Movie:
    def __init__(self, title, director, actors={}):
        self.title = str(title)
        self.director = director
        self.actors = actors
    def __str__(self):
        stars = ''
        for role in self.actors:
            stars = stars + self.actors[role] + ', '
        return self.title + " " + self.director + ' starring: ' + stars

moviesDict = {'killer': Movie('killer', 'rezyser killera', {'rola1':'Aktor1'}), 'mis' : Movie('mis', 'pan rezyser')}

print(moviesDict['killer'])


def showAllMovies(moviesD):
    all = ''
    for movie in moviesD:
        all += 'Tytuł: ' + moviesD[movie].title + ', reżyser: ' + moviesD[movie].director + '\n'
    return all


@app.route('/', methods=['GET'])
def home():
    return "<h1>Strona główna</h1>"


@app.route('/movies/<title>', methods=['GET', 'POST', 'DELETE'])
def movies(title):
    # adding new movie - title from Path parameter, director from query string parameter
    # np: http://0.0.0.0:5000/movies/killer?director=jakisrezyser
    # aktorzy z body requestu
    if flask.request.method == 'POST':
        print(type(flask.request.json))
        if "director" in flask.request.args:
            director = flask.request.args.get("director")
            m = Movie(title, director, flask.request.json)
        else:
            m = Movie(title, 'unknown')
        moviesDict[m.title] = m
        newMovie = moviesDict[title]
        return flask.Response(f"<h1> Film {newMovie.title} wyreżyserowany przez {newMovie.director}, w rolach głownych: {newMovie.actors} został dodany do bazy filmów </h1>", 201)
    elif flask.request.method == 'GET' and title in moviesDict:
        return flask.Response(f"<h1>Zapytania zapytanie dotyczy filmu: {title}. Film został wyreżyserowany przez {moviesDict[title].director}", 200)
    elif flask.request.method == 'DELETE' and title in moviesDict:
        moviesDict.pop(title)
        return flask.Response(f"<h1>Usuwanie filmu: {title}. Z bazy danych", 202)
    elif flask.request.method == 'GET' and title not in moviesDict:
        return flask.Response(f'<h1>Nie ma takiego filmu: {title}, lista dostępnych filmów:</h1>' + '\n' + showAllMovies(moviesDict), 200)
    else:
        return flask.Response(f"<h1>Error</h1>", 405)


@app.route('/movies', methods=['GET'])
def getAllMovies():
    if flask.request.method == 'GET':
        return flask.Response('<h1>Lista dostępnych filmów:</h1>' + '\n' + showAllMovies(moviesDict), 200)

app.run(host='0.0.0.0')

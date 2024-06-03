from servidor import app, db_session

@app.route('/')
def index():
    return "Ainda não existem gatinhos por aqui."

if __name__ == '__main__':
    app.run()
from servidor import create_app


app = create_app()


if __name__ == '__main__':
    app.run(port=6102, debug=False)

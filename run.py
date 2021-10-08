from app import create_app, mongo, bcrypt, login_manager

app = create_app()
if __name__ == '__main__':
    app.run(debug=True)

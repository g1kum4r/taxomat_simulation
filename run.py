from app import create_app, mongo, bcrypt, login_manager

application = create_app()
if __name__ == '__main__':
    application.run(debug=True)

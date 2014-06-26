from todo import app
from flask.ext.script import Manager, Server
manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_reloader = True,
    host = '0.0.0.0')
)

if __name__ == "__main__":
    manager.run()

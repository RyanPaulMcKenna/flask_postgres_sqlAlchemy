from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from project import create_app
from project.extensions import db
from project.modules.users.models import Users


app = create_app()

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    print('Database dropped and recreated.')

@manager.command
def seed_db():
    """Seeds the database."""
    db.session.add(
        Users(username='admin',
              password='verysecurepassword',
              email='admin@gmail.com',
              admin=True))
    db.session.commit()
    print('Admin user added.')


if __name__ == '__main__':
    manager.run()

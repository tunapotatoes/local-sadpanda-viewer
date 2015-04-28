import sqlalchemy
import filecmp
#from migrate.versioning import api
import contextlib
from sqlalchemy.ext.declarative import declarative_base
import os
import imp
from Logger import Logger

CONFIG_DIR = os.path.expanduser("~/.lsv")
DB_NAME = "db.sqlite"
DATABASE_URI = "sqlite:///" + os.path.join(CONFIG_DIR, DB_NAME)
DATABASE_FILE = os.path.join(CONFIG_DIR, DB_NAME)
MIGRATE_REPO = os.path.join(CONFIG_DIR, "dbrepo/")

base = declarative_base()
engine = sqlalchemy.create_engine(DATABASE_URI)
session_maker = sqlalchemy.orm.sessionmaker(bind=engine)


class Database(Logger):
    "Dummy class to log in this file"
    pass

Database = Database()


class Config(base):
    __tablename__ = "config"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    version = sqlalchemy.Column(sqlalchemy.Text)
    json = sqlalchemy.Column(sqlalchemy.Text)


class Gallery(base):
    __tablename__ = "gallery"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    dead = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    path = sqlalchemy.Column(sqlalchemy.Text)
    type = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    thumbnail_path = sqlalchemy.Column(sqlalchemy.Text)
    image_hash = sqlalchemy.Column(sqlalchemy.Text)
    uuid = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    last_read = sqlalchemy.Column(sqlalchemy.Integer)
    read_count = sqlalchemy.Column(sqlalchemy.Integer, default=0, nullable=False)
    time_added = sqlalchemy.Column(sqlalchemy.Integer)
    metadata_collection = sqlalchemy.orm.relationship("Metadata", lazy="dynamic", backref="gallery")


class Metadata(base):
    __tablename__ = "metadata"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    json = sqlalchemy.Column(sqlalchemy.Text)
    gallery_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("gallery.id"))


def setup():
    Database.logger.debug("Setting up database.")
    if not os.path.exists(DATABASE_FILE):
        create()
    # migrate()


def create():
    Database.logger.debug("Creating new database")
    base.metadata.create_all(engine)
    # if not os.path.exists(MIGRATE_REPO):
    #     api.create(MIGRATE_REPO, "database repository")
    #     api.version_control(DATABASE_URI, MIGRATE_REPO)
    # else:
    #     api.version_control(DATABASE_URI, MIGRATE_REPO, api.version(MIGRATE_REPO))


# def migrate():
#     "Stolen from blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database"
#     Database.logger.debug("Creating new migration.")
#     version = api.db_version(DATABASE_URI, MIGRATE_REPO)
#     old_migration = os.path.join(MIGRATE_REPO, "versions", "%03d_migration.py" % version)
#     migration = os.path.join(MIGRATE_REPO, "versions", "%03d_migration.py" % (version + 1))
#     tmp_module = imp.new_module("old_model")
#     old_model = api.create_model(DATABASE_URI, MIGRATE_REPO)
#     exec(old_model, tmp_module.__dict__)
#     script = api.make_update_script_for_model(DATABASE_URI, MIGRATE_REPO, tmp_module.meta, base.metadata)
#     open(migration, "wt").write(script)
#     if os.path.exists(old_migration) and filecmp.cmp(old_migration, migration):
#         Database.logger.info("No new migration needed, deleting created migration.")
#         os.remove(migration)
#     else:
#         api.upgrade(DATABASE_URI, MIGRATE_REPO)


@contextlib.contextmanager
def get_session(requester):
    Database.logger.debug("New DB session requested from %s" % requester)
    session = None
    try:
        session = sqlalchemy.orm.scoped_session(session_maker)
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    setup()

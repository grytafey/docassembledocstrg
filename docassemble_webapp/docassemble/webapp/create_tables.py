import sys
import docassemble.webapp.config
from docassemble.webapp.config import daconfig
if __name__ == "__main__":
    docassemble.webapp.config.load(arguments=sys.argv)
from docassemble.base.util import word
from docassemble.webapp.app_and_db import app, db
from docassemble.webapp.packages.models import Package, PackageAuth, Install
from docassemble.webapp.core.models import Attachments, Uploads, SpeakList, Supervisors, KVStore
from docassemble.webapp.users.models import User, UserAuth, Role, UserRoles, UserDict, UserDictKeys, UserDictLock
from sqlalchemy import create_engine, MetaData
import docassemble.webapp.database
import random
import string
#from flask import Flask
#from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.user import UserManager, SQLAlchemyAdapter

if __name__ == "__main__":
    app.config['SQLALCHEMY_DATABASE_URI'] = docassemble.webapp.database.alchemy_connection_string()
    app.secret_key = daconfig.get('secretkey','28ihfiFehfoU34mcq_4clirglw3g4o87')

def populate_tables():
    existing_admin = Role.query.filter_by(name=word('admin')).first()
    if existing_admin:
        return
    defaults = daconfig.get('default_admin_account', {'nickname': 'admin', 'email': 'admin@admin.com', 'password': 'password'})
    admin_role = Role(name=word('admin'))
    user_role = Role(name=word('user'))
    developer_role = Role(name=word('developer'))
    advocate_role = Role(name=word('advocate'))
    db.session.add(admin_role)
    db.session.add(user_role)
    db.session.add(developer_role)
    db.session.add(advocate_role)
    user_manager = UserManager(SQLAlchemyAdapter(db, User, UserAuthClass=UserAuth), app)
    user_auth = UserAuth(password=app.user_manager.hash_password(defaults['password']))
    user = User(
        active=True,
        nickname=defaults['nickname'],
        social_id='local$' + ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32)),
        email=defaults['email'],
        user_auth=user_auth
    )
    user.roles.append(admin_role)
    db.session.add(user_auth)
    db.session.add(user)
    db.session.commit()
    return

if __name__ == "__main__":
    #db.drop_all()
    db.create_all()
    populate_tables()
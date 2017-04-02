from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from models import db
db.init_app(app)

from copyright import models

from copyright.home.controllers import homeRoutes
app.register_blueprint(homeRoutes)

from copyright.create.controllers import createRoutes
app.register_blueprint(createRoutes)

from copyright.purchase.controllers import purchaseRoutes
app.register_blueprint(purchaseRoutes)
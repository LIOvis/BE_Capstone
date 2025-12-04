import routes

def register_blueprint(app):
    app.register_blueprint(routes.auth)
    app.register_blueprint(routes.cuisine)
    app.register_blueprint(routes.image)
    app.register_blueprint(routes.ingredient)
    app.register_blueprint(routes.preference)
    app.register_blueprint(routes.recipe)
    app.register_blueprint(routes.user)

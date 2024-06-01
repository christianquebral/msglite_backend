#from decouple import config
from flask import Flask
from flask_cors import CORS
from flask_restful import Api, Resource
from session import Session

import markdown
import os
import ssl

app = Flask(__name__)
CORS(app)
api = Api(app)


@app.route("/")
def index():
    with open(os.path.dirname(app.root_path) + "/README.md", "r") as readme:
        content = readme.read()
        return markdown.markdown(content)

api.add_resource(Session, "/session")

app.run(host="0.0.0.0", port=80, debug=True)

# if config("ENV") == "PROD":
#     ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
#     ctx.load_cert_chain("./cert/fullchain.pem", "./cert/privkey.pem")
#     app.run(host="0.0.0.0", port=80, debug=False, ssl_context=ctx)

# else:
#     app.run(host="0.0.0.0", port=80, debug=True)

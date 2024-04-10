import os
from flask import Flask

app = Flask(__name__)

from controllers import * # importando todos os controllers

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
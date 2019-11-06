import os
import sys
from server import init_app

if __name__ == '__main__':
    app = init_app()
    app.run()

import os

from app import app
import app.views.student

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.app.run('0.0.0.0', port=port)

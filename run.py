
import os

from app import app
import app.views.debug
import app.views.student_view
import app.views.backend
import app.views.navigation
import app.views.event

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.app.run('0.0.0.0', port=port)

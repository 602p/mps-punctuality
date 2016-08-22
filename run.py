
import os

from app import app
import app.views.student
import app.views.event
import app.views.consequence
import app.views.navigation
import app.views.student_view

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.app.run('0.0.0.0', port=port)

# This file is used by Apache2 mod_wsgi. If you are using a virtualenv
# and strictly follwoed the installation instructions, leave in the
# first 2 line. If you are not using a virtualenv, comment the
# first 2 lines.

activate_this = '/var/www/Twenty47/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0, '/var/www/Twenty47')

from twenty47 import app as application

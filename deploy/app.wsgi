#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/vehicle-catalog-project/")
from deploy.project import app as application
application.secret_key = 'super secret key'



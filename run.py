#!/usr/bin/python
from app import app

# Launch on all available interfaces
app.run(debug=True,host='0.0.0.0')

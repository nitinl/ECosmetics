"""
Description: Script for starting the flask application. Usage: $ python ECosmetics.py
"""
from controller import app

if __name__ == '__main__':
    app.run(debug=True)

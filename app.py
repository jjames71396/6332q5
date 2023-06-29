#Programming Assignment 5
#Jordan James 1001879608
#CSE 6332-002
import os
import json
import random
import pandas as pd
import numpy as np
import nltk
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')


@app.route('/results', methods=['POST'])
def results():
    arg = request.form.get('name')
    results = None
    if results is not None:
       return render_template('results.html', name = results)
    else:
       return redirect(url_for('index'))

if __name__ == '__main__':
   app.run()

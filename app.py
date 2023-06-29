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
password = None
four = None
l1 = None
l2 = None

def check_string(string):
    # Check if the string contains #@+-%
    if any(char in string for char in '#@+-%%'):
        # Check if the string contains !@$*
        if not any(char in string for char in '!$*'):
            return True
    return False

    
def check_string2(string):
    capital_count = 0
    number_count = 0

    for char in string:
        if char.isupper():
            capital_count += 1
        elif char.isdigit():
            number_count += 1

    if capital_count >= 2 and number_count >= 1:
        return True
    else:
        return False
        
def extract_text_within_tags(html_string):
    tags = ['<b>', '</b>', '<i>', '</i>', '<p>', '</p>', '<h1>', '</h1>']
    extracted_text = []

    while html_string:
        start_tag_pos = None
        for tag in tags:
            if tag in html_string:
                start_tag_pos = html_string.find(tag)
                break

        if start_tag_pos is not None:
            end_tag_pos = html_string.find(tags[tags.index(tag) + 1])
            if end_tag_pos != -1:
                extracted_text.append(html_string[start_tag_pos + len(tag):end_tag_pos])
                html_string = html_string[end_tag_pos + len(tags[tags.index(tag) + 1]):]
            else:
                break
        else:
            break

    return extracted_text
    
def remove_tags(html_string):
    tags = ['<b>', '</b>', '<i>', '</i>', '<p>', '</p>', '<h1>', '</h1>']

    for tag in tags:
        html_string = html_string.replace(tag, '')

    return html_string

def remove_word(text, word):
    return text.replace(word, '')    


def check_strings(original_strings, check_strings):
    trigrams_list = ["_".join(item) for item in nltk.trigrams(original_strings.split(' '))]
    for check_str in check_strings:
        found = False
        for original_str in trigrams_list:
            if check_str in original_str:
                found = True
                break
        if not found:
            return False
    return True

def find_words(text, words):
    trigrams_list = ["_".join(item) for item in nltk.trigrams(text.split(' '))]
    print(trigrams_list)
    for word in trigrams_list:
        for w in words:
            if w not in word:
                return False
    return True if all(word in string for word in word_list) else False

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')


@app.route('/htmldoc', methods=['POST'])
def htmldoc():
    arg = request.form.get('name')
    print(arg)
    text = extract_text_within_tags(arg)
    txt = ""
    for t in text:
        txt += t
        txt += " "
        
    print(txt)
    return render_template('results.html', name = txt) 
    


@app.route('/htmldoc2', methods=['POST'])
def htmldoc2():
    arg = request.form.get('name')
    text = remove_tags(arg)
    txt = ""
    for t in text:
        txt += t
        txt += " "
    return render_template('results.html', name = txt) 
    
@app.route('/te', methods=['POST'])
def te():
    text = request.form['text']
    word = request.form['word']
    words = request.form['words'].split()
    action = request.form['action']
    
    modified_text = text
    if action == 'RM':
        modified_text = remove_word(modified_text, word)
    elif action == 'F':
        bo = check_strings(modified_text, words)
        modified_text = "not found"
        if bo:
            modified_text = " found"
    
    return render_template('index.html', text=text, modified_text=modified_text, word=word, words=' '.join(words), action=action)
    
    
@app.route('/admin', methods=['POST'])
def admin():
    arg = request.form.get('name')
    args = arg.split(' ')
    global l1
    global l2
    l1 = int(args[0])
    l2 = int(args[1])
    global four
    four = args[2]
    
    if results is not None:
       return render_template('cp.html')
    else:
       return redirect(url_for('index'))
       
@app.route('/cp', methods=['POST'])
def cp():
    arg = request.form.get('name')
    global l1
    global l2
    global four
    valid = None
    if len(arg) < l1 or len(arg) > l2:
        valid = False
    if valid is None:
        valid = check_string(arg)
        for c in arg:
            if c == four:
                valid = False
                break
    if valid:
        valid = check_string2(arg)
    if valid:
        return render_template('results.html', name = 'valid')
    else:
        return render_template('results.html', name = 'invalid')
    
    
@app.route('/results', methods=['POST'])
def results():
    arg = request.form.get('name')
    global l1
    global l2
    global four
    valid = None
    print(l1)
    print(l2)
    if len(arg) < l1 or len(arg) > l2:
        valid = False
    print(valid)
    if valid is None:
        valid = check_string(arg)
        for c in arg:
            if c == four:
                valid = False
                break
    if valid:
        valid = check_string2(arg)
    if valid:
        return render_template('results.html', name = 'valid')
    else:
        return render_template('results.html', name = 'invalid')

if __name__ == '__main__':
   app.run()

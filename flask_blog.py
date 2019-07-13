from flask import Flask,render_template, url_for, flash, redirect, jsonify, request
from forms import DNAEntry, DNADelete, DNAUpdate
import sqlite3
import ctypes
from random import sample

#webapp
app = Flask(__name__)

#setting the mode
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
app.config['SECRET_KEY'] = 's200195'

#Inserting new DNA into the database
@app.route("/", methods=['GET', 'POST'])
@app.route("/entry", methods=['GET', 'POST'])
def entry():
    conn = sqlite3.connect('DNA.db')
    cur = conn.cursor()
    form = DNAEntry()
    if form.validate_on_submit():
        #checking if the DNA is already in the database
        cur.execute('SELECT * FROM DNA WHERE DNA=:DNA', {'DNA':form.DNA.data})
        if len(cur.fetchall()) > 0:
            flash(f'The DNA is already in the database, please recheck')
            return redirect(url_for('entry'))
        else:
            with conn:
                cur.execute('INSERT INTO DNA VALUES(:DNA, :Disease, :Description)',
                            {'DNA':form.DNA.data, 'Disease':form.Disease.data,
                             'Description':form.Description.data})
                conn.commit()
                flash(f'Successfully added {form.Disease.data} to database', 'success')
            return redirect(url_for('entry'))

    return render_template('entry.html', title='DNA entry', form=form)

#deleting data from the database
@app.route('/delete', methods={'GET', 'POST'})
def delete():
    conn = sqlite3.connect('DNA.db')
    cur = conn.cursor()
    form = DNADelete()
    #deleting the specific disease from the database of DNA
    if form.validate_on_submit():
        cur.execute('DELETE FROM DNA WHERE Disease=:Disease',
                    {'Disease':form.Disease.data})
        conn.commit()
        flash(f'Deleted the specific dataset')
        return redirect(url_for('delete'))

    return render_template('delete.html', form=form)

#TEMPORARILY DELETED
# #displaying data from the database 
# @app.route('/display', methods={'GET', 'POST'})
# def analyze():
#     conn = sqlite3.connect('DNA.db')
#     cur = conn.cursor()
#     selecting_all = cur.execute('SELECT * FROM DNA')
#     all_dataset = cur.fetchall()
#     return render_template('display.html', all_dataset=all_dataset)
#UNCOMMENT EVERYTHING ABOVE


#CHANGE TO POST AFTER
@app.route('/display/data', methods=['GET'])
def data():
    conn = sqlite3.connect('DNA.db')
    cur = conn.cursor()
    selecting_all = cur.execute('SELECT * FROM DNA')
    all_dataset = cur.fetchall()
    #test = request.form['name']
    return jsonify({'results': all_dataset})

@app.route('/display')
def analyze():
    return render_template('display.html')

#updating the database
@app.route('/update', methods=['GET', 'POST'])
def update():
    conn = sqlite3.connect('DNA.db')
    cur = conn.cursor()
    form = DNAUpdate()
    if form.validate_on_submit():

        #checking which information needs updating
        DNA_len = len(form.DNA.data)
        Description_len = len(form.Description.data)

        #updating the appropriate elements of the database
        if DNA_len == 0  and Description_len > 0:
            cur.execute('UPDATE DNA SET Description=:Description WHERE '
                        'Disease=:Disease',
                        {'Description':form.Description.data,
                         'Disease':form.Disease.data})
            conn.commit()
        elif DNA_len > 0 and Description_len == 0:
            cur.execute('UPDATE DNA SET DNA=:DNA WHERE '
                        'Disease=:Disease',
                        {'DNA': form.DNA.data,
                         'Disease': form.Disease.data})
            conn.commit()
        else:
            cur.execute('UPDATE DNA SET DNA=:DNA, Description=:Description '
                        'WHERE '
                        'Disease=:Disease',
                        {'DNA': form.DNA.data, 'Description':form.Description.data,
                         'Disease': form.Disease.data})
            conn.commit()
        return redirect(url_for('update'))

    return render_template('update.html', form=form)



if __name__ == "__main__":
    app.run(debug=True)
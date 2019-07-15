from flask import Flask,render_template, url_for, flash, redirect, jsonify, request
from forms import DNAEntry, DNADelete, DNAUpdate
import sqlite3
import ctypes
from gene import DNA
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
    #connecting to the databse
    conn = sqlite3.connect('DNA.db')
    cur = conn.cursor()
    form = DNAEntry()

    #checking if the form was submitted
    if form.validate_on_submit():

        #checking if the DNA is already in the database
        cur.execute('SELECT * FROM DNA WHERE DNA=:DNA', {'DNA':form.DNA.data})
        if len(cur.fetchall()) > 0:
            flash(f'The DNA is already in the database, please recheck')
            return redirect(url_for('entry'))
        else:
            #inserting the new dataset into the DNA database
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
    #connecting to the database
    conn = sqlite3.connect('DNA.db')
    cur = conn.cursor()

    #initializing the form on the page
    form = DNADelete()

    #checking if the form is submitted
    if form.validate_on_submit():

        #deleting the disease form the database
        cur.execute('DELETE FROM DNA WHERE Disease=:Disease',
                    {'Disease':form.Disease.data})
        conn.commit()
        flash(f'Deleted the specific dataset')

        #redirecting to a fresh version of the delete page
        return redirect(url_for('delete'))

    return render_template('delete.html', form=form)

#displaying data from the database 
@app.route('/display', methods={'GET', 'POST'})
def analyze():
    return render_template('display.html')

#sending data to client
@app.route('/display/data', methods=['POST'])
def data():
    #connecting to the database
    conn = sqlite3.connect('DNA.db')
    cur = conn.cursor()

    #creating the form for g
    disease = request.form['disease']
    if disease:

        #obtainng the DNA data
        cur.execute('SELECT * FROM DNA WHERE Disease=:Disease', {'Disease':disease})
        output = cur.fetchall()[0]
        dna = DNA(output[0])

        #creating a DNA class object
        conn.commit()
        print(dna.count())
        return jsonify({'DNA':dna.gene, 'DNA_Count':dna.count()})

    return jsonify({'disease': 'error'})

#updating the database
@app.route('/update', methods=['GET', 'POST'])
def update():
    #connecting to the database
    conn = sqlite3.connect('DNA.db')
    cur = conn.cursor()
    form = DNAUpdate()

    #checking if the form is submitted
    if form.validate_on_submit():

        #checking which information needs updating
        DNA_len = len(form.DNA.data)
        Description_len = len(form.Description.data)

        #updating the appropriate elements of the database
        if DNA_len == 0  and Description_len > 0:

            #updating only the description
            cur.execute('UPDATE DNA SET Description=:Description WHERE '
                        'Disease=:Disease',
                        {'Description':form.Description.data,
                         'Disease':form.Disease.data})
            conn.commit()
        elif DNA_len > 0 and Description_len == 0:

            #updating only the DNA
            cur.execute('UPDATE DNA SET DNA=:DNA WHERE '
                        'Disease=:Disease',
                        {'DNA': form.DNA.data,
                         'Disease': form.Disease.data})
            conn.commit()
        else:

            #updating both
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
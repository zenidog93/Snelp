from flask_app import app   
from flask import render_template, request, redirect, session, flash

from flask_app.models import ride_model
from flask_app.models import user_model
from flask_app.models import destination_model


@app.route('/display/create/ride/form')
def display_create_ride_form():
    if 'user_id'  not in session:
        return redirect ('/display/user/login')
    all_mountains = destination_model.Destination.get_all_mountains()
    return render_template('display_create_ride_form.html', all_mountains = all_mountains)

@app.route('/ride/create', methods=['POST'])
def create_ride():
    if 'user_id'  not in session:
        return redirect ('/display/user/login')
    
    if not ride_model.Ride.validate_ride(request.form):
        return redirect('/display/create/ride/form')
    
    ride_data = {
        **request.form,
        'user_id' : session['user_id'],
    }
    
    ride_model.Ride.create_ride(ride_data)
    
    return redirect('/user_dashboard')

@app.route('/ride/edit/<int:id>')
def display_ride_edit_page(id):
    if 'user_id'  not in session:
        return redirect ('/display/user/login')
    ride_data = {
        'id' : id
    }
    
    this_ride = ride_model.Ride.get_one_ride_for_edit(ride_data)
    return render_template('display_ride_edit_page.html', this_ride = this_ride)

@app.route('/rides/<int:id>/update', methods = ['POST'])
def update_ride(id):
    if 'user_id'  not in session:
        return redirect ('/display/user/login')
    if not ride_model.Ride.validate_ride(request.form):
        return redirect(f'/ride/edit/{id}')
    
    ride_data = {
        **request.form,
        'id':id
    }
    
    ride_model.Ride.update_ride(ride_data)
    return redirect('/user_dashboard')

@app.route('/delete/<int:id>')
def delete_ride(id):
    if 'user_id'  not in session:
        return redirect ('/display/user/login')
    print(id)
    
    ride_model.Ride.delete_ride({'id':id})
    return redirect('/user_dashboard')
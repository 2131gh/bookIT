def user():
    return dict(form=auth())# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
auth.requires_login()
def details():
    return dict()

@auth.requires_login()
def store():
    submitted_hotel_name=request.vars.hotel_name
    submitted_description = request.vars.description
    submitted_hotelclass = request.vars.hotelclass
    submitted_contactnumber = request.vars.contactnumber
    submitted_rooms = request.vars.rooms
    submitted_minimumprice = request.vars.minimumprice
    submitted_email = request.vars.email
    submitted_files = request.vars.files

    results = db.hotels.insert(
            db_hotel_name=submitted_hotel_name,
            db_description=submitted_description,
            db_hotelclass=submitted_hotelclass,
            db_contactnumber=submitted_contactnumber,
            db_rooms=submitted_rooms,
            db_minimumprice=submitted_minimumprice,
            db_email=submitted_email,

        )

    if results:
        for image in submitted_files:
            db.images.insert(hotel_id=results.id, file=image)
        session.flash = "Hotel added successfully"
        redirect(URL('admindashboard'))
    else:
        session.flash = "Error occurred while adding a Hotel. Please try again"
        redirect(URL('details'))


@auth.requires_login()
def seeDetails():
    hotels =db().select(db.hotels.ALL)
    return dict(hotels=hotels)


@auth.requires_login()
def editdetails():
    parameters = request.args
    submitted_id = parameters[0]
    hotel = db.hotels(submitted_id)
    if hotel:
        return dict(hotel=hotel)
    redirect(URL('admindashboard'))

    
@auth.requires_login()
def update():
    submitted_hotel_name=request.vars.hotel_name
    submitted_description = request.vars.description
    submitted_hotelclass = request.vars.hotelclass
    submitted_contactnumber = request.vars.contactnumber
    submitted_rooms = request.vars.rooms
    submitted_minimumprice = request.vars.minimumprice
    submitted_email = request.vars.email
    submitted_id = request.vars.id

    if db(db.hotels.id == submitted_id).select():

        db(db.hotels.id == submitted_id).update(
            db_hotel_name=submitted_hotel_name,
            db_description=submitted_description,
            db_hotelclass=submitted_hotelclass,
            db_contactnumber=submitted_contactnumber,
            db_rooms=submitted_rooms,
            db_minimumprice=submitted_minimumprice,
            db_email=submitted_email
            )
        session.flash = "Hotel updated successfully"
        redirect(URL('admindashboard'))
    else:
        session.flash = "There was an error while updating Hotel"
        redirect(URL('editdetails', args=submitted_id))

@auth.requires_login()
def delete():
    parameters = request.args
    submitted_id = parameters[0]

    if db(db.hotels.id == submitted_id).select():

        db(db.hotels.id == submitted_id).delete()
        session.flash = "Hotel deleted successfully"
        redirect(URL('admindashboard'))

    else:
        session.flash = "There was an error while deleting Hotel. Please try again"
        redirect(URL('admindashboard'))

@auth.requires_login()
def addservice():
    parameters = request.args
    hotel_id = parameters[0]
    return dict(hotel_id=hotel_id)

@auth.requires_login()
def storeservice():
    submitted_title = request.vars.title
    submitted_description = request.vars.description
    submitted_files = request.vars.file
    submitted_price = request.vars.price
    submitted_hotel_id = request.vars.hotel_id
    

    results = db.services.insert(
            db_title=submitted_title,
            db_description=submitted_description,
            db_price=submitted_price,
            db_hotel_id=submitted_hotel_id
           )    

    if results:
        for image in submitted_files:
            db.images.insert(service_id=results.id, file=image)
        session.flash = "Service added successfully"
        redirect(URL('hotelDetails', args=submitted_hotel_id))
    else:
        session.flash = "Error while adding a service. Please try again"
        redirect(URL('addservice', args=submitted_hotel_id))
        

@auth.requires_login()
def checkservice():
    hotel_id = request.args[0]
    services =db(db.services.db_hotel_id==hotel_id).select()
    return dict(services=services)

@auth.requires_login()
def editservices():
    parameters = request.args
    submitted_id = parameters[0]
    return dict(submitted_id=submitted_id)

@auth.requires_login()
def updateservice():
    submitted_title = request.vars.title
    submitted_description = request.vars.description
    submitted_price = request.vars.price
    submitted_id = request.vars.id

    if db(db.services.id == submitted_id).select():

        db(db.services.id == submitted_id).update(
            db_title = submitted_title,
            db_description = submitted_description,
            db_price =submitted_price
            )
        session.flash = "Service updated successfully"
        redirect(URL('admindashboard'))

    else:
        session.flash = "There was an error while updating Service. Please try again"
        redirect(URL('editservices', args=submitted_id))
        
@auth.requires_login()
def deleteservice():
    parameters = request.args
    submitted_id = parameters[0]

    if db(db.services.id == submitted_id).select():
        db(db.services.id == submitted_id).delete()
        session.flash = "Service deleted successfully"
        redirect(URL('admindashboard'))

    else:
        session.flash = "There was an error while deleting Service. Please try again"
        redirect(URL('admindashboard'))


@auth.requires_login()
def admindashboard():
    hotels =db(db.hotels.created_by==auth.user.id).select(orderby=~db.hotels.id)
    return dict(hotels=hotels)

@auth.requires_login()
def hotelDetails():
    hotel_id = request.args[0]
    services =db(db.services.db_hotel_id==hotel_id).select()
    images =db(db.images.hotel_id==hotel_id).select()
    hotel = db.hotels(hotel_id)
    return dict(hotel=hotel, services=services, images=images)

@auth.requires_login()
def hotelServices():
    service_id = request.args[0]
    service = db.services(service_id)
    images =db(db.images.service_id==service_id).select()
    return dict(service=service, images=images)


def download():
    return response.download(request, db)

def index():
    hotels =db().select(db.hotels.ALL)
    return dict(hotels=hotels)

def hotel_details():
    hotel_id = request.args[0]
    services =db(db.services.db_hotel_id==hotel_id).select()
    images =db(db.images.hotel_id==hotel_id).select()
    hotel = db.hotels(hotel_id)
    return dict(hotel=hotel, services=services, images=images)

def hotel_services():
    service_id = request.args[0]
    service = db.services(service_id)
    images =db(db.images.service_id==service_id).select()
    return dict(service=service, images=images)


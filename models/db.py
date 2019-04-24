from gluon.contrib.appconfig import AppConfig 
configuration = AppConfig(reload=True)

db = DAL("sqlite://storage.sqlite")


from gluon.tools import Auth
auth = Auth(db)
auth.define_tables(username=True)

db.define_table("hotels",
                    Field('db_hotel_name'),
                    Field('db_description'),                                                    
                    Field('db_hotelclass'),  
                    Field('db_contactnumber'),
                    Field('db_rooms'), 
                    Field('db_minimumprice'), 
                    Field('db_email'),
                    auth.signature)

db.define_table("services",
                    Field('db_hotel_id'),
                    Field('db_title'),
                    Field('db_description'),
                    Field('db_price'))

db.define_table("images",
                    Field('hotel_id'),
                    Field('service_id'),
                    Field('file','upload'))


def getImage(hotel_id):
    return db(db.images.hotel_id==hotel_id).select()[0]
    

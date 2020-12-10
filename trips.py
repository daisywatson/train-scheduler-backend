import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

from flask_login import current_user


trip = Blueprint('trips', 'trip')

# current directory is this '/api/v1/trips
# @trip.route('/', methods=["GET"])
# def get_all_trips():
#     try:
#         trips= [model_to_dict(trip) for trip in models.Trip.select()]
#         print(trips)
#         return jsonify(data=trips, status={"code": 201, "message": "Success"})
#     except models.DoesNotExist:
#         return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@trip.route('/mypage', methods=["GET"])
def get_my_trips():
    try:
        trips = [model_to_dict(trip) for trip in current_user.trips]
        for trip in trips:
            trip['time']=trip['time'].__str__()
        print(trips)
        return jsonify(data=trips, status={"code": 201, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

# Create route
@trip.route('/mypage/create', methods=["POST"])
def create_trips():
    payload = request.get_json()

    print(type(payload), 'payload')

    new_trip= models.Trip.create(name=payload['name'],
    uploader=current_user.id, center_lat=payload['center_lat'],
    center_long=payload['center_long'], pin1_title=payload['pin1_title'],
    pin1_subtitle=payload['pin1_subtitle'], pin1_text=payload['pin1_text'],
    pin1_color=payload['pin1_color'], pin1_lat=payload['pin1_lat'],
    pin1_long=payload['pin1_long'], pin2_title=payload['pin2_title'],
    pin2_subtitle=payload['pin2_subtitle'], pin2_text=payload['pin2_text'],
    pin2_color=payload['pin2_color'], pin2_lat=payload['pin2_lat'],
    pin2_long=payload['pin1_long'], date=payload['date'], time=payload['time'])
    ## see the object
    print(trip.__dict__)
    ## Look at all the methods
    print(dir(trip))

    # Change the model to a dict
    trip_dict = model_to_dict(new_trip)
    return jsonify(data=trip_dict, status={"code": 201, "message": "Success"})

# Show route
@trip.route('/mypage/<id>', methods=['GET'])
def get_one_trip(id):
    trip = model_to_dict(models.Trip.get_by_id(id))
    trip['time']=trip['time'].__str__()

    return jsonify(data=trip, status={"code": 200, "message": "Success"})

# Update route
@trip.route('/mypage/<id>', methods=["PUT"])
def update_trip(id):
    payload = request.get_json()
    print(payload)

    query = models.Trip.update(**payload).where(models.Trip.id==id)
    query.execute()
    trip = model_to_dict(models.Trip.get_by_id(id))
    trip['time']=trip['time'].__str__()
    return jsonify(data=trip, status={"code": 200, "message": "Success"})

# Delete route
@trip.route('/mypage/<id>', methods=["Delete"])
def delete_trip(id):
    #delete trip with id
    delete_query = query = models.Trip.delete().where(models.Trip.id==id)
    num_of_rows_deleted = delete_query.execute()
    print(num_of_rows_deleted)


    return jsonify(
    data={},
    message="Successfully deleted {} trip with id {}".format(num_of_rows_deleted, id),
    status={"code": 200, "message": "Success"}
    )

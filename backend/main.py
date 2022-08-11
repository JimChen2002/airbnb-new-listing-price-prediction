# main.py
import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from joblib import load
import numpy as np
import pandas as pd
from models.prediction import PredictionModel
import math

svr_model = load('svr_model.joblib')
svc_model = load('svc_model.joblib')

bathroom_options = ['1 bath', '1 private bath', '1 shared bath', '1.5 baths',
    '1.5 shared baths', '2 baths', '2 shared baths', '2.5 baths',
    '2.5 shared baths', '3 baths', '3 shared baths', '3.5 baths',
    '3.5 shared baths', '4.5 baths', '5 baths', '5 shared baths',
    '6 shared baths', 'Half-bath']
neighbourhood_options = ['Allston', 'Back Bay', 'Bay Village',
    'Beacon Hill', 'Brighton', 'Charlestown', 'Chinatown', 'Dorchester',
    'Downtown', 'East Boston', 'Fenway', 'Hyde Park', 'Jamaica Plain',
    'Leather District', 'Longwood Medical Area', 'Mattapan', 'Mission Hill',
    'North End', 'Roslindale', 'Roxbury', 'South Boston',
    'South Boston Waterfront', 'South End', 'West End', 'West Roxbury']
property_options = ['Boat', 'Entire condominium (condo)', 'Entire guest suite',
       'Entire guesthouse', 'Entire loft', 'Entire rental unit',
       'Entire residential home', 'Entire serviced apartment',
       'Entire townhouse', 'Houseboat', 'Private room in bed and breakfast',
       'Private room in bungalow', 'Private room in condominium (condo)',
       'Private room in guest suite', 'Private room in loft',
       'Private room in rental unit', 'Private room in residential home',
       'Private room in townhouse', 'Private room in villa',
       'Room in bed and breakfast', 'Room in boutique hotel', 'Room in hotel',
       'Shared room in condominium (condo)', 'Shared room in residential home',
       'Shared room in townhouse']
room_options = ['Entire home/apt', 'Hotel room', 'Private room', 'Shared room']
numerical_features = ['accommodates', 'bedrooms', 'beds']
chosen_amenities = ['Lock on bedroom door', 'Private entrance',
    'Pack \u2019n play/Travel crib', 'Elevator', 'Iron', 'Hair dryer', 'Microwave',
    'Free street parking',  'Cable TV', 'Ethernet connection']
other_features = ['is_bath_shared']
all_features = bathroom_options + neighbourhood_options + property_options \
    + room_options + numerical_features + chosen_amenities + other_features
bins = [100, 200, 300]
accommodates_mean = 3.3652482269503547
accommodates_std = 2.4253971179001046
bedrooms_mean = 1.5301418439716312
bedrooms_std = 0.9325550091702445
beds_mean = 1.9078014184397163
beds_std = 1.5328585877135132


def get_id(s):
    for i in range(len(all_features)):
        if all_features[i] == s:
            return i
    return -1

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/predictPrice/")
async def predict_price(input: PredictionModel):
    input = jsonable_encoder(input)
    accommodates = input["accommodates"]
    bedrooms = input["bedrooms"]
    beds = input["beds"]
    neighbourhood = input["neighbourhood"]
    bathroom_type = input["bathroom_type"]
    property_type = input["property_type"]
    room_type = input["room_type"]
    amenities = input["amenities"]

    tmp = [0 for i in range(len(all_features))]
    tmp[get_id("accommodates")] = (accommodates - accommodates_mean) / accommodates_std
    tmp[get_id("bedrooms")] = (bedrooms - bedrooms_mean) / bedrooms_std
    tmp[get_id("beds")] = (beds - beds_mean) / beds_std
    tmp[get_id(neighbourhood)] = 1
    tmp[get_id(bathroom_type)] = 1
    tmp[get_id(property_type)] = 1
    tmp[get_id(room_type)] = 1
    for x in amenities:
        tmp[get_id(x)] = 1
    X = pd.DataFrame([tmp], columns=all_features)
    
    price = svr_model.predict(X)
    range_id = svc_model.predict(X)
    if range_id == 0:
        range_text = "Less than $100"
    elif range_id == 1:
        range_text = "$100 - $200"
    elif range_id == 2:
        range_text = "$200 - $300"
    else:
        range_text = "More than $300"
    return {"message": "Success!", "price": math.exp(price[0]), "range": range_text}
    
if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
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
import re
import time

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
chosen_amenities = ['Wifi', 'Smoke alarm', 'Long term stays allowed', 'Carbon monoxide alarm', 'Kitchen', 'Essentials', 'Heating', 'Hangers', 'Hair dryer', 'Air conditioning', 'Iron', 'Shampoo', 'Hot water', 'Refrigerator', 'Microwave', 'Dedicated workspace', 'Washer', 'Coffee maker', 'Dryer', 'Dishes and silverware', 'Cooking basics', 'Bed linens', 'Oven', 'TV', 'Fire extinguisher', 'Stove', 'Dishwasher', 'Extra pillows and blankets', 'First aid kit', 'Private entrance', 'Free street parking', 'Cable TV', 'Luggage dropoff allowed', 'TV with standard cable', 'Security cameras on property', 'Keypad', 'Lock on bedroom door', 'Lockbox', 'Elevator', 'Bathtub', 'Free parking on premises', 'Shower gel', 'Freezer', 'Baking sheet', 'Gym', 'Toaster', 'Patio or balcony', 'Hot water kettle', 'Dining table', 'Body soap', 'Backyard', 'Cleaning products', 'Laundromat nearby', 'Paid parking off premises', 'Wine glasses', 'BBQ grill', 'Pack \\u2019n play/Travel crib', 'Conditioner', 'Room-darkening shades', 'Indoor fireplace', 'Smart lock', 'Pool', 'Ethernet connection', 'Breakfast', 'Paid parking on premises', 'Trash compactor', 'Outdoor furniture', 'Host greets you', 'Portable fans', 'Clothing storage: closet', 'Pocket wifi', 'Keurig coffee machine', 'Crib', 'Central heating', 'Children\\u2019s books and toys', 'Clothing storage', 'High chair', 'Mini fridge', 'Ceiling fan', 'Private patio or balcony', 'Shared patio or balcony', 'Outdoor dining area', 'Single level home', 'Cleaning before checkout', 'Barbecue utensils', 'Window AC unit', 'Building staff', ', ', 'Paid parking garage off premises', 'Dryer \\u2013\\u00a0In unit', 'Stainless steel oven', 'Washer \\u2013\\u00a0In unit', 'Paid washer \\u2013 In building', 'TV with Chromecast', 'Window guards', 'Dryer \\u2013 In building', 'Washer \\u2013\\u00a0In building', 'Central air conditioning', 'Drying rack for clothing', 'Children\\u2019s dinnerware', 'EV charger', 'Board games', 'Paid dryer \\u2013 In building', 'Hot tub', 'Babysitter recommendations', 'Waterfront', 'Beach essentials', 'Fireplace guards', 'Free dryer \\u2013 In unit', 'Outlet covers', 'Baby safety gates', 'Safe', 'Clothing storage: dresser and closet', 'Rice maker', 'Radiant heating', 'Beachfront', 'Clothing storage: closet and dresser', 'Fire pit', 'Baby bath', 'Free washer \\u2013 In unit', 'Private garden or backyard', 'Private fenced garden or backyard', 'Shared garden or backyard', 'Shared fenced garden or backyard', 'Changing table', 'Stainless steel gas stove', 'Electric stove', 'Dedicated workspace: table', 'Pour-over coffee', 'Bath & Body Works conditioner', 'Baby monitor', 'Paid parking lot off premises', 'Sound system', '32\\', 'Bath & Body Works shampoo', 'Paid parking lot on premises \\u2013 1 space', 'Free washer \\u2013 In building', 'Paid parking garage on premises', 'Game console', 'Nespresso machine', 'Bath & Body Works body soap', 'Free dryer \\u2013 In building', 'Clothing storage: wardrobe', 'Lake access', 'Bread maker', 'Dedicated workspace: desk and office chair', 'Bidet', 'Gas stove', '55\\', 'Free driveway parking on premises \\u2013 1 space', 'Stainless steel stove', 'Pool table', 'Mosquito net', 'Clothing storage: dresser', 'Stainless steel electric stove', 'HDTV with Roku', '65\\', 'Paid street parking off premises', 'Shared pool', 'Piano', 'Dove body soap', '50\\', 'Paid parking lot on premises', 'HDTV', 'Dedicated workspace: desk', 'Paid dryer', 'Clothing storage: walk-in closet', 'Paid washer', 'TV with Roku', 'Bikes', 'HDTV with standard cable', '40\\', 'Free driveway parking on premises', 'Portable heater', 'Dedicated workspace: office chair and desk', 'Ping pong table', 'Google Home Bluetooth sound system', 'Free driveway parking on premises \\u2013 2 spaces', 'Pantene conditioner', 'Private hot tub', 'Record player', 'Children\\u2019s books and toys for ages 0-2 years old and 2-5 years old', 'Shared gym in building', 'Clothing storage: walk-in closet and closet', 'Clothing storage: wardrobe and dresser', 'Shared hot tub', '52\\', 'Bluetooth sound system', '42\\', 'Shared outdoor pool', 'Portable air conditioning', 'Induction stove', 'HDTV with Amazon Prime Video, HBO Max, Netflix, standard cable', 'Pantene shampoo', 'TV with Amazon Prime Video, HBO Max, Netflix, Roku, standard cable', '43\\', 'Fast wifi \\u2013 54 Mbps', 'Free dryer', 'Clothing storage: dresser and wardrobe', 'Free wifi', 'Paid parking lot on premises \\u2013 2 spaces', 'Not sure  body soap', '75\\', 'Private gym in building', 'Paid dryer \\u2013 In unit', 'Dedicated workspace: office chair, table, and desk', 'Private pool', 'Table corner guards', 'Clothing storage: closet and walk-in closet', 'Clothing storage: closet, dresser, and walk-in closet', 'Clothing storage: walk-in closet, dresser, and closet', 'Bosch refrigerator', 'Outdoor shower', 'Beekman shampoo', 'Paid washer \\u2013 In unit', 'Dedicated workspace: desk, table, and office chair', 'Samsung stainless steel oven', 'Clothing storage: dresser, walk-in closet, and closet', 'Samsung refrigerator', 'LG refrigerator', 'under counter refrigerator', 'GE refrigerator', 'Alaffia, vegan and cruelty-free body soap', 'Samsung stainless steel gas stove', '54\\', 'Dial Soap Bars body soap', 'Bed sheets and pillows', 'Dedicated workspace: desk, office chair, and table', 'Eco bar soap body soap', 'Sound system with Bluetooth and aux', 'Alaffia, vegan and cruelty-free shampoo', '60\\', 'Dedicated workspace: monitor, desk, and office chair', 'Kayak', 'Kirkland shampoo', 'Game console: PS2', 'Alaffia, vegan and cruelty-free conditioner', 'KitchenAid stainless steel oven', 'HDTV with Amazon Prime Video, HBO Max, Netflix, Roku', 'Clothing storage: wardrobe and closet', 'mini fridge refrigerator', 'Free washer', 'Dedicated workspace: table, desk, and office chair', '48\\', 'TRESemm\\u00e9 shampoo', 'Maxxam conditioner', 'Kirkland conditioner', 'Fast wifi \\u2013 97 Mbps', 'Various body soap', 'Clothing storage: closet and wardrobe', 'Beekman conditioner', 'Whole Foods body soap', 'Shared outdoor heated saltwater pool', 'Dove conditioner', 'KitchenAid stainless steel gas stove', 'HDTV with Amazon Prime Video, Apple TV, HBO Max, Netflix, Roku', 'HDTV with Netflix', 'TRESemm\\u00e9 conditioner', 'Gas oven', 'Fast wifi \\u2013 96 Mbps', 'Toiletries', '24-hour fitness center', 'Children\\u2019s books and toys for ages 0-2 years old, 2-5 years old, 5-10 years old, and 10+ years old', 'TV with Roku, standard cable', 'Free parking on premises \\u2013 1 space', 'TV with Amazon Prime Video, Chromecast, Netflix', 'Fast wifi \\u2013 121 Mbps', 'Fast wifi \\u2013 302 Mbps', 'TV with Amazon Prime Video', 'TV with Amazon Prime Video, Roku, Netflix', 'Bose sound system with Bluetooth and aux', 'HDTV with HBO Max, Netflix, Roku, premium cable, Amazon Prime Video', 'Self-parking \\u2014 $42/stay', 'Avanti stainless steel oven', 'Clothing storage: wardrobe, walk-in closet, closet, and dresser', 'dove  conditioner', 'Organic  body soap', 'HDTV with premium cable, standard cable', 'Fast wifi \\u2013 100 Mbps', 'LG New as of 3/21 stainless steel oven', 'Amana refrigerator', 'Loreal conditioner', 'TV with Apple TV, Roku', 'Fast wifi \\u2013 93 Mbps', 'Private outdoor lap pool', 'There are two induction burners with pots and pans. induction stove', 'google assistant sound system', 'whirlpool  oven', 'Dedicated workspace: office chair, desk, monitor, and table', 'Clothing storage: dresser, walk-in closet, wardrobe, and closet', 'Limited housekeeping \\u2014 ', 'dove body soap', ' linens', 'DOVE Usually body soap', 'Clothing storage: wardrobe, closet, and dresser', 'Fast wifi \\u2013 157 Mbps', 'Panasonic sound system', 'Wine Mini Fridge (For Beverages Only) refrigerator', 'Toshiba with Boss Speakers sound system with Bluetooth and aux', 'Audio-Technica Record Player  sound system with Bluetooth and aux', 'Kirkland body soap', 'Teenage Engineering Bluetooth sound system', ' Bath & Body Works shampoo', 'Limited housekeeping \\u2014 on request', 'Gaggenau stainless steel gas stove', 'TV with HBO Max, Netflix, Roku, standard cable', 'Paid parking lot on premises \\u2013 3 spaces', '37\\', 'Kitchenaid refrigerator', 'Polk Bluetooth sound system', 'KitchenAid refrigerator', 'Game console: PS4', 'Paid valet parking on premises', 'Cambridge Soundworks / Doss (two small units) sound system with Bluetooth and aux', 'Slippers', 'Samsung  stainless steel oven', 'Samsung  stainless steel gas stove', 'Dove shampoo', 'Fast wifi \\u2013 102 Mbps', 'No stove but has a hot plate electric stove', 'Small fridge in room. Larger fridge in kitchenette  refrigerator', 'Paid parking garage on premises \\u2013 1 space', 'WHRILPOOL refrigerator', 'HDTV with Amazon Prime Video, standard cable', '57\\', '36\\', 'Dedicated workspace: monitor, table, desk, and office chair', 'Both bar soaps and body wash are available for you. body soap', 'Dedicated workspace: monitor', 'Avanti stainless steel electric stove', 'Indoor pool', 'Sonos sound system with Bluetooth and aux', 'Kitchenaid stainless steel oven', 'HDTV with standard cable, Roku', 'Dedicated workspace: monitor, table, office chair, and desk', '45\\', 'Shared gym nearby', 'Kenmore oven', 'Fast wifi \\u2013 68 Mbps', 'Bluetooth speaker Bluetooth sound system', 'Gilchrist And Saomes body soap', 'GE oven', 'GE Profile refrigerator', '46\\', 'Fast wifi \\u2013 51 Mbps', 'HDTV with Netflix, HBO Max, Chromecast, standard cable', 'Fast wifi \\u2013 63 Mbps', '21\\', 'HDTV with Amazon Prime Video, HBO Max, Netflix, premium cable, Roku, standard cable, Chromecast', 'Your choice 100% Organic or Skin Sensitive no scent - MILK Brand body soap', 'HDTV with Netflix, HBO Max, Amazon Prime Video', 'House bikes', 'Samsung  gas stove', 'Fast wifi \\u2013 276 Mbps', 'minifridge refrigerator', 'Fast wifi \\u2013 95 Mbps', 'Game console: Nintendo Wii', 'Connect your device via Bluetooth sound system', 'Onsite restaurant \\u2014 canteenM-open 24/7 Open 24/7,  canteenM is our casual and cosy kitchen, offering a choice of homemade meals, healthy snacks, and goodies for sharing. Our baristas will make you a perfect coffee all day (and night) long, and in the evenings they transform into expert mixologists!', 'Pets allowed', 'Ivory body soap', 'Fast wifi \\u2013 220 Mbps', 'Children\\u2019s books and toys for ages 2-5 years old, 5-10 years old, and 10+ years old', 'Clothing storage: walk-in closet and dresser', 'HDTV with Netflix, HBO Max, Amazon Prime Video, standard cable', 'Sono sound system', 'TV with HBO Max, Netflix, Roku, Amazon Prime Video, standard cable', 'Suave body soap', 'Boat slip', 'SONOS Bluetooth sound system', 'Pantene  conditioner', 'Freshscent shampoo', 'Clothing storage: closet, wardrobe, walk-in closet, and dresser', 'Tresemme  conditioner', 'Free residential garage on premises \\u2013 1 space', 'Sonos  sound system', ' HDTV with Amazon Prime Video, Chromecast, Netflix', 'KEF sound system with Bluetooth and aux', 'Gel body soap', 'Central AC  conditioner', 'Radio and CD player sound system', 'Concierge', 'Game room', 'TV with Amazon Prime Video, Netflix, standard cable', 'Samsung french door refrigerator', 'HDTV with Amazon Prime Video, Netflix', 'Ikea gas stove', 'Fast wifi \\u2013 58 Mbps', 'Paid parking lot on premises \\u2013 6 spaces', 'HDTV with Netflix, Roku', 'Tresemme shampoo', 'Infuse - Made from white tea and coconut conditioner', 'Nexus or Kirkland shampoo', 'SoapBox Tea Tree Clean & Purify shampoo', 'Fast wifi \\u2013 59 Mbps', 'Infuse made from white tea and coconut body soap', ':) conditioner', 'Dedicated workspace: office chair, desk, and monitor', 'Gilchrist and Soames body soap', 'Kenmore stainless steel electric stove', 'Kiehl\'s body soap', 'Fast wifi \\u2013 103 Mbps', ' toiletries', 'Gel shampoo', 'Infuse- made from white tea And coconut shampoo', 'Bosch stainless steel oven', 'Neutrogena or Kirkland body soap', 'Whirlpool refrigerator', 'Beekman body soap', 'HDTV with Amazon Prime Video, HBO Max, Netflix, premium cable, standard cable, Chromecast, Roku', 'Fast wifi \\u2013 191 Mbps', 'Fast wifi \\u2013 445 Mbps', 'TV with Netflix, Amazon Prime Video', 'Fast wifi \\u2013 409 Mbps', 'Various conditioner', 'Free carport on premises \\u2013 1 space', 'MIlk, Organic 365% and EVERYBODY shampoo', 'Sonos sound system', 'Whirlpool stainless steel oven', 'Fast wifi \\u2013 98 Mbps', 'HDTV with Netflix, HBO Max, Amazon Prime Video, premium cable', 'Shared refrigerator', 'Organic shampoo', 'Sonos wifi sound system', 'Children\\u2019s books and toys for ages 2-5 years old and 5-10 years old', 'Aveeno body soap', 'bose sound system with Bluetooth and aux', 'Children\\u2019s books and toys for ages 5-10 years old and 10+ years old', 'Freshscent body soap', 'Ikea oven', 'Gilchrist and Somes body soap', 'Private sauna', 'HDTV with Apple TV, standard cable', 'Free residential garage on premises', 'Beekman Hotel conditioner', 'something nice! :) body soap', 'Oster Toaster Oven oven', 'HDTV with Amazon Prime Video', 'Honest body soap', 'Organic conditioner', 'Breakfast buffet available \\u2014 $19 per person per day', 'There is a 24\\', 'Bluetooth speaker', 'Sonos Bluetooth sound system', 'Kiehl\'s conditioner', 'Housekeeping', ':) body soap', 'Fast wifi \\u2013 78 Mbps', 'Children\\u2019s books and toys for ages 2-5 years old', 'Kitchenaid stainless steel gas stove', 'HDTV with Netflix, standard cable', 'Paid parking lot on premises \\u2013 4 spaces', 'Dedicated workspace: office chair and table', 'WHIRPOOL refrigerator', 'hypoallergenic body soap', 'Laundry services', 'Onsite restaurant \\u2014 Cosmica', 'HDTV with premium cable, Roku, standard cable', 'Dedicated workspace: desk and table', 'Samsung oven', 'Fast wifi \\u2013 395 Mbps', 'trader joes conditioner', 'Softsoap body soap', 'Dedicated workspace: table and office chair', '70\\', 'Irish Spring Shower gel/Dial liquid hand soap/Tulip body soap body soap', 'SoapBox Sea Minerals & Blue Iris body soap', 'HDTV with Netflix, Roku, premium cable, HBO Max, Amazon Prime Video', 'Rikoko conditioner', 'Purchased in 2020. refrigerator', 'HDTV with Chromecast, Amazon Prime Video, HBO Max, Netflix, standard cable', 'Generic conditioner', 'Fast wifi \\u2013 55 Mbps', 'GE 20.2 CU FT refrigerator', 'Olay body soap']
# chosen_amenities = ['Lock on bedroom door', 'Private entrance',
#     'Pack \u2019n play/Travel crib', 'Elevator', 'Iron', 'Hair dryer', 'Microwave',
#     'Free street parking',  'Cable TV', 'Ethernet connection']
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
    tmp[get_id("is_bath_shared")] = ("shared" in bathroom_type)
    X = pd.DataFrame([tmp], columns=all_features)
    price = svr_model.predict(X)
    # range_id = svc_model.predict(X)
    range_id = -1
    improve_amenity = "None"
    improve_price = float(price[0])
    X_list = []
    for x in chosen_amenities:
        cur_id = get_id(x)
        if tmp[cur_id] != 1:
            tmp[cur_id] = 1
            X_list.append(tmp.copy())
            tmp[cur_id] = 0
    
    X = pd.DataFrame(X_list, columns=all_features)
    y_pred = svr_model.predict(X)
    max_id = y_pred.argmax()
    improve_amenity = all_features[max_id]
    improve_price = float(y_pred[max_id])

    # model_amenities = svr_model.feature_names_in_
    # model_amenities = "\', \'".join(model_amenities)
    # model_amenities = re.sub(r"\\", r"\\\\", model_amenities)
    # print(model_amenities)

    if range_id == 0:
        range_text = "Less than $100"
    elif range_id == 1:
        range_text = "$100 - $200"
    elif range_id == 2:
        range_text = "$200 - $300"
    elif range_id == 3:
        range_text = "More than $300"
    else:
        range_text = "Out of Service"
    return {"message": "Success!", 
        "price": math.exp(price[0]), 
        "range": range_text, 
        "improve_amenity": improve_amenity,
        "improve_price": math.exp(improve_price),
    }
    
if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
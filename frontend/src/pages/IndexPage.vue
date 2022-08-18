<template>
  <div class="background">
    <div>
      <h3 align="center">AirBnB Listing Price Estimator</h3>
      <h5 align="end">-- Based on Boston Data</h5>
    </div>
    <div class="library-content">
      <q-form @submit="handleInput">
        <div>
          <label class="input-label-text">Accommodates</label>
          <q-input
            filled
            type="number"
            v-model="accommodates"
          />
        </div>
        <div>
          <label class="input-label-text">Bedrooms</label>
          <q-input
            filled
            type="number"
            v-model="bedrooms"
          />
        </div>
        <div>
          <label class="input-label-text">Beds</label>
          <q-input
            filled
            type="number"
            v-model="beds"
          />
        </div>
        <div>
          <label class="input-label-text">Neighbourhood</label>
          <q-select
            fill-input
            outlined
            :options="neighbourhood_options"
            v-model="neighbourhood"
          />
        </div>
        <div>
          <label class="input-label-text">Bathroom Type</label>
          <q-select
            fill-input
            outlined
            :options="bathroom_options"
            v-model="bathroom_type"
          />
        </div>
        <div>
          <label class="input-label-text">Property Type</label>
          <q-select
            fill-input
            outlined
            :options="property_options"
            v-model="property_type"
          />
        </div>
        <div>
          <label class="input-label-text">Room Type</label>
          <q-select
            fill-input
            outlined
            :options="room_options"
            v-model="room_type"
          />
        </div>
        <div>
          <label class="input-label-text">Amenities</label>
          <q-select
            fill-input
            multiple
            outlined
            :options="amenity_options"
            v-model="amenities"
          />
        </div>
        <div class="predict-btn-position">
          <q-btn
            label="Predict"
            type="submit"
            outline
            class="outlined-button text-body1 text-weight-bolder"
          ></q-btn>
        </div>
      </q-form>
    </div>
    <div class="upload-content">
      <div class="row">
        <div class="col-6" align="center">
          <p class="input-label-text">Price: ${{Math.round(predicted_price*100) / 100}}</p><br />
          <p>Median Absolute Error: $26</p>
        </div>
        <div class="col-6" align="center">
          <p class="input-label-text">Range: {{predicted_range}}</p><br />
          <p>Accuracy: 72%</p>
        </div>
      </div>
      <div align="center">
        <p class="input-label-text">Adding {{improve_amenity}} would increase price to ${{Math.round(improve_price*100) / 100}}</p><br />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
/* eslint-disable @typescript-eslint/no-explicit-any */
import { ref, defineComponent } from 'vue';
import axios from 'axios';
export default defineComponent({
  name: 'IndexPage',
  setup() {
    const accommodates = ref(0);
    const bedrooms = ref(0);
    const beds = ref(0);
    const bathroom_type = ref('');
    const property_type = ref('');
    const room_type = ref('');
    const neighbourhood = ref('');
    const amenities = ref([]);
    const predicted_price = ref(0);
    const predicted_range = ref('');
    const improve_amenity = ref('');
    const improve_price = ref(0);
    return {
      accommodates,
      bedrooms,
      beds,
      bathroom_type,
      property_type,
      room_type,
      neighbourhood,
      amenities,
      predicted_price,
      predicted_range,
      improve_amenity,
      improve_price,
    }
  },
  components: {},
  data(){
    return {
      neighbourhood_options: ['Allston', 'Back Bay', 'Bay Village',
       'Beacon Hill', 'Brighton', 'Charlestown', 'Chinatown', 'Dorchester',
       'Downtown', 'East Boston', 'Fenway', 'Hyde Park', 'Jamaica Plain',
       'Leather District', 'Longwood Medical Area', 'Mattapan', 'Mission Hill',
       'North End', 'Roslindale', 'Roxbury', 'South Boston',
       'South Boston Waterfront', 'South End', 'West End', 'West Roxbury'],
      bathroom_options: ['1 bath', '1 private bath', '1 shared bath', '1.5 baths',
       '1.5 shared baths', '2 baths', '2 shared baths', '2.5 baths',
       '2.5 shared baths', '3 baths', '3 shared baths', '3.5 baths',
       '3.5 shared baths', '4.5 baths', '5 baths', '5 shared baths',
       '6 shared baths', 'Half-bath'],
      property_options: ['Boat', 'Entire condominium (condo)', 'Entire guest suite',
       'Entire guesthouse', 'Entire loft', 'Entire rental unit',
       'Entire residential home', 'Entire serviced apartment',
       'Entire townhouse', 'Houseboat', 'Private room in bed and breakfast',
       'Private room in bungalow', 'Private room in condominium (condo)',
       'Private room in guest suite', 'Private room in loft',
       'Private room in rental unit', 'Private room in residential home',
       'Private room in townhouse', 'Private room in villa',
       'Room in bed and breakfast', 'Room in boutique hotel', 'Room in hotel',
       'Shared room in condominium (condo)', 'Shared room in residential home',
       'Shared room in townhouse'],
      room_options: ['Entire home/apt', 'Hotel room', 'Private room', 'Shared room'],
    //   amenity_options: ['Lock on bedroom door', 'Private entrance',
    //     'Pack \u2019n play/Travel crib', 'Elevator', 'Iron', 'Hair dryer', 'Microwave',
    //     'Free street parking',  'Cable TV', 'Ethernet connection']
      amenity_options: ['Wifi', 'Smoke alarm', 'Long term stays allowed', 'Carbon monoxide alarm', 'Kitchen', 'Essentials', 'Heating', 'Hangers', 'Hair dryer', 'Air conditioning', 'Iron', 'Shampoo', 'Hot water', 'Refrigerator', 'Microwave', 'Dedicated workspace', 'Washer', 'Coffee maker', 'Dryer', 'Dishes and silverware', 'Cooking basics', 'Bed linens', 'Oven', 'TV', 'Fire extinguisher', 'Stove', 'Dishwasher', 'Extra pillows and blankets', 'First aid kit', 'Private entrance', 'Free street parking', 'Cable TV', 'Luggage dropoff allowed', 'TV with standard cable', 'Security cameras on property', 'Keypad', 'Lock on bedroom door', 'Lockbox', 'Elevator', 'Bathtub', 'Free parking on premises', 'Shower gel', 'Freezer', 'Baking sheet', 'Gym', 'Toaster', 'Patio or balcony', 'Hot water kettle', 'Dining table', 'Body soap', 'Backyard', 'Cleaning products', 'Laundromat nearby', 'Paid parking off premises', 'Wine glasses', 'BBQ grill', 'Pack \\u2019n play/Travel crib', 'Conditioner', 'Room-darkening shades', 'Indoor fireplace', 'Smart lock', 'Pool', 'Ethernet connection', 'Breakfast', 'Paid parking on premises', 'Trash compactor', 'Outdoor furniture', 'Host greets you', 'Portable fans', 'Clothing storage: closet', 'Pocket wifi', 'Keurig coffee machine', 'Central heating', 'Crib', 'Clothing storage', 'Children\\u2019s books and toys', 'High chair', 'Mini fridge', 'Ceiling fan', 'Private patio or balcony', 'Shared patio or balcony', 'Outdoor dining area', 'Single level home', 'Cleaning before checkout', 'Barbecue utensils', 'Window AC unit', 'Building staff', ', ', 'Paid parking garage off premises', 'Dryer \\u2013\\u00a0In unit', 'Stainless steel oven', 'Washer \\u2013\\u00a0In unit', 'Paid washer \\u2013 In building', 'TV with Chromecast', 'Window guards', 'Dryer \\u2013 In building', 'Washer \\u2013\\u00a0In building', 'Central air conditioning', 'Drying rack for clothing', 'Children\\u2019s dinnerware', 'EV charger', 'Board games', 'Paid dryer \\u2013 In building', 'Hot tub', 'Babysitter recommendations', 'Waterfront', 'Beach essentials', 'Fireplace guards', 'Free dryer \\u2013 In unit', 'Outlet covers', 'Baby safety gates', 'Clothing storage: dresser and closet', 'Safe', 'Radiant heating', 'Rice maker', 'Clothing storage: closet and dresser', 'Beachfront', 'Fire pit', 'Baby bath', 'Free washer \\u2013 In unit', 'Private garden or backyard', 'Private fenced garden or backyard', 'Shared garden or backyard', 'Shared fenced garden or backyard', 'Stainless steel gas stove', 'Changing table', 'Electric stove', 'Dedicated workspace: table', 'Pour-over coffee', 'Bath & Body Works conditioner', 'Paid parking lot off premises', 'Baby monitor', '32\\', 'Sound system', 'Paid parking lot on premises \\u2013 1 space', 'Bath & Body Works shampoo', 'Free washer \\u2013 In building', 'Paid parking garage on premises', 'Game console', 'Nespresso machine', 'Bath & Body Works body soap', 'Lake access', 'Free dryer \\u2013 In building', 'Clothing storage: wardrobe', 'Bread maker', 'Dedicated workspace: desk and office chair', 'Bidet', 'Gas stove', 'Mosquito net', 'Free driveway parking on premises \\u2013 1 space', '55\\', 'Clothing storage: dresser', 'Pool table', 'Stainless steel stove', 'HDTV with Roku', 'Stainless steel electric stove', 'Paid street parking off premises', '65\\', '50\\', 'Shared pool', 'Piano', 'Dove body soap', 'Paid dryer', 'TV with Roku', 'HDTV', 'Paid parking lot on premises', 'Paid washer', 'Dedicated workspace: desk', 'Clothing storage: walk-in closet', 'Free driveway parking on premises', 'Bikes', 'HDTV with standard cable', '40\\', 'Portable heater', 'Dedicated workspace: office chair and desk', 'Ping pong table', 'Google Home Bluetooth sound system', 'Record player', 'Children\\u2019s books and toys for ages 0-2 years old and 2-5 years old', 'Pantene conditioner', 'Shared gym in building', 'Private hot tub', 'Free driveway parking on premises \\u2013 2 spaces', 'Shared outdoor pool', 'Clothing storage: wardrobe and dresser', 'Fast wifi \\u2013 54 Mbps', '42\\', 'Bluetooth sound system', 'Portable air conditioning', 'Clothing storage: walk-in closet and closet', 'Shared hot tub', 'Induction stove', 'TV with Amazon Prime Video, HBO Max, Netflix, Roku, standard cable', 'Free dryer', 'HDTV with Amazon Prime Video, HBO Max, Netflix, standard cable', '52\\', 'Pantene shampoo', '43\\', 'Dedicated workspace: desk, table, and office chair', 'Clothing storage: closet, dresser, and walk-in closet', 'Private pool', 'Paid dryer \\u2013 In unit', 'Free wifi', 'Clothing storage: dresser, walk-in closet, and closet', 'Paid washer \\u2013 In unit', 'Clothing storage: closet and walk-in closet', 'Beekman shampoo', 'Not sure  body soap', '75\\', 'Bosch refrigerator', 'Samsung stainless steel oven', 'Clothing storage: dresser and wardrobe', 'Paid parking lot on premises \\u2013 2 spaces', 'Outdoor shower', 'Private gym in building', 'Dedicated workspace: office chair, table, and desk', 'LG refrigerator', 'Clothing storage: walk-in closet, dresser, and closet', 'Samsung refrigerator', 'Table corner guards', 'Kirkland shampoo', 'Children\\u2019s books and toys for ages 0-2 years old, 2-5 years old, 5-10 years old, and 10+ years old', 'Dial Soap Bars body soap', '54\\', '60\\', 'Samsung stainless steel gas stove', 'TRESemm\\u00e9 shampoo', 'HDTV with Amazon Prime Video, HBO Max, Netflix, Roku', '48\\', 'Alaffia, vegan and cruelty-free shampoo', 'Free parking on premises \\u2013 1 space', 'Alaffia, vegan and cruelty-free conditioner', 'Shared outdoor heated saltwater pool', 'Gas oven', 'mini fridge refrigerator', 'GE refrigerator', 'TV with Roku, standard cable', 'Dedicated workspace: table, desk, and office chair', 'Game console: PS2', 'HDTV with Amazon Prime Video, Apple TV, HBO Max, Netflix, Roku', 'KitchenAid stainless steel oven', 'Clothing storage: closet and wardrobe', 'Kayak', 'Eco bar soap body soap', 'KitchenAid stainless steel gas stove', '24-hour fitness center', 'Sound system with Bluetooth and aux', 'Whole Foods body soap', 'Free washer', 'Fast wifi \\u2013 96 Mbps', 'Maxxam conditioner', 'Various body soap', 'Dove conditioner', 'Fast wifi \\u2013 97 Mbps', 'Toiletries', 'Dedicated workspace: desk, office chair, and table', 'Beekman conditioner', 'Alaffia, vegan and cruelty-free body soap', 'Kirkland conditioner', 'under counter refrigerator', 'TRESemm\\u00e9 conditioner', 'Bed sheets and pillows', 'Clothing storage: wardrobe and closet', 'Dedicated workspace: monitor, desk, and office chair', 'HDTV with Netflix', '45\\', 'Bosch stainless steel oven', 'Fast wifi \\u2013 98 Mbps', 'Gel shampoo', 'WHIRPOOL refrigerator', 'Radio and CD player sound system', 'HDTV with premium cable, Roku, standard cable', 'DOVE Usually body soap', 'Central AC  conditioner', 'HDTV with Amazon Prime Video, Netflix', 'Polk Bluetooth sound system', 'Paid valet parking on premises', 'House bikes', 'MIlk, Organic 365% and EVERYBODY shampoo', 'Tresemme shampoo', 'HDTV with Netflix, standard cable', 'Kenmore oven', 'GE Profile refrigerator', 'Bluetooth speaker', 'WHRILPOOL refrigerator', 'Samsung oven', 'Whirlpool refrigerator', 'Cambridge Soundworks / Doss (two small units) sound system with Bluetooth and aux', 'Kenmore stainless steel electric stove', 'Fast wifi \\u2013 58 Mbps', 'Paid parking lot on premises \\u2013 3 spaces', 'google assistant sound system', 'Fast wifi \\u2013 102 Mbps', 'bose sound system with Bluetooth and aux', '70\\', 'HDTV with Amazon Prime Video, HBO Max, Netflix, premium cable, Roku, standard cable, Chromecast', 'KEF sound system with Bluetooth and aux', 'SoapBox Tea Tree Clean & Purify shampoo', 'HDTV with premium cable, standard cable', 'Ivory body soap', 'Samsung  gas stove', ' toiletries', 'Kitchenaid stainless steel oven', 'Dedicated workspace: table and office chair', 'Purchased in 2020. refrigerator', 'KitchenAid refrigerator', ':) body soap', 'Both bar soaps and body wash are available for you. body soap', 'Fast wifi \\u2013 63 Mbps', 'Dedicated workspace: monitor', 'Your choice 100% Organic or Skin Sensitive no scent - MILK Brand body soap', 'HDTV with HBO Max, Netflix, Roku, premium cable, Amazon Prime Video', 'Dedicated workspace: desk and table', 'HDTV with Netflix, Roku, premium cable, HBO Max, Amazon Prime Video', 'Loreal conditioner', 'TV with Netflix, Amazon Prime Video', 'Connect your device via Bluetooth sound system', 'Children\\u2019s books and toys for ages 2-5 years old, 5-10 years old, and 10+ years old', '57\\', 'Free residential garage on premises \\u2013 1 space', 'Ikea oven', 'Sonos Bluetooth sound system', 'Private sauna', 'Onsite restaurant \\u2014 canteenM-open 24/7 Open 24/7,  canteenM is our casual and cosy kitchen, offering a choice of homemade meals, healthy snacks, and goodies for sharing. Our baristas will make you a perfect coffee all day (and night) long, and in the evenings they transform into expert mixologists!', 'Bluetooth speaker Bluetooth sound system', 'Organic  body soap', 'HDTV with Chromecast, Amazon Prime Video, HBO Max, Netflix, standard cable', 'There are two induction burners with pots and pans. induction stove', 'Boat slip', 'Game room', 'GE oven', 'Dove shampoo', 'Sonos wifi sound system', 'Fast wifi \\u2013 220 Mbps', 'Oster Toaster Oven oven', 'Amana refrigerator', 'Avanti stainless steel oven', 'Wine Mini Fridge (For Beverages Only) refrigerator', 'Aveeno body soap', 'Clothing storage: dresser, walk-in closet, wardrobe, and closet', 'Onsite restaurant \\u2014 Cosmica', "Kiehl's body soap", 'Private outdoor lap pool', 'Teenage Engineering Bluetooth sound system', 'Gel body soap', 'Sonos sound system', 'whirlpool  oven', ' HDTV with Amazon Prime Video, Chromecast, Netflix', 'Slippers', 'Breakfast buffet available \\u2014 $19 per person per day', 'Free carport on premises \\u2013 1 space', 'Game console: Nintendo Wii', 'Panasonic sound system', 'HDTV with Netflix, Roku', 'something nice! :) body soap', 'Clothing storage: closet, wardrobe, walk-in closet, and dresser', 'Honest body soap', 'Fast wifi \\u2013 93 Mbps', 'Shared refrigerator', 'Fast wifi \\u2013 55 Mbps', 'HDTV with Netflix, HBO Max, Chromecast, standard cable', 'HDTV with Netflix, HBO Max, Amazon Prime Video', 'HDTV with Netflix, HBO Max, Amazon Prime Video, standard cable', 'Dedicated workspace: office chair, desk, and monitor', 'Children\\u2019s books and toys for ages 5-10 years old and 10+ years old', 'Samsung  stainless steel oven', 'Fast wifi \\u2013 409 Mbps', 'Fast wifi \\u2013 95 Mbps', 'Various conditioner', 'Children\\u2019s books and toys for ages 2-5 years old and 5-10 years old', 'Clothing storage: walk-in closet and dresser', 'Samsung  stainless steel gas stove', 'Dedicated workspace: monitor, table, office chair, and desk', 'Avanti stainless steel electric stove', 'Neutrogena or Kirkland body soap', 'HDTV with Netflix, HBO Max, Amazon Prime Video, premium cable', 'Sonos  sound system', 'Pets allowed', 'Dedicated workspace: office chair, desk, monitor, and table', 'Fast wifi \\u2013 68 Mbps', "Kiehl's conditioner", 'Fast wifi \\u2013 157 Mbps', 'Paid parking lot on premises \\u2013 4 spaces', 'TV with Apple TV, Roku', 'Fast wifi \\u2013 100 Mbps', 'TV with Amazon Prime Video, Netflix, standard cable', 'Small fridge in room. Larger fridge in kitchenette  refrigerator', 'Concierge', 'Shared gym nearby', 'Limited housekeeping \\u2014 on request', 'dove  conditioner', 'Game console: PS4', 'Fast wifi \\u2013 191 Mbps', 'Fast wifi \\u2013 121 Mbps', 'Olay body soap', 'Free residential garage on premises', 'Dedicated workspace: monitor, table, desk, and office chair', 'Nexus or Kirkland shampoo', ' linens', 'Infuse- made from white tea And coconut shampoo', 'Audio-Technica Record Player  sound system with Bluetooth and aux', 'TV with Amazon Prime Video', '36\\', 'Kirkland body soap', 'HDTV with Apple TV, standard cable', 'Ikea gas stove', 'Dedicated workspace: office chair and table', 'Irish Spring Shower gel/Dial liquid hand soap/Tulip body soap body soap', 'Freshscent body soap', 'trader joes conditioner', 'Beekman Hotel conditioner', 'Fast wifi \\u2013 445 Mbps', 'No stove but has a hot plate electric stove', 'Freshscent shampoo', 'TV with HBO Max, Netflix, Roku, Amazon Prime Video, standard cable', 'Organic shampoo', 'Generic conditioner', 'Beekman body soap', 'SoapBox Sea Minerals & Blue Iris body soap', '37\\', 'HDTV with Amazon Prime Video, standard cable', 'Organic conditioner', 'Toshiba with Boss Speakers sound system with Bluetooth and aux', 'Clothing storage: wardrobe, closet, and dresser', 'There is a 24\\', 'Suave body soap', 'Tresemme  conditioner', 'Gilchrist and Soames body soap', 'Children\\u2019s books and toys for ages 2-5 years old', 'Self-parking \\u2014 $42/stay', 'HDTV with Amazon Prime Video', 'Clothing storage: wardrobe, walk-in closet, closet, and dresser', 'Laundry services', 'Sonos sound system with Bluetooth and aux', 'Fast wifi \\u2013 51 Mbps', 'Housekeeping', 'Limited housekeeping \\u2014 ', 'Fast wifi \\u2013 78 Mbps', 'dove body soap', 'Rikoko conditioner', 'Kitchenaid refrigerator', ' Bath & Body Works shampoo', 'TV with Amazon Prime Video, Roku, Netflix', 'Sono sound system', 'minifridge refrigerator', 'Fast wifi \\u2013 395 Mbps', 'Infuse made from white tea and coconut body soap', 'GE 20.2 CU FT refrigerator', 'Fast wifi \\u2013 302 Mbps', 'LG New as of 3/21 stainless steel oven', '46\\', 'HDTV with Amazon Prime Video, HBO Max, Netflix, premium cable, standard cable, Chromecast, Roku', '21\\', 'Fast wifi \\u2013 103 Mbps', 'Infuse - Made from white tea and coconut conditioner', 'Fast wifi \\u2013 59 Mbps', 'Samsung french door refrigerator', 'TV with Amazon Prime Video, Chromecast, Netflix', 'TV with HBO Max, Netflix, Roku, standard cable', 'HDTV with standard cable, Roku', 'Kitchenaid stainless steel gas stove', 'hypoallergenic body soap', 'Indoor pool', 'Bose sound system with Bluetooth and aux', 'SONOS Bluetooth sound system', 'Whirlpool stainless steel oven', 'Gilchrist and Somes body soap', 'Fast wifi \\u2013 276 Mbps', 'Pantene  conditioner', 'Gilchrist And Saomes body soap', 'Paid parking lot on premises \\u2013 6 spaces', 'Paid parking garage on premises \\u2013 1 space', 'Softsoap body soap', 'Gaggenau stainless steel gas stove', ':) conditioner'],
    }
  },
  mounted() {
    this.amenity_options.sort();
  },
  methods: {
    handleInput(){
      const api = axios.create({ baseURL: 'http://localhost:8000' });
      api
      .post('/predictPrice/', {
        accommodates: this.accommodates,
        bedrooms: this.bedrooms,
        beds: this.beds,
        neighbourhood: this.neighbourhood,
        bathroom_type: this.bathroom_type,
        property_type: this.property_type,
        room_type: this.room_type,
        amenities: this.amenities
      })
      .then((resp: any) => {
        this.predicted_price = resp.data.price
        this.predicted_range = resp.data.range
        this.improve_price = resp.data.improve_price
        this.improve_amenity = resp.data.improve_amenity
      })
      .catch((err: any) => {
        console.log(err);
      });
    }
  }
});
</script>
<style lang="scss" scoped>
.background {
  padding: 10%;
  height: 100%;
}
.upload-content {
  align-items: center;
  justify-content: center;
  padding: 5%;
}
.image-icon{
  margin-right: 10%;
  margin-left: 10%;
}
.pick-button{
  height: 40px;
  margin-top: 15px;
  margin-bottom: 10px;
}
.upload-btn-position {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  margin-top: 5%;
}
.input-label-text {
  font-size: 25px;
}
.predict-btn-position {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  margin-top: 5%;
}
</style>
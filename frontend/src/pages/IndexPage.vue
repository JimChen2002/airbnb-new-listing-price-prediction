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
    </div>
  </div>
</template>

<script lang="ts">
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
      amenity_options: ['Lock on bedroom door', 'Private entrance',
        'Pack \u2019n play/Travel crib', 'Elevator', 'Iron', 'Hair dryer', 'Microwave',
        'Free street parking',  'Cable TV', 'Ethernet connection']
    }
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
<template>
  <div>
    <h1>Driver</h1>
    <Map v-on:set-startpoint="startPoint = $event" v-on:set-destination="destination = $event" />
    <v-btn>Submit</v-btn>
    <v-btn @click.native="$emit('cancel')">Cancel</v-btn>
  </div>
</template>
<script>
import Map from "./Map";

export default {
  components: {
    Map
  },
  data() {
    return {
      startPoint: null,
      destination: null,
      center: { lat: 20, lng: 20 }
      //
    };
  },
  methods: {
    setStartpoint(place) {
      this.startPoint = {
        lat: place.geometry.location.lat(),
        lng: place.geometry.location.lng()
      };
      this.center = this.startPoint;
    },
    setDestination(place) {
      this.destination = {
        lat: place.geometry.location.lat(),
        lng: place.geometry.location.lng()
      };
    }
  }
};
</script>
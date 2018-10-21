<template>
  <v-flex xs12>
    <h1>Passenger</h1>
    <Map v-on:set-start-point="startPoint = $event" v-on:set-destination="destination = $event" />
    <v-btn @click.native="submit">Submit</v-btn>
    <v-btn @click.native="$emit('cancel')">Cancel</v-btn>
  </v-flex>
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
      error_text: null
    };
  },
  methods: {
    setStartpoint(place) {
      this.startPoint = {
        latitude: place.geometry.location.lat.toFixed(6),
        longitude: place.geometry.location.lng.toFixed(6)
      };
      this.center = this.startPoint;
    },
    setDestination(place) {
      this.destination = {
        latitude: place.geometry.location.lat.toFixed(6),
        longitude: place.geometry.location.lng.toFixed(6)
      };
    },
    submit() {
      if (this.startPoint != null && this.destination != null) {
        this.$emit("submit", {
          startPoint: this.startPoint,
          destination: this.destination
        });
      } else {
        this.error_text = "Please set start point and destionation to proceed";
      }
    }
  }
};
</script>
<template>
  <v-flex xs12>
    <v-alert :value="error_text != null" type="error">
      {{error_text}}
    </v-alert>
    <Map label="Drivers route:" v-on:set-start-point="setStartpoint($event)" v-on:set-destination="setDestination($event)" @submit="submit" @cancel="$emit('cancel')" />
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
      //
    };
  },
  methods: {
    setStartpoint(place) {
      this.startPoint = {
        latitude: place.lat.toFixed(6),
        longitude: place.lng.toFixed(6)
      };
      this.center = this.startPoint;
    },
    setDestination(place) {
      this.destination = {
        latitude: place.lat.toFixed(6),
        longitude: place.lng.toFixed(6)
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
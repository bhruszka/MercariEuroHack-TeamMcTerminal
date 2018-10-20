<template>
    <div>
        <h1>Driver</h1>
        <Map />
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
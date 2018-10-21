<template>
  <div>
    <div style="width: 100%; position: relative">
      <div class="map-input-container">
        <h1 class="visible">{{label}}</h1>
        <gmap-autocomplete @place_changed="setStartpoint" class="location-input input-startpoint" placeholder="Enter start point">
        </gmap-autocomplete>
        <gmap-autocomplete @place_changed="setDestination" class="location-input input-destination" placeholder="Enter destination">
        </gmap-autocomplete>
        <v-btn @click.native="$emit('submit')" class="button-map button-map-first">Submit</v-btn>
        <v-btn @click.native="$emit('cancel')" class="button-map">Cancel</v-btn>
      </div>
      <GmapMap :center="center" :zoom="7" class="my-map" :options="options">
        <GmapMarker v-if="startPoint" :position="startPoint" :clickable="true" />
        <GmapMarker v-if="destination" :position="destination" :clickable="true" />
      </GmapMap>
    </div>
  </div>
</template>
<script>
export default {
  props: ["label"],
  data() {
    return {
      startPoint: null,
      destination: null,
      center: { lat: 55, lng: 54 },
      options: {
        disableDefaultUI: true
      }
    };
  },
  methods: {
    setStartpoint(place) {
      this.startPoint = {
        lat: place.geometry.location.lat(),
        lng: place.geometry.location.lng()
      };
      this.center = this.startPoint;
      this.$emit("set-start-point", this.startPoint);
    },
    setDestination(place) {
      this.destination = {
        lat: place.geometry.location.lat(),
        lng: place.geometry.location.lng()
      };
      this.$emit("set-destination", this.destination);
    }
  }
};
</script>
<style>
.location-input {
  padding: 10px;
  background-color: white;
  height: 50px;
  width: 100%;
  z-index: 99999;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

.map-input-container {
  display: flex;
  flex-wrap: wrap;
  width: 325px;
  position: absolute;
  left: 10px;
  top: 10px;
  padding: 25px;
  border-radius: 10px;
  z-index: 9000;
  background-color: rgba(125, 125, 125, 0.25);
}

.input-destination {
  margin-top: 25px;
}

.button-map {
  z-index: 99999;
  margin-top: 25px;
  margin-bottom: 25px;
  margin-left: 0px;
  margin-right: 0px;
}

.button-map-first {
  margin-right: 25px !important;
}

.visible {
  z-index: 99999;
  margin-bottom: 12px;
  color: white;
  text-shadow: 1px 1px 1px rgb(125, 125, 125);
}

.pac-container {
  z-index: 99999;
}

.my-map {
  height: 100vh;
  margin-top: -64px;
  padding-top: 64px;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
  width: 100%;
   z-index: 0;
}
</style>

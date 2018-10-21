<template>
  <div>
    <div style="width: 100%; position: relative">
      <div class="map-input-container">
        <gmap-autocomplete @place_changed="setStartpoint" class="location-input input-startpoint" placeholder="Enter start point">
        </gmap-autocomplete>
        <gmap-autocomplete @place_changed="setDestination" class="location-input input-destination" placeholder="Enter destination">
        </gmap-autocomplete>
      </div>
      <GmapMap :center="center" :zoom="7" style="width: 100%; height: 700px" :options="options">
        <GmapMarker v-if="startPoint" :position="startPoint" :clickable="true" />
        <GmapMarker v-if="destination" :position="destination" :clickable="true" />
      </GmapMap>
    </div>
  </div>
</template>
<script>
export default {
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
  left: 0px;
  top: 0px;
  padding: 25px;

}

.input-destination {
  margin-top: 25px;
}
</style>

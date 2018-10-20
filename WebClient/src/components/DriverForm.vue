<template>
    <div>
        <h1>DriverForm</h1>
        <h3>Start point:</h3>
        <gmap-autocomplete @place_changed="setStartpoint">
        </gmap-autocomplete>
        <h3>Destination:</h3>
        <gmap-autocomplete @place_changed="setDestination">
        </gmap-autocomplete>
        <GmapMap :center="center" :zoom="7" style="width: 700px; height: 700px">
            <GmapMarker v-if="startPoint" :position="startPoint" :clickable="true" />
            <GmapMarker v-if="destination" :position="destination" :clickable="true" />
        </GmapMap>
        <h4 v-if="startPoint"> Start point: {{startPoint.lat }} : {{startPoint.lng }}</h4>
        <h4 v-if="destination"> Destination: {{destination.lat }} : {{destination.lng }}</h4>
    </div>
</template>
<script>
export default {
  data() {
    return {
      startPoint: null,
      destination: null,
      center: {lat:20, lng:20}
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
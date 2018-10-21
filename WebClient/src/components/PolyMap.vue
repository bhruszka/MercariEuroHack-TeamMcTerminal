<template>
    <GmapMap :center="center" :zoom="8" class="poly-map" :options="options">
        <gmap-polyline v-if="path.length > 0" :path="path" ref="polyline">
      </gmap-polyline>
    </GmapMap>
</template>
<script>
export default {
  props: ["path"],
  data() {
    return {
      startPoint: null,
      destination: null,
      center: { lat: 52.2297, lng: 21.0122 },
      options: {
        disableDefaultUI: true
      }
    };
  },
  methods: {}
};
</script>
<style>
.poly-map {
  height: 100%;
  width: 100%;
}
</style>


<template>
    <GmapMap :center="center" :zoom="12" class="poly-map" :options="options">
        <gmap-polyline v-if="path != null && path.length > 0" :path="full_path" ref="polyline" :options="{strokeColor: 'red'}">
        </gmap-polyline>
        <gmap-marker v-for="(m, index) in path" :position="m" :key="index" ></gmap-marker>
    </GmapMap>
</template>
<script>
export default {
  props: ["path", "full_path", "users"],
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


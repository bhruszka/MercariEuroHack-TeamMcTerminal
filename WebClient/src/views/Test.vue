<template>
    <GmapMap :center="center" :zoom="12" class="poly-map" :options="options">
        <div v-for="(element, index) in data" :key="index">
            <gmap-marker v-for="(m, index2) in element.path" :position="m" :key="index2"></gmap-marker>
            <gmap-polyline v-if="element.full_path != null && element.full_path.length > 0" :path="element.full_path" ref="polyline" :options="{strokeColor: colorArray[index]}">
            </gmap-polyline>
        </div>
        <!-- <gmap-polyline v-if="path != null && path.length > 0" :path="full_path" ref="polyline">
        </gmap-polyline> -->
    </GmapMap>
</template>
<script>
import axios from "axios";

export default {
  data() {
    return {
      center: { lat: 52.2297, lng: 21.0122 },
      data: [],
      options: {
        disableDefaultUI: true
      },
      colorArray: [
        "#FF6633",
        "#FFB399",
        "#FF33FF",
        "#FFFF99",
        "#00B3E6",
        "#E6B333",
        "#3366E6",
        "#999966",
        "#99FF99",
        "#B34D4D",
        "#80B300",
        "#809900",
        "#E6B3B3",
        "#6680B3",
        "#66991A",
        "#FF99E6",
        "#CCFF1A",
        "#FF1A66",
        "#E6331A",
        "#33FFCC",
        "#66994D",
        "#B366CC",
        "#4D8000",
        "#B33300",
        "#CC80CC",
        "#66664D",
        "#991AFF",
        "#E666FF",
        "#4DB3FF",
        "#1AB399",
        "#E666B3",
        "#33991A",
        "#CC9999",
        "#B3B31A",
        "#00E680",
        "#4D8066",
        "#809980",
        "#E6FF80",
        "#1AFF33",
        "#999933",
        "#FF3380",
        "#CCCC00",
        "#66E64D",
        "#4D80CC",
        "#9900B3",
        "#E64D66",
        "#4DB380",
        "#FF4D4D",
        "#99E6E6",
        "#6666FF"
      ]
    };
  },
  mounted() {
    var self = this;
    axios
      .get("https://carpooling.com.pl:4242/api/routes_all/")
      .then(function(response) {
        // self.full_path = response.data.full_path;
        // self.path = response.data.path;
        self.data = response.data;
        console.log(response);
      })
      .catch(function(error) {
        self.errorText = error.message;
      });
  }
};
</script>


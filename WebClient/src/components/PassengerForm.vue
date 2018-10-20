<template>
    <div>
        <h1>Passenger</h1>
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
  deta() {
    return {
      startPoint: null,
      destination: null
    };
  }
};
</script>
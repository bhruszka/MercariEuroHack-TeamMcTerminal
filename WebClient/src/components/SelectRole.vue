<template>
    <v-flex xs12 d-flex style="height: 100%" class="background-dudes">
        <v-flex xs6>
            <v-btn @click.native="$emit('set-role', 'driver')" class="role-button left-dude" color="transparent">Driver</v-btn>
        </v-flex>
        <v-flex xs6>
            <v-btn @click.native="$emit('set-role', 'passenger')" class="role-button right-dude" color="transparent">Passenger</v-btn>
        </v-flex>
    </v-flex>
</template>
<script>
export default {};
</script>
<style scoped>
.role-button {
  width: 100%;
  height: 100%;
  color: white;
  text-shadow: 2px 2px 2px rgb(125, 125, 125);
  font-size: 30px;
}
.background-dudes {
  background-image: url("https://images.unsplash.com/photo-1537211790624-e6f568af4b13");
  background-size: cover;
}
</style>

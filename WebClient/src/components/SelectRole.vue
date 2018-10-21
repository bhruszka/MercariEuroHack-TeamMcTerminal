<template>
    <v-flex xs12 d-flex>
        <v-flex xs6>
            <v-btn @click.native="$emit('set-role', 'driver')" class="role-button">Driver</v-btn>
        </v-flex>
        <v-flex xs6>
            <v-btn @click.native="$emit('set-role', 'passenger')" class="role-button">Passenger</v-btn>
        </v-flex>
    </v-flex>
</template>
<script>
export default {};
</script>
<style scoped>
.role-button {
  width: 100%;
  height: 100px;
}
</style>

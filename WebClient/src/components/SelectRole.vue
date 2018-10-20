<template>
    <div>
        <v-layout>
            <v-btn @click.native="$emit('set-role', 'driver')">Driver</v-btn>
            <v-btn @click.native="$emit('set-role', 'passenger')">Passenger</v-btn>
        </v-layout>
    </div>
</template>
<script>
export default {

    
};
</script>
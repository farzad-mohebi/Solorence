<template>
  <v-card max-width="400"
          class="mx-auto"
          elevation="0"
          color="transparent"
  >
    <v-card-text class="text-center">
      <div class="ma-4 ">
        <v-img src="~/assets/svg/push-failed.svg"
               width="100%"
               contain
        />
      </div>
      <h1 class="text-center mt-5 text-red py-5">
        Payment Failed
      </h1>
      <v-btn :to="localePath('/')"
             color="primary"
             variant="tonal"
      >
        Return Home
      </v-btn>
    </v-card-text>
  </v-card>
</template>

<script setup>

</script>

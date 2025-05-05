<template>
  <v-card max-width="400"
          class="mx-auto"
          elevation="0"
          color="transparent"
  >
    <v-card-text class="text-center">
      <div class="ma-4 ">
        <v-img src="~/assets/svg/push-success.svg"
               width="100%"
               contain
        />
      </div>
      <h1 class="text-center mt-5 text-green py-5">
        Payment Success
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
const sessionID = ref()
const route = useRoute()
console.log(route.query.session_id)
sessionID.value = route.query.session_id
if (!sessionID.value) {
  navigateTo('/payment/failed')
}
const { data, error } = await useAuthAPIFetch('/api/v1/payment/confirm/', {
  method: 'POST',
  body: {
    session_id: sessionID,
  },
})
if (error.value) {
  navigateTo('/payment/failed')
}
else {
  console.log(data.value)
}
</script>

<template>
  <div name="snackbars">
    <v-snackbar v-model="utilsStore.message.show"
                location="top right"
                :timeout="utilsStore.message.timeout"
                :color="utilsStore.message.color"
    >
      {{ $t(utilsStore.message.text) }}
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { useUtilsStore } from '~/store/utils'

const utilsStore = useUtilsStore()
</script>

<style>
.v-snack__wrapper,
div[name="snackbars"] {
    z-index: 99999999 !important;
}
</style>

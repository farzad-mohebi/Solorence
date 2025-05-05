<template>
  <div>
    <v-card variant="0"
            class="pa-2 bg-white mb-3 "
            rounded="lg"
    >
      <v-card-actions class="px-3">
        <nuxt-link to="/"
                   class="me-5 d-flex align-center text-decoration-none"
        >
          <v-img width="35"
                 src="/assets/logo/android-icon-48x48.png"
          />
          <div class="font-weight-bold text-h6 ms-2 text-primary">
            Solorence
          </div>
        </nuxt-link>
        <v-btn rounded="lg"
               size="large"
               class="text-none"
        >
          Home
        </v-btn>
        <v-btn rounded="lg"
               size="large"
               class="text-none ms-3"
        >
          Products
        </v-btn>
        <v-btn rounded="lg"
               size="large"
               class="text-none ms-3"
        >
          Blog
        </v-btn>
        <v-spacer />
        <v-btn
          icon
          variant="text"
          @click="toggleTheme"
        >
          <v-icon :icon="cookieTheme === 'dark' ? 'mdi-weather-sunny' : 'mdi-weather-night'" />
        </v-btn>
        <v-btn :to="localePath('/login')"
               rounded="lg"
               size="large"
               class="text-none ms-3"
        >
          Login to Account
        </v-btn>
      </v-card-actions>
    </v-card>
    <div class="text-center">
      <h1 class="text-h1 font-weight-bold mt-10 pt-5 mb-5"
          style="background: radial-gradient(circle, rgba(121,85,72,0.1) 0%, rgba(0,0,0,0) 100%);"
      >
        Solorence
      </h1>
      <h2 class="mb-10">
        Write and Connect your Students to your Notes
      </h2>
      <v-btn size="x-large"
             :to="localePath('/login')"
             color="primary"
             variant="flat"
      >
        Start for Free
      </v-btn>
    </div>
    <IndexFeatures/>
  </div>
</template>

<script setup>
import { useTheme } from 'vuetify'
import { VSpacer } from 'vuetify/components'

const theme = useTheme()
const cookieTheme = useCookie('theme')
theme.global.name.value = cookieTheme.value === 'dark' ? 'dark' : 'light'
const toggleTheme = () => {
  const cookieTheme = useCookie('theme')
  cookieTheme.value = cookieTheme.value === 'dark' ? 'light' : 'dark'
  theme.global.name.value = cookieTheme.value
}
useHead(seoConfig('index_page_title'))
definePageMeta({
  layout: 'empty',
})
const { t, locale } = useI18n()
const localePath = useLocalePath()
</script>

<style></style>

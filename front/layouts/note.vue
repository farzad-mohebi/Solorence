<template>
  <v-app>
    <v-locale-provider :rtl="isRTL">
      <MessageComponent />
      <GoogleCalendarDialog />
      <v-main>
        <slot />
      </v-main>
    </v-locale-provider>
  </v-app>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/store/auth'

const { locale } = useI18n()

const localePath = useLocalePath()

useHead({
  htmlAttrs: { dir: locale.value === 'fa' ? 'rtl' : 'ltr', lang: locale.value },
})

const isRTL = ref(locale.value === 'fa')

watch(locale, (newLocale) => {
  isRTL.value = newLocale === 'fa'
  useHead({
    htmlAttrs: { dir: locale.value === 'fa' ? 'rtl' : 'ltr', lang: locale.value },
  })
})
const authStore = useAuthStore()

if (!authStore.isAuthenticated) {
  navigateTo(localePath('/login'))
}
await authStore.getMyInfo()

if (!authStore.info) {
  authStore.logUserOut()
  navigateTo(localePath('/login'))
}
</script>

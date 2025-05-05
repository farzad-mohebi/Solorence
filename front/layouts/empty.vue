<template>
  <v-app>
    <v-locale-provider :rtl="isRTL">
      <MessageComponent />
      <v-main class="">
        <v-container>
          <slot />
        </v-container>
      </v-main>
    </v-locale-provider>
  </v-app>
</template>

<script setup>
const { locale } = useI18n()
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
</script>

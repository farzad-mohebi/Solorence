<script setup lang="ts">
import { useLocale } from 'vuetify'

const { locale, setLocale } = useI18n()
const { current } = useLocale() // Vuetify

const items = ref([
  { title: 'English', value: 'en' },
  { title: 'Persian', value: 'fa' },
  { title: 'Finland', value: 'fi' },
])

const select = ref({ title: items.value.find(d => d.value === (locale.value || 'en'))?.title, value: locale.value || 'en' })

current.value = select.value.value

const updateLang = () => {
  setLocale(select.value.value)
  current.value = select.value.value
}
</script>

<template>
  <div>
    <v-select v-model="select"
              hide-details
              class="pb-3"
              variant="plain"
              :items="items"
              item-title="title"
              item-value="value"
              label="Select"
              persistent-hint
              return-object
              single-line
              @update:menu="updateLang"
    />
  </div>
</template>

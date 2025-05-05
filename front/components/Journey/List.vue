<template>
  <v-card elevation="0"
          :title="$t('your_journeyes')"
          :subtitle="$t('your_journeyes_description')"
  >
    <template #prepend>
      <v-icon icon="mdi-human-greeting"
              size="x-large"
              class="me-2"
      />
    </template>
    <template #append>
      <v-btn
        id="add-journey"
        color="green"
        variant="flat"
        @click="journeyDialog = true; selectedJourney = { ...JourneyDefaultValue }"
      >
        {{ $t('new_journey') }}
      </v-btn>
    </template>
    <template v-if="loading">
      <v-skeleton-loader v-for="_ in 10"
                         :key="_"
                         type="list-item-avatar"
                         width="400"
                         max-width="100%"
                         class="mt-1"
      />
    </template>
    <v-card v-else-if="journeys.length > 0"
            elevation="0"
            class="py-2 overflow-auto"
            max-height="600"
    >
      <v-timeline
        side="end"
      >
        <v-timeline-item v-for="journey in journeys"
                         :key="journey.id"
                         class="journey"
                         dot-color="primary"
                         size="small"
        >
          <template #opposite>
            <span>{{ timeAgo(new Date(journey.action_at)) }}</span>
          </template>
          <v-card class="elevation-2 me-5">
            <v-card-title class="text-h6">
              {{ journey.title }}
              <v-btn icon
                     size="x-small"
                     flat
                     @click="journeyDialog = true; selectedJourney = { ...journey }"
              >
                <v-icon icon="mdi-pencil" />
              </v-btn>
            </v-card-title>
            <v-card-text v-if="journey.description">
              {{ journey.description }}
            </v-card-text>
          </v-card>
        </v-timeline-item>
      </v-timeline>
    </v-card>
    <template v-else>
      <VCardText>
        No Journey ...
      </VCardText>
    </template>
    <JourneyManager />
  </v-card>
</template>

<script setup lang="ts">
import { useUtilsStore } from '~/store/utils'
import { JourneyDefaultValue, type Journey } from '~/composables/models/Journey.js'
import { timeAgo } from '~/composables/custom_functions.js'

const selectedJourney = useState<Journey>('selectedJourney', () => {
  return { ...JourneyDefaultValue }
})

const journeyDialog = useState<boolean>('journeyDialog', () => false)
const journeys = useState<Journey[]>('journeys', () => [])
const utilStore = useUtilsStore()
const loading = ref<boolean>(true)

const getjourneys = async (): Promise<void> => {
  loading.value = true
  const { error, data } = await useAuthAPIFetch<Journey[]>('/api/v1/journey/')

  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else if (data.value) {
    journeys.value = data.value
  }
  loading.value = false
}
getjourneys()
</script>

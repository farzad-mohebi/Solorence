<template>
  <div>
    <v-dialog v-model="journeyDialog"
              max-width="600"
    >
      <v-card prepend-icon="mdi-check-circle-outline"
              :title="selectedJourney.id ? $t('update_journey') : $t('new_journey')"
      >
        <v-card-text class="mt-2">
          <v-text-field v-model="selectedJourney.title"
                        name="title"
                        :label="$t('title')"
                        required
          />
          <v-textarea v-model="selectedJourney.description"
                      name="description"
                      :label="$t('description')"
                      required
          />
          <!-- <v-row>
            <v-col md="6">
              <v-date-input id="journey-due-date"
                            v-model="action_at"
                            hide-actions
                            clearable
                            :label="$t('action_at')"
                            hide-details
                            @click:clear="action_at = null"
              />
            </v-col>
          </v-row> -->
        </v-card-text>
        <v-divider />
        <v-card-actions>
          <v-btn v-if="selectedJourney.id"
                 color="red"
                 variant="flat"
                 @click="deleteDialog = true"
          >
            {{
              $t('delete')
            }}
          </v-btn>
          <v-spacer />
          <v-btn :text="$t('cancel')"
                 variant="plain"
                 @click="journeyDialog = false"
          />
          <v-btn color="primary"
                 :text="selectedJourney.id ? $t('update') : $t('save')"
                 variant="flat"
                 @click="selectedJourney.id ? updateJourney() : createJourney()"
          />
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="deleteDialog"
              width="auto"
              persistent
              max-width="400"
    >
      <v-card :loading="loading"
              max-width="400"
              prepend-icon="mdi-alert"
              :text="$t('delete_sure')"
              :title="$t('deleting') + '!'"
      >
        <template #actions>
          <v-spacer />
          <v-btn variant="plain"
                 @click="deleteDialog = false"
          >
            {{ $t('cancel') }}
          </v-btn>
          <v-btn variant="elevated"
                 color="red"
                 @click="deleteJourney()"
          >
            {{ $t('yes_delete_it') }}
          </v-btn>
        </template>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { useUtilsStore } from '~/store/utils'
import { JourneyDefaultValue, type Journey } from '~/composables/models/Journey.js'

const utilStore = useUtilsStore()

const action_at = ref<Date | null>(null)
const loading = ref<any>(false)

const selectedJourney = useState<Journey>('selectedJourney', () => {
  return { ...JourneyDefaultValue }
})
const journeyDialog = useState<boolean>('journeyDialog', () => false)
const journeys = useState<Journey[]>('journeys', () => [])
const deleteDialog = ref(false)
const createJourney = async () => {
  if (!selectedJourney.value) {
    return
  }
  loading.value = true
  const { error, data } = await useAuthAPIFetch('/api/v1/journey/', {
    method: 'POST',
    body: {
      ...selectedJourney.value,
      // action_at: action_at.value ? action_at.value.toISOString().split('T')[0] : null,
      action_at: undefined,
    },
  })
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else {
    utilStore.showSuccessMessage('created_successfully')

    journeys.value = [data.value as Journey, ...journeys.value]
    selectedJourney.value = { ...JourneyDefaultValue }

    journeyDialog.value = false
  }
  loading.value = false
}
const updateJourney = async () => {
  loading.value = true
  const { error, data } = await useAuthAPIFetch<Journey>(`/api/v1/journey/${selectedJourney.value.id}/`, {
    method: 'PUT',
    body: {
      ...selectedJourney.value,
      // action_at: action_at.value ? action_at.value.toISOString().split('T')[0] : null,
    },
  })
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else if (data.value) {
    utilStore.showSuccessMessage('updated_successfully')
    journeys.value = journeys.value.map((journey: Journey) => {
      if (journey.id === data.value?.id) {
        return { ...data.value } as Journey
      }
      return journey
    })
    selectedJourney.value = { ...JourneyDefaultValue }
    action_at.value = null
    journeyDialog.value = false
  }
  loading.value = false
}
const loadJourney = async () => {
  loading.value = true
  const { error, data } = await useAuthAPIFetch<Journey>(`/api/v1/journey/${selectedJourney.value.id}/`)
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else if (data.value) {
    selectedJourney.value = data.value
    if (selectedJourney.value.action_at)
      action_at.value = new Date(selectedJourney.value.action_at)
  }
  loading.value = false
}
const deleteJourney = async () => {
  loading.value = true
  const { error } = await useAuthAPIFetch(`/api/v1/journey/${selectedJourney.value.id}/`, {
    method: 'DELETE',
  })
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else {
    utilStore.showSuccessMessage('deleted_successfully')
    journeys.value = journeys.value.filter(journey => journey.id !== selectedJourney.value.id)

    selectedJourney.value = { ...JourneyDefaultValue }
    journeyDialog.value = false
    deleteDialog.value = false
  }
  loading.value = false
}
watch(journeyDialog, async () => {
  if (selectedJourney.value.id && !selectedJourney.value.title) {
    await loadJourney()
  }
  if (selectedJourney.value.action_at)
    action_at.value = new Date(selectedJourney.value.action_at)
  else
    action_at.value = null
  if (!journeyDialog.value) {
    selectedJourney.value = { ...JourneyDefaultValue }
    action_at.value = null
  }
  if (journeyDialog.value) {
    loading.value = false
  }
})
</script>

<style></style>

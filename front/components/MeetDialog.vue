<template>
  <div>
    <v-dialog v-model="meetDialog"
              max-width="600"
    >
      <v-card prepend-icon="mdi-check-circle-outline"
              :title="selectedEvent.id ? $t('update_meet') : $t('add_new_meet')"
      >
        <v-card-text class="mt-2">
          <v-text-field v-model="selectedEvent.title"
                        name="title"
                        :label="$t('title')"
                        required
          />
          <v-textarea v-model="selectedEvent.description"
                      name="description"
                      :label="$t('description')"
                      required
          />
          <v-date-input id="meet-due-date"
                        v-model="selectedDateModel"
                        :allowed-dates="checkDateBiggerThanToday"
                        hide-actions
                        clearable
                        :label="$t('selectedDate')"
                        prepend-icon="mdi-calendar"
                        @click:clear="selectedDate = null"
          />
          <v-row>
            <v-col cols="12"
                   md="6"
            >
              <v-text-field v-model="startTime"
                            class="event-time-start"
                            :active="startTimeModal"
                            :focused="startTimeModal"
                            label="Start at"
                            prepend-icon="mdi-clock-time-four-outline"
                            readonly
              >
                <v-dialog v-model="startTimeModal"
                          activator="parent"
                          width="auto"
                >
                  <v-card>
                    <v-time-picker v-if="startTimeModal"
                                   v-model="startTime"
                                   class="event-start-time-picker"
                                   color="green"
                                   format="24hr"
                    />
                    <v-card-actions class="justify-center">
                      <v-btn class="close-time-picker"
                             text="SET"
                             block
                             @click="startTimeModal = false"
                      />
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-text-field>
            </v-col>
            <v-col cols="12"
                   md="6"
            >
              <v-text-field v-model="endTime"
                            class="event-time-end"
                            :active="endTimeModal"
                            :focused="endTimeModal"
                            label="Finish at"
                            prepend-icon="mdi-clock-time-four-outline"
                            readonly
              >
                <v-dialog v-model="endTimeModal"
                          activator="parent"
                          width="auto"
                >
                  <v-card>
                    <v-time-picker v-if="endTimeModal"
                                   v-model="endTime"
                                   class="event-end-time-picker"
                                   color="pink"
                                   format="24hr"
                    />
                    <v-card-actions class="justify-center">
                      <v-btn class="close-time-picker"
                             text="SET"
                             block
                             @click="endTimeModal = false"
                      />
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-text-field>
            </v-col>
          </v-row>
          <v-checkbox v-if="!selectedEvent.id"
                      v-model="hasLink"
                      hide-details
                      color="primary"
                      label="With Link/Location"
          />
          <template v-if="hasLink || selectedEvent.id">
            <v-select v-model="selectedEvent.place"
                      :label="$t('place')"
                      class="mb-3"
                      item-value="key"
                      item-title="name"
                      hide-details
                      :items="[
                        { key: 0, name: $t('private') },
                        { key: 1, name: $t('google_meet') },
                        { key: 2, name: $t('zoom') },
                        { key: 3, name: $t('location') },
                        { key: 4, name: $t('link') },
                      ]"
            >
              <template #prepend>
                <span class="d-flex align-center"
                      v-html="placeIcon[selectedEvent.place]"
                />
              </template>
              <template #item="{ props, item }">
                <v-list-item v-bind="props">
                  <template #prepend>
                    <span class="pe-3 d-flex align-center"
                          style="height: 50px;"
                          v-html="placeIcon[item.value]"
                    />
                  </template>
                </v-list-item>
              </template>
            </v-select>
          </template>
          <template v-if="hasLink || selectedEvent.id">
            <!-- <v-checkbox hide-details v-if="!selectedEvent.id && !selectedEvent.place === " color="primary"
                            v-model="selectedEvent.noAddress" label="Generate a Link"></v-checkbox> -->
            <!-- <template v-if="!selectedEvent.noAddress || selectedEvent.id"> -->
            <v-text-field v-model="selectedEvent.address"
                          label="Link/Address"
            />
            <!-- </template> -->
          </template>
        </v-card-text>
        <v-divider />
        <v-card-actions>
          <v-btn v-if="selectedEvent.id"
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
                 @click="meetDialog = false"
          />
          <v-btn color="primary"
                 :text="selectedEvent.id ? $t('update') : $t('save')"
                 variant="flat"
                 @click="selectedEvent.id ? updateEvent() : createEvent()"
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
                 @click="deleteDialog = false; clearValues()"
          >
            {{ $t('cancel') }}
          </v-btn>
          <v-btn variant="elevated"
                 color="red"
                 @click="deleteEvent()"
          >
            {{ $t('yes_delete_it') }}
          </v-btn>
        </template>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { EventModelDefaultValue, type EventModel } from '~/composables/models/Event'
import { useUtilsStore } from '~/store/utils'
import { checkDateBiggerThanToday } from '~/composables/custom_functions.js'

const utilStore = useUtilsStore()
const route = useRoute()

const selectedDate = ref<string | null>()
const selectedDateModel = ref<Date | null>()
const startTime = ref<string | null>()
const endTime = ref<string | null>()
const startTimeModal = ref<boolean>(false)
const endTimeModal = ref<boolean>(false)

const eventDialog = useState('eventDialog', () => false)
const noAddress = ref<boolean>(false)
const hasLink = ref<boolean>(false)
const loading = ref(false)
const selectedEvent = useState<EventModel>('selectedEvent', () => {
  return { ...EventModelDefaultValue }
})
const meetDialog = useState('meetDialog', () => false)
const meets = useState<EventModel[]>('meets', () => [])
const deleteDialog = ref(false)

const clearValues = () => {
  startTime.value = null
  endTime.value = null
  selectedEvent.value = { ...EventModelDefaultValue }
  selectedDateModel.value = null
}
// CRUD Functions

const createEvent = async () => {
  loading.value = true
  const { error, data } = await useAuthAPIFetch<EventModel>('/api/v1/event/', {
    method: 'POST',
    body: {
      ...selectedEvent.value,
      start_at: new Date(selectedDate.value + ' ' + startTime.value).toISOString(),
      end_at: new Date(selectedDate.value + ' ' + endTime.value).toISOString(),
      note: route.params?.id,
    },
  })
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else if (data.value) {
    utilStore.showSuccessMessage('created_successfully')

    // @ts-expect-error: 'set_event_state' is not typed on the Window object
    if (window['set_meet_state']) window['set_meet_state']('set', data.value)
    meets.value = [data.value, ...meets.value]

    meetDialog.value = false
    clearValues()
  }
  loading.value = false
}
const updateEvent = async () => {
  loading.value = true
  const { error, data } = await useAuthAPIFetch<EventModel>(`/api/v1/event/${selectedEvent.value.id}/`, {
    method: 'PUT',
    body: {
      ...selectedEvent.value,
      start_at: new Date(selectedDate.value + ' ' + startTime.value).toISOString(),
      end_at: new Date(selectedDate.value + ' ' + endTime.value).toISOString(),
    },
  })
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else if (data.value) {
    utilStore.showSuccessMessage('updated_successfully')
    meets.value = meets.value.map((meet: EventModel) => {
      if (meet.id === data.value?.id) {
        meet = { ...data.value }
      }
      return meet
    })
    clearValues()
    meetDialog.value = false

    // @ts-expect-error: 'update_meet_ID' is not typed on the Window object
    if (window['update_meet_' + data.value.id]) window['update_meet_' + data.value.id](data.value)
  }
  loading.value = false
}
const loadEvent = async () => {
  loading.value = true
  const { error, data } = await useAuthAPIFetch<EventModel>(`/api/v1/event/${selectedEvent.value.id}/`)
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else if (data.value) {
    selectedEvent.value = data.value
    if (selectedEvent.value.address)
      noAddress.value = false
    if (data.value.start_at) {
      const startAt = new Date(data.value.start_at)
      selectedDateModel.value = startAt
      startTime.value = `${String(startAt.getHours()).padStart(2, '0')}:${String(startAt.getMinutes()).padStart(2, '0')}`
    }
    if (data.value.end_at) {
      const endAt = new Date(data.value.end_at)
      endTime.value = `${String(endAt.getHours()).padStart(2, '0')}:${String(endAt.getMinutes()).padStart(2, '0')}`
    }
  }
  loading.value = false
}
const deleteEvent = async () => {
  loading.value = true
  const { error } = await useAuthAPIFetch(`/api/v1/event/${selectedEvent.value.id}/`, {
    method: 'DELETE',
  })
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else {
    utilStore.showSuccessMessage('deleted_successfully')
    meets.value = meets.value.filter(meet => meet.id !== selectedEvent.value.id)
    // @ts-expect-error: 'update_meet_ID' is not typed on the Window object
    if (window['update_meet_' + selectedEvent.value.id]) window['update_meet_' + selectedEvent.value.id]('deleted')
    clearValues()
    deleteDialog.value = false
    meetDialog.value = false
  }
  loading.value = false
}

// Watches

watch(meetDialog, async () => {
  if (selectedEvent.value.id && !selectedEvent.value.title) {
    await loadEvent()
  }
  if (meetDialog.value === false) {
    // @ts-expect-error: 'set_event_state' is not typed on the Window object
    if (window['set_meet_state']) window['set_meet_state']('cancel')
  }
  if (selectedEvent.value) {
    // if (selectedEvent.value.selectedDate)
    //   selectedDate.value = new Date(selectedEvent.value.selectedDate)
  }
  if (!meetDialog.value) {
    clearValues()
  }
})
watch(selectedDateModel, async () => {
  const selected = selectedDateModel.value || new Date()
  selected.setHours(12)
  selectedDate.value = selected.toISOString().split('T')[0].replace(/-/g, '/')
})
watch(eventDialog, async () => {
  if (selectedEvent.value.id && !selectedEvent.value.title) {
    await loadEvent()
  }
  if (eventDialog.value === false) {
    // @ts-expect-error: 'set_event_state' is not typed on the Window object
    if (window['set_event_state']) window['set_event_state']('cancel')
  }
})
</script>

<style></style>

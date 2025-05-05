<template>
  <v-menu v-model="calendarMenu"
          :close-on-content-click="false"
          location="end"
          :target="calendarMenuTarget"
  >
    <v-card min-width="300"
            prepend-icon="mdi-calendar-clock"
            :subtitle="'Start: ' + new Date(selectedCalendarEvent.start).toLocaleString()"
            :title="selectedCalendarEvent.title"
    >
      <v-card-text style="max-width: 350px;">
        <p>
          {{ selectedCalendarEvent.description }}
        </p>
      </v-card-text>

      <v-card-actions>
        <p class="text-body-2 text-grey text-center"
           style="max-width: 125px;"
        >
          End: {{ new Date(selectedCalendarEvent.start).toLocaleString() }}
        </p>
        <v-spacer />

        <v-btn size="small"
               title="delete"
               color="red"
               variant="text"
               icon="mdi-delete"
               @click="setSelectedEvent(selectedCalendarEvent as EventModel); deleteDialog = true"
        />
        <v-btn size="small"
               title="edit"
               color="primary"
               variant="text"
               icon="mdi-pencil"
               @click="setSelectedEvent(selectedCalendarEvent as EventModel); eventDialog = true; calendarMenu = false;"
        />
        <v-btn size="small"
               title="close"
               variant="text"
               icon="mdi-close"
               @click="calendarMenu = false"
        />
      </v-card-actions>
    </v-card>
  </v-menu>
  <v-dialog v-model="eventDialog"
            max-width="900"
  >
    <v-card prepend-icon="mdi-calendar-clock"
            :loading="loading"
            :title="selectedEvent.id ? 'Update Event' : 'Add new Event'"
    >
      <v-card-text class="mt-2">
        <v-row>
          <v-col md="6"
                 class="d-flex align-center justify-center"
          >
            <v-date-picker v-model="selectedDateModel"
                           :allowed-dates="checkDateBiggerThanToday"
                           color="primary"
                           show-adjacent-months
            />
          </v-col>
          <v-col md="6">
            <v-text-field v-model="selectedEvent.title"
                          name="title"
                          :label="$t('title')"
                          required
            />
            <v-textarea v-model="selectedEvent.description"
                        :label="$t('description')"
                        required
                        name="description"
            />
            <v-row>
              <v-col cols="12"
                     md="12"
              >
                <v-text-field id="event-date-picker"
                              v-model="selectedDate"
                              :label="$t('date')"
                              prepend-icon="mdi-calendar"
                />
              </v-col>
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
          </v-col>
        </v-row>
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
        <v-btn text="Close"
               variant="plain"
               @click="eventDialog = false"
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
               @click="deleteDialog = false"
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
</template>

<script setup lang="ts">
import { type EventModel, type CalendarEventModel, EventModelDefaultValue, CalendarEventDefaultValue } from '~/composables/models/Event.js'
import { useUtilsStore } from '~/store/utils'
import { checkDateBiggerThanToday } from '~/composables/custom_functions.js'

const selectedCalendarEvent = ref<CalendarEventModel>({ ...CalendarEventDefaultValue })
const calendarMenuTarget = useState<Element | string>('calendarMenuTarget', () => 'parent')
const utilStore = useUtilsStore()
const eventDialog = useState<boolean>('eventDialog', () => false)
const deleteDialog = ref<boolean>(false)
const loading = ref<boolean>(true)
const startTimeModal = ref(false)
const endTimeModal = ref(false)
const calendarMenu = useState<boolean>('calendarMenu', () => false)
const events = useState<CalendarEventModel[]>('calendarEvents', () => [])

const selectedEvent = useState<EventModel>('selectedEvent', () => {
  return { ...EventModelDefaultValue }
})

function showEvent(event: CalendarEventModel, ele: Event) {
  if (calendarMenu.value === true)
    calendarMenu.value = false
  else
    calendarMenu.value = true
  calendarMenuTarget.value = ele?.target as Element || 'parent'
  selectedCalendarEvent.value = { ...event }
  setTimeout(() => {
    calendarMenu.value = true
  }, 300)
}
defineExpose({ showEvent })
const createEvent = async () => {
  loading.value = true
  const { error, data } = await useAuthAPIFetch<EventModel>('/api/v1/event/', {
    method: 'POST',
    body: {
      title: selectedEvent.value.title,
      description: selectedEvent.value.description,
      start_at: new Date(selectedDate.value + ' ' + startTime.value).toISOString(),
      end_at: new Date(selectedDate.value + ' ' + endTime.value).toISOString(),
    },
  })
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else if (data.value) {
    utilStore.showSuccessMessage('created_successfully')

    // @ts-expect-error: 'set_event_state' is not typed on the Window object
    if (window['set_event_state']) window['set_event_state']('set', data.value)

    events.value.push({
      title: selectedEvent.value.title,
      description: selectedEvent.value.description,
      start: new Date(selectedDate.value + ' ' + startTime.value),
      end: new Date(selectedDate.value + ' ' + endTime.value),
      color: 'red',
      place: selectedEvent.value.place,
      address: selectedEvent.value.address,
      id: data.value.id,
    })
    resetSelectedEvent()
    eventDialog.value = false
  }
  loading.value = false
}
const updateEvent = async () => {
  loading.value = true
  const { error, data } = await useAuthAPIFetch(`/api/v1/event/${selectedEvent.value.id}/`, {
    method: 'PUT',
    body: {
      title: selectedEvent.value.title,
      description: selectedEvent.value.description,
      start_at: new Date(selectedDate.value + ' ' + startTime.value).toISOString(),
      end_at: new Date(selectedDate.value + ' ' + endTime.value).toISOString(),
    },
  })
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else {
    utilStore.showSuccessMessage('created_successfully')

    // @ts-expect-error: 'set_event_state' is not typed on the Window object
    if (window['set_event_state']) window['set_event_state']('set', data.value)

    events.value = events.value.filter(event => event.id !== selectedEvent.value.id)
    events.value.push({
      id: selectedEvent.value.id,
      title: selectedEvent.value.title,
      description: selectedEvent.value.description,
      start: new Date(selectedDate.value + ' ' + startTime.value),
      end: new Date(selectedDate.value + ' ' + endTime.value),
      color: 'red',
      place: selectedEvent.value.place,
      address: selectedEvent.value.address,
    })
    resetSelectedEvent()
    eventDialog.value = false
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
    events.value = events.value.filter(event => event.id !== selectedEvent.value.id)
    resetSelectedEvent()
    eventDialog.value = false
    deleteDialog.value = false
    calendarMenu.value = false
  }
  loading.value = false
}
const resetSelectedEvent = () => {
  selectedEvent.value = { ...EventModelDefaultValue }
}
const selectedDate = ref<string | Date>(new Date().toISOString().split('T')[0].replace(/-/g, '/'))
const selectedDateModel = ref()
const startTime = ref()
const endTime = ref()
watch(selectedDateModel, async () => {
  selectedDate.value = new Date(selectedDateModel.value)
  selectedDate.value.setHours(12)
  selectedDate.value = selectedDate.value.toISOString().split('T')[0].replace(/-/g, '/')
})
const setSelectedEvent = (event: EventModel) => {
  console.log('selectedCalendarEvent.value', event)
  selectedEvent.value = {
    ...event,
  }
  selectedDateModel.value = selectedCalendarEvent.value.start
  startTime.value = getTimeOfDate(selectedCalendarEvent.value.start)
  endTime.value = getTimeOfDate(selectedCalendarEvent.value.end)
  loading.value = false
}
// const events = useState('events', () => [])

const loadEvent = async () => {
  loading.value = true
  const { error, data } = await useAuthAPIFetch<EventModel>(`/api/v1/event/${selectedEvent.value.id}/`)
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else if (data.value) {
    selectedEvent.value = data.value
  }
  loading.value = false
  console.log('loaded', loading.value)
}
watch(eventDialog, async () => {
  if (selectedEvent.value.id && !selectedEvent.value.title) {
    loadEvent()
  }
  if (eventDialog.value === true && !selectedEvent.value.id) {
    startTime.value = ''
    endTime.value = ''
    selectedDateModel.value = new Date()
    loading.value = false
  }
  if (eventDialog.value === false) {
    // @ts-expect-error: 'set_event_state' is not typed on the Window object
    if (window['set_event_state']) window['set_event_state']('cancel')
  }
})
</script>

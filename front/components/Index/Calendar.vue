<template>
  <div class=" py-2 px-2 mb-2 ">
    <template v-if="loading">
      <v-skeleton-loader
        type="table-heading"
        width="100%"
        class="mt-1"
      />
      <v-skeleton-loader
        v-for="_ in 2"
        :key="_"
        type="table-tbody"
        width="100%"
        class="mt-1"
      />
    </template>
    <template v-else>
      <v-calendar
        v-model="focus"
        :events="events"
        :event-color="getEventColor"
        :view-mode="viewMode"
        color="primary"
      >
        <template #event="{ event }">
          <div class="w-100 overflow-hidden">
            <v-chip class="event-chip px-1"
                    style="max-width: 100%;margin-bottom: 2px;"
                    :rounded="0"
                    color="green"
                    label
                    text-color="white"
                    :title="event.title"
                    @click="(e) => eventManager.showEvent(event, e)"
            >
              <v-icon left>
                mdi-label
              </v-icon>
              {{ event.title }}
            </v-chip>
          </div>
        </template>
      </v-calendar>
    </template>
    <EventManager ref="eventManager" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import type { EventModel, CalendarEventModel } from '~/composables/models/Event.js'
import { useUtilsStore } from '~/store/utils'

const eventManager = ref()
const viewMode = useState<'month' | 'day' | 'week' >('viewMode', () => 'month')
const focus = ref<Date[]>([new Date()])
const events = useState<CalendarEventModel[]>('calendarEvents', () => [])
const loading = ref<boolean>(true)
const getEvents = async () => {
  loading.value = true
  const { error, data } = await useAuthAPIFetch<EventModel[]>('/api/v1/event/')
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else if (data.value) {
    events.value = data.value.map((event: EventModel) => {
      return {
        id: event.id,
        title: event.title,
        start: new Date(event.start_at || ''),
        end: new Date(event.end_at || ''),
        color: 'red',
      } as CalendarEventModel
    })
  }
}
onMounted(async () => {
  await nextTick()
  loading.value = false
})

getEvents()

function getEventColor(event: CalendarEventModel) {
  console.log('Event color:', event)
  return event.color
}
const utilStore = useUtilsStore()
</script>

<style>
.v-calendar-weekly__day-alldayevents-container {
  display: none;
}
</style>

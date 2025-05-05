<template>
  <div>
    <Transition>
      <v-card elevation="0"
              class="mb-5 border rounded-lg"
      >
        <v-card-text>
          <v-row v-if="showMode"
                 class="pa-2 pt-4"
                 align="center"
                 justify="space-between"
          >
            <v-col class="text-h5"
                   cols="6"
            >
              <v-row class="center pa-3">
                <v-select v-model="showMode"
                          hide-details
                          item-title="title"
                          item-value="value"
                          color="primary"
                          density="comfortable"
                          max-width="200"
                          :label="$t('show')"
                          :items="[{ title: $t('calendar'), value: 'calendar' }, { title: $t('tasks'), value: 'tasks' }, { title: $t('goals'), value: 'goals' }, { title: $t('journeys'), value: 'journeys' }]"
                          variant="outlined"
                          class="home-show-mode"
                />
                <v-spacer />
              </v-row>
            </v-col>
            <v-col cols="6"
                   class="text-end"
            >
              <v-btn v-if="showMode === 'calendar'"
                     id="add-event"
                     class="me-2"
                     prepend-icon="mdi-plus"
                     color="green"
                     size="large"
                     variant="flat"
                     @click="eventDialog = true;selectedEvent = { ...EventModelDefaultValue }"
              >
                {{ $t('new_event') }}
              </v-btn>
              <v-btn-toggle v-if="showMode === 'calendar'"
                            v-model="viewMode"
                            mandatory
              >
                <v-btn value="day">
                  {{ $t('day') }}
                </v-btn>
                <v-btn value="week">
                  {{ $t('week') }}
                </v-btn>
                <v-btn value="month">
                  {{ $t('month') }}
                </v-btn>
              </v-btn-toggle>
            </v-col>
          </v-row>
          <v-spacer />
          <div v-if="showMode === 'calendar'">
            <IndexCalendar />
          </div>
          <div v-else-if="showMode === 'tasks'">
            <TaskList />
          </div>
          <div v-else-if="showMode === 'goals'">
            <GoalList />
          </div>
          <div v-else-if="showMode === 'journeys'">
            <JourneyList />
          </div>
        </v-card-text>
      </v-card>
    </Transition>
    <h1 class="text-primary mb-2">
      {{ $t('my_notes') }}:
    </h1>
    <v-card class=" mb-5 rounded-lg"
            color="primary"
            elevation="0"
    >
      <v-card-text>
        <v-row>
          <div v-if="!noteLoading"
               class="ma-2"
          >
            <v-card id="create-note"
                    width="300"
                    color="brown-lighten-1"
                    elevation="0"
                    @click="createNewNote()"
            >
              <v-card-text class="text-center align-center d-flex ">
                <v-icon class=""
                        color="white"
                        size="30"
                >
                  mdi-plus-circle
                </v-icon>
                <div class="text-start ms-4 overflow-hidden">
                  <div class="text-body-1 text-white font-weight-bold">
                    {{ $t('new_note') }}
                  </div>
                </div>
              </v-card-text>
            </v-card>
          </div>
          <template v-if="!noteLoading">
            <div v-for="note in notes"

                 :key="note.id"
                 class="ma-2"
            >
              <v-card width="300"
                      class="note-card"
                      elevation="0"
                      :to="localePath(`/note/${note.id}`)"
              >
                <v-card-text class="text-center align-center d-flex ">
                  <v-icon class=""
                          color="primary"
                          size="30"
                  >
                    mdi-file
                  </v-icon>
                  <div class="text-start ms-4 overflow-hidden">
                    <div class="text-body-1 text-truncate font-weight-bold">
                      {{ note.title }}
                    </div>
                  </div>
                </v-card-text>
              </v-card>
            </div>
          </template>
          <div v-if="noteLoading"
               class="d-flex ga-2 ma-2"
          >
            <v-skeleton-loader v-for="_ in 4"
                               :key="_"
                               type="paragraph"
                               width="250"
            />
          </div>
        </v-row>
      </v-card-text>
    </v-card>
    <h1 class="text-light-blue mb-2">
      {{ $t('shared_notes') }}:
    </h1>
    <v-card class=" mb-5 rounded-lg"
            color="light-blue"
            elevation="0"
    >
      <v-card-text>
        <v-row>
          <template v-if="!accessLoading">
            <div v-for="note in accessibleNotes"
                 :key="note.id"
                 class="ma-2"
            >
              <v-card width="250"
                      class=""
                      elevation="0"
                      :to="'/note/link/' + note.link"
              >
                <v-card-text class="text-center">
                  <v-icon class="mb-4 my-5"
                          size="76"
                  >
                    mdi-file
                  </v-icon>
                  <div class="text-h5 text-truncate mb-3">
                    {{ note.title }}
                  </div>
                </v-card-text>
              </v-card>
            </div>
          </template>
          <div v-if="accessLoading"
               class="d-flex ga-2 ma-2"
          >
            <v-skeleton-loader v-for="_ in 4"
                               :key="_"
                               type="paragraph"
                               width="250"
            />
          </div>
          <h3 v-else-if="!accessibleNotes.length"
              class="d-flex ga-2 ma-2"
          >
            {{ $t('nothings_here') }}
          </h3>
        </v-row>
      </v-card-text>
    </v-card>
    <h1 class="text-green mb-2">
      {{ $t('templates') }}:
    </h1>
    <v-card class=" mb-5 rounded-lg"
            color="green"
            elevation="0"
    >
      <v-card-text>
        <v-row>
          <div v-if="!noteLoading"
               class="ma-2"
          >
            <v-card id="create-template"
                    width="300"
                    color="green-lighten-1"
                    elevation="0"
                    @click="createNewTemplate()"
            >
              <v-card-text class="text-center align-center d-flex ">
                <v-icon class=""
                        color="white"
                        size="30"
                >
                  mdi-file-document-plus-outline
                </v-icon>
                <div class="text-start ms-4 overflow-hidden">
                  <div class="text-body-1 text-white font-weight-bold">
                    {{ $t('new_template') }}
                  </div>
                </div>
              </v-card-text>
            </v-card>
          </div>
          <template v-if="!templateLoading">
            <div v-for="template in templates"
                 :key="template.id"
                 class="ma-2"
            >
              <v-card width="300"
                      class="template-card"
                      elevation="0"
                      :to="localePath(`/template/${template.id}`)"
              >
                <v-card-text class="text-center align-center d-flex ">
                  <v-icon class=""
                          color="green"
                          size="30"
                  >
                    mdi-file-document
                  </v-icon>
                  <div class="text-start ms-4 overflow-hidden">
                    <div class="text-body-1 text-truncate font-weight-bold">
                      {{ template.title }}
                    </div>
                  </div>
                </v-card-text>
              </v-card>
            </div>
          </template>
          <div v-if="templateLoading"
               class="d-flex ga-2 ma-2"
          >
            <v-skeleton-loader v-for="_ in 4"
                               :key="_"
                               type="paragraph"
                               width="250"
            />
          </div>
        </v-row>
      </v-card-text>
    </v-card>
    <h1 class="text-red mb-2">
      {{ $t('trash') }}:
    </h1>
    <v-card class=" mb-5 rounded-lg"
            color="red"
            elevation="0"
    >
      <v-card-text>
        <v-row>
          <template v-if="!trashLoading">
            <div v-for="note in trashNotes"
                 :key="note.id"
                 class="ma-2"
            >
              <v-card width="300"
                      class="trash-note-card"
                      elevation="0"
                      :to="localePath(`/note/${note.id}`)"
              >
                <v-card-text class="text-center py-3 align-center d-flex ">
                  <v-icon class=""
                          color="red"
                          size="30"
                  >
                    mdi-file
                  </v-icon>
                  <div class="text-start ms-4 overflow-hidden">
                    <div class="text-body-1 text-truncate font-weight-bold">
                      {{ note.title }}
                    </div>
                    <div class="text-caption text-grey ">
                      {{ $t('deleted_at') }} :
                      {{ new Date(note.deleted_at).toLocaleString(locale) }}
                    </div>
                  </div>
                </v-card-text>
              </v-card>
            </div>
          </template>
          <div v-if="trashLoading"
               class="d-flex ga-2 ma-2"
          >
            <v-skeleton-loader v-for="_ in 4"
                               :key="_"
                               type="paragraph"
                               width="250"
            />
          </div>
          <h3 v-else-if="!trashNotes.length"
              class="d-flex ga-2 ma-2"
          >
            {{ $t('nothings_here') }}
          </h3>
        </v-row>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { EventModelDefaultValue, type EventModel } from '~/composables/models/Event'

useHead(seoConfig('index_page_title'))
const { t, locale } = useI18n()
const localePath = useLocalePath()
const eventDialog = useState<boolean>('eventDialog', () => false)
const selectedEvent = useState<EventModel>('selectedEvent', () => {
  return { ...EventModelDefaultValue }
})
const viewMode = useState<'month' | 'day' | 'year'>('viewMode', () => 'month')
const showMode = useCookie<null | 'tasks' | 'calendar' | 'goals' | 'journeys'>('INDEX_SHOW_MODE')
showMode.value = showMode.value || 'tasks'
const { data: notes, error, pending: noteLoading } = await useAuthAPIFetch('/api/v1/note/', {
  server: false,
})
if (error.value) {
  console.log(error.value)
}
const { data: accessibleNotes, error: accessError, pending: accessLoading } = await useAuthAPIFetch('/api/v1/note/accessible_notes', {
  server: false,
})
if (accessError.value) {
  console.log(error.value)
}

const { data: templates, error: templateError, pending: templateLoading } = await useAuthAPIFetch('/api/v1/template', {
  server: false,
})
if (templateError.value) {
  console.log(error.value)
}
const { data: trashNotes, error: trashError, pending: trashLoading } = await useAuthAPIFetch('/api/v1/note/trash', {
  server: false,
})
if (trashError.value) {
  console.log(error.value)
}
const createNewNote = async () => {
  noteLoading.value = true
  const now = new Date()
  const { error, data } = await useAuthAPIFetch('/api/v1/note/', {
    method: 'POST',
    body: {
      title: t('untitled') + ` ${now.toLocaleDateString(locale.value)}_${now.toLocaleTimeString(locale.value)}`,
      editor_data: [{
        id: 'headeartitle',
        type: 'paragraph',
        data: {
          text: '',
        },
      }],
      editor_version: '2.0.6',
      editor_time: new Date().toLocaleString('en'),
    },
  })
  if (error.value) {
    throw createError({
      message: error.value.detail,
      statusCode: error.value.statusCode,
    })
  }
  else {
    navigateTo(localePath('/note/' + data.value.id))
  }
  noteLoading.value = false
}
const createNewTemplate = async () => {
  templateLoading.value = true
  const now = new Date()
  const { error, data } = await useAuthAPIFetch('/api/v1/template/', {
    method: 'POST',
    body: {
      title: t('template') + ` ${now.toLocaleDateString(locale.value)}_${now.toLocaleTimeString(locale.value)}`,
      editor_data: [{
        id: 'headeartitle',
        type: 'paragraph',
        data: {
          text: '',
        },
      }],
    },
  })
  if (error.value) {
    throw createError({
      message: error.value.detail,
      statusCode: error.value.statusCode,
    })
  }
  else {
    navigateTo(localePath('/template/' + data.value.id))
  }
  templateLoading.value = false
}
</script>

<style></style>

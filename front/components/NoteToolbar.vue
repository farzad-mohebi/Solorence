<template>
  <v-card elevation="0"
          class="d-flex align-center justify-space-between mb-5 px-3 py-2  border rounded-lg"
  >
    <div class="text-h6 my-2  d-flex align-center justify-space-between ">
      <div class="d-flex align-center justify-content-between">
        <div>
          <v-icon class="mb-1"
                  color="primary"
                  size="x-large"
          >
            mdi-account-circle
          </v-icon>
        </div>
        <div v-if="authStore.info"
             class="text-start ms-3"
        >
          <div class="text-caption text-primary">
            {{ $t('welcome') }},
          </div>
          <div class="text-uppercase mt-n1">
            {{ authStore.info.first_name }} {{
              authStore.info.last_name }}
          </div>
        </div>
      </div>
    </div>
    <div class="d-flex ga-4 align-center justify-center">
      <v-dialog v-model="dialog"
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
                   @click="dialog = false"
            >
              {{ $t('cancel') }}
            </v-btn>
            <v-btn id="id-note-delete"
                   variant="elevated"
                   color="red"
                   @click="removeNote"
            >
              {{ $t('yes_delete_it') }}
            </v-btn>
          </template>
        </v-card>
      </v-dialog>
      <v-dialog v-model="templateDialog"
                scrollable
                max-width="400"
      >
        <v-card title="select_template"
                :loading="templateLoading"
        >
          <template #prepend>
            <v-icon color="green"
                    icon="mdi-file-document"
            />
          </template>
          <v-divider class="mt-0" />
          <v-card-text class="px-4"
                       style="height: 300px;"
          >
            <v-radio-group v-model="selectedTemplate"
                           color="green"
                           column
            >
              <v-radio v-for="template in templates"
                       :key="template.id"
                       :label="template.title"
                       :value="template"
              />
            </v-radio-group>
          </v-card-text>

          <v-divider />

          <v-card-actions>
            <v-btn :text="$t('cancel')"
                   @click="templateDialog = false"
            />

            <v-spacer />

            <v-btn color="green"
                   :text="$t('add')"
                   variant="flat"
                   @click="addTemplateToNote()"
            />
          </v-card-actions>
        </v-card>
      </v-dialog>
      <div class="mt-2" />
      <LanguageChange />
      <NoteShare />
      <!-- <NoteAttachments></NoteAttachments> -->
      <NotificationBar />
      <v-btn
        icon
        variant="text"
        @click="toggleTheme"
      >
        <v-icon :icon="cookieTheme === 'dark' ? 'mdi-weather-sunny' : 'mdi-weather-night'" />
      </v-btn>
      <v-menu>
        <template #activator="{ props }">
          <v-btn id="id-show-note-toolbar"
                 icon="mdi-dots-vertical"
                 variant="text"
                 v-bind="props"
          />
        </template>

        <v-list class="less-prepend-space">
          <!-- <v-list-item @click="showNoteAttachments=true">
                        <template v-slot:prepend>
                            <v-icon>mdi-file-document-multiple-outline</v-icon>
                        </template>
                        <v-list-item-title>
                            {{ $t('attachments') }}
                        </v-list-item-title>
                    </v-list-item> -->
          <v-list-item @click="showTemplates">
            <template #prepend>
              <v-icon>mdi-file-document-plus-outline</v-icon>
            </template>
            <v-list-item-title>
              {{ $t('add_template') }}
            </v-list-item-title>
          </v-list-item>
          <v-list-item @click="showHistoryDialog">
            <template #prepend>
              <v-icon>mdi-history</v-icon>
            </template>
            <v-list-item-title>
              {{ $t('history') }}
            </v-list-item-title>
          </v-list-item>
          <v-list-item @click="duplicateNote">
            <template #prepend>
              <v-icon>mdi-content-duplicate</v-icon>
            </template>
            <v-list-item-title>
              {{ $t('duplicate_note') }}
            </v-list-item-title>
          </v-list-item>
          <v-list-item @click="exportNote">
            <template #prepend>
              <v-icon color="green">
                mdi-file-export-outline
              </v-icon>
            </template>
            <v-list-item-title class="text-green">
              {{ $t('export') }}
            </v-list-item-title>
          </v-list-item>
          <v-list-item @click="importFile = true">
            <template #prepend>
              <v-icon color="teal">
                mdi-file-import-outline
              </v-icon>
            </template>
            <v-list-item-title class="text-teal">
              {{ $t('import') }}
            </v-list-item-title>
          </v-list-item>
          <v-list-item @click="redoChanges">
            <template #prepend>
              <v-icon color="orange">
                mdi-redo
              </v-icon>
            </template>
            <v-list-item-title class="text-orange">
              {{ $t('revert_changes') }}
            </v-list-item-title>
          </v-list-item>
          <v-list-item id="id-show-note-delete"
                       @click="dialog = true"
          >
            <template #prepend>
              <v-icon color="red">
                mdi-delete
              </v-icon>
            </template>
            <v-list-item-title class="text-red">
              {{ $t('delete') }}
            </v-list-item-title>
          </v-list-item>
          <v-list-item>
            <template #prepend>
              <v-icon>mdi-cogs</v-icon>
            </template>
            <v-list-item-title>
              {{ $t('settings') }}
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-btn
        icon="mdi-home"
        :to="localePath('/home')"
        variant="text"
      />
    </div>

    <v-dialog v-model="historyDialog"
              scrollable
              max-width="800"
    >
      <v-card :title="$t('history')"
              :loading="historyLoading"
      >
        <template #prepend>
          <v-icon color="green"
                  icon="mdi-file-document"
          />
        </template>
        <v-divider class="mt-0" />
        <v-card-text v-if="!selectedHistory">
          <v-card v-for="history in noteHistories"
                  :key="history.time"
                  class="mb-2 bg-grey-lighten-5"
                  variant="flat"
                  @click="showHistory(history)"
          >
            <v-card-text class="d-flex align-center">
              <div>
                <h3 class="mb-2">
                  {{ history.title }}
                </h3>
                <div class="text-grey">
                  {{ new Date(history.time * 1000).toLocaleString(locale) }}
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-card-text>
        <v-card-text v-else>
          <v-card class="mb-2 bg-grey-lighten-5"
                  variant="flat"
          >
            <v-card-text class="d-flex align-center">
              <div>
                <h3 class="mb-2">
                  {{ selectedHistory.title }}
                </h3>
                <div class="text-grey">
                  {{ new Date(selectedHistory.time * 1000).toLocaleString(locale) }}
                </div>
                <div id="historyBlock"
                     class="text-grey"
                />
              </div>
            </v-card-text>
          </v-card>
        </v-card-text>

        <v-divider />

        <v-card-actions>
          <v-btn :text="selectedHistory ? $t('back') : $t('cancel')"
                 @click="selectedHistory ? selectedHistory = null : historyDialog = false;"
          />
          <v-btn :disabled="!selectedHistory"
                 variant="flat"
                 :text="$t('apply_to_new_note')"
                 color="green"
                 @click="applyNewNoteHistory"
          />
          <v-btn :disabled="!selectedHistory"
                 variant="flat"
                 :text="$t('revert_to_existing')"
                 color="red"
                 @click="revertHistoryDialog = true"
          />
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="revertHistoryDialog"
              width="auto"
              persistent
              max-width="400"
    >
      <v-card :loading="loading"
              max-width="400"
              prepend-icon="mdi-alert"
              :text="$t('revert_sure')"
              :title="$t('reverting') + '!'"
      >
        <template #actions>
          <v-spacer />
          <v-btn variant="plain"
                 @click="revertHistoryDialog = false"
          >
            {{ $t('cancel') }}
          </v-btn>
          <v-btn variant="elevated"
                 color="red"
                 @click="applyHistory"
          >
            {{ $t('yes_revert_it') }}
          </v-btn>
        </template>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script setup lang="ts">
import { useTheme } from 'vuetify'
import { useAuthStore } from '~/store/auth'
import { useUtilsStore } from '~/store/utils'
import type { Note, NoteHistory } from '~/composables/models/Note'
import type { ResponseOK } from '~/composables/models/Response.js'
import type { Template } from '~/composables/models/Template'

const importFile = ref<boolean>(false)
const theme = useTheme()
const cookieTheme = useCookie('theme')
theme.global.name.value = cookieTheme.value === 'dark' ? 'dark' : 'light'
const toggleTheme = () => {
  const cookieTheme = useCookie('theme')
  cookieTheme.value = cookieTheme.value === 'dark' ? 'light' : 'dark'
  theme.global.name.value = cookieTheme.value
}
const loading = ref<boolean>(false)
const { locale } = useI18n()
const utilStore = useUtilsStore()
const route = useRoute()
const dialog = ref(false)
const revertHistoryDialog = ref(false)
const localePath = useLocalePath()
const authStore = useAuthStore()
const emit = defineEmits(['revertNote', 'enableLoading', 'disableLoading', 'setNoteData', 'addBlocks', 'export'])
// const showNoteAttachments = useState('showNoteAttachments', () => false)

const removeNote = async () => {
  emit('enableLoading')
  const { error } = await useAuthAPIFetch(`/api/v1/note/${route.params.id}/`, {
    method: 'DELETE',
  })
  if (error.value) {
    utilStore.showApiError(error.value)
    emit('disableLoading')
  }
  else {
    utilStore.showSuccessMessage('deleted_successfully')
    navigateTo(localePath('/home'))
  }
}

const duplicateNote = async () => {
  emit('enableLoading')
  const { error, data } = await useAuthAPIFetch<Note>(`/api/v1/note/duplicate/${route.params.id}/`, {
    method: 'POST',
  })
  if (error.value) {
    utilStore.showApiError(error.value)
    emit('disableLoading')
  }
  else if (data.value) {
    utilStore.showSuccessMessage('duplicated_successfully')
    navigateTo(localePath('/note/' + data.value.id))
  }
}

const exportNote = () => {
  emit('export')
}

let editor
const noteHistories = ref<NoteHistory[]>([])
const historyDialog = ref<boolean>(false)
const selectedHistory = ref<NoteHistory | null>(null)
const historyLoading = ref<boolean>(false)

const applyHistory = async () => {
  const { error } = await useAuthAPIFetch<ResponseOK>(`/api/v1/note/set_history/${route.params.id}/`, {
    method: 'POST',
  })
  if (error.value) {
    utilStore.showApiError(error.value)
    emit('disableLoading')
  }
  else {
    revertHistoryDialog.value = false
    emit('setNoteData', selectedHistory.value)
    selectedHistory.value = null
    historyDialog.value = false
  }
}
const applyNewNoteHistory = async () => {
  if (!selectedHistory.value)
    return
  historyLoading.value = true
  const { error, data } = await useAuthAPIFetch<Note>(`/api/v1/note/`, {
    method: 'POST',
    body: {
      title: selectedHistory.value.title,
      editor_data: selectedHistory.value.blocks,
      editor_version: '2.30.6',
    },
  })
  if (error.value) {
    utilStore.showApiError(error.value)
    emit('disableLoading')
    historyLoading.value = false
  }
  else if (data.value) {
    selectedHistory.value = null
    historyDialog.value = false
    historyLoading.value = false
    navigateTo(localePath('/note/' + data.value.id))
  }
}
const showHistory = async (history: NoteHistory) => {
  historyLoading.value = true
  console.log('showHistory', history.title)
  selectedHistory.value = {
    blocks: history.blocks,
    title: history.title,
    time: history.time,
  }
  const { $editorjs } = useNuxtApp()
  editor = $editorjs('historyBlock', {
    locale: locale.value,
    readOnly: true,
  })
  await editor.isReady
  editor.blocks.render({
    blocks: history.blocks,
  })
  historyLoading.value = false
}
const showHistoryDialog = async () => {
  historyLoading.value = true
  emit('enableLoading')
  const { error, data } = await useAuthAPIFetch<NoteHistory[]>(`/api/v1/note/history/${route.params.id}/`)
  if (error.value) {
    utilStore.showApiError(error.value)
    emit('disableLoading')
  }
  else if (data.value) {
    emit('disableLoading')
    noteHistories.value = data.value
    historyDialog.value = true
  }
  historyLoading.value = false
}
const redoChanges = async () => {
  emit('revertNote')
}

const templateDialog = ref(false)
const templates = ref<Template[]>([])
const selectedTemplate = ref<Template | null>()
const templateLoading = ref(false)
const showTemplates = async () => {
  templateLoading.value = true
  const { data: temps, error: templateError } = await useAuthAPIFetch<Template[]>('/api/v1/template', {
    server: false,
  })
  if (templateError.value) {
    utilStore.showApiError(templateError.value)
  }
  else if (temps.value) {
    templateDialog.value = true
    templates.value = temps.value
  }
  templateLoading.value = false
}
const addTemplateToNote = () => {
  if (selectedTemplate.value) {
    emit('addBlocks', selectedTemplate.value.editor_data)
    templateDialog.value = false
  }
}
</script>

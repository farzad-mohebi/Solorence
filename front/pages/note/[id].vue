<template>
  <div>
    <TaskManager />
    <v-container max-width="1340">
      <NoteToolbar @revert-note="revertNote"
                   @add-blocks="addBlocksToNote"
                   @set-note-data="setNoteData"
                   @enable-loading="loading = true"
                   @disable-loading="loading = false"
                   @export="exportNoteInfo"
      />
      <v-card color="transparent"
              :disabled="loading || noteLoading"
              :loading="loading || noteLoading"
              elevation="0"
      >
        <template #loader="{ isActive }">
          <v-progress-linear :active="isActive"
                             color="primary"
                             height="4"
                             indeterminate
          />
        </template>
        <v-form ref="form">
          <v-card-text>
            <v-text-field v-model="title"
                          :rules="FormRules.notEmpty"
                          variant="underlined"
                          :placeholder="$t('note_title')"
            />
            <div class="py-10 bg-white justify-center align-center flex-column"
                 :class="[loading ? 'd-flex' : 'd-none']"
            >
              <v-skeleton-loader width="700"
                                 type="article"
              />
              <v-skeleton-loader class="mt-3"
                                 width="700"
                                 type="paragraph"
              />
            </div>
            <div id="editorjs"
                 :class="[loading ? 'd-none' : 'mt-5']"
            />
          </v-card-text>
        </v-form>
      </v-card>
    </v-container>
    <NotePageDialog />
    <EditorWhiteBoard />
    <MentionMenu @add-mention="addMention" />
  </div>
</template>

<script setup lang="ts">
import type { OutputBlockData, OutputData } from '@editorjs/editorjs'
import type EditorJS from '@editorjs/editorjs'
import { onMounted } from 'vue'
import { type EditorData, EditorDataDefaultValue } from '~/composables/models/EditorData.js'
import type { Note, NoteHistory } from '~/composables/models/Note.js'
import { useUtilsStore } from '~/store/utils'
import { FormRules } from '~/composables/FormRules'
import { downloadJsonFile } from '~/composables/custom_functions.js'

const { locale } = useI18n()
const utilStore = useUtilsStore()
const route = useRoute()
const loading = ref<boolean>(true)
const noteLoading = useState<boolean>('noteLoading', () => false)
const title = ref<string>('')
const loadedTitle = ref<string>('')
const dbTitle = ref<string>('')
const unChangedBlocks = ref<EditorData>({ ...EditorDataDefaultValue })
const form = ref() // Auto Find Form ref
const editorData = ref<EditorData>({ ...EditorDataDefaultValue })

const { error, data } = await useAuthAPIFetch<Note>(`/api/v1/note/${route.params.id}`, {
  method: 'GET',
})
if (error.value) {
  throw createError({
    message: 'This note is unavailable!',
    statusCode: 404,
  })
}
if (data.value) {
  title.value = data.value.title
  useHead(seoConfig(title.value))
  dbTitle.value = data.value.title
  loadedTitle.value = data.value.title
  editorData.value.blocks = data.value.editor_data
  editorData.value.time = new Date().getTime()
  unChangedBlocks.value = editorData.value
}
const save = async (content: OutputData) => {
  const formValidation = await form.value?.validate()
  if (!formValidation?.valid) return
  const { error, data } = await useAuthAPIFetch<Note>(`/api/v1/note/${route.params.id}/`, {
    method: 'PUT',
    body: {
      title: title.value,
      editor_data: content.blocks,
      editor_version: content.version,
      editor_time: (content.time || new Date()).toLocaleString('en'),
    },
  })
  if (data.value)
    dbTitle.value = data.value.title
  if (error.value) {
    utilStore.showApiError(error.value)
  }
}

let editor: EditorJS
let tempData: OutputData = {
  blocks: [],
}

onMounted(async () => {
  const { $editorjs } = useNuxtApp()
  editor = $editorjs('editorjs', {
    saveInGoogleCalendar: saveInGoogleCalendar,
    // createMeet: getGoogleMeetLink,
    showPage: showPage,
    showShareBlock: showShareBlock,
    locale: locale.value,
    showCreateTask: showCreateTask,
    showTask: showTask,
    uploadFile: uploadFile,
    showCreateMeet: showCreateMeet,
    showMeet: showMeet,
    showBoard: showBoard,
  })
  await editor.isReady
  loading.value = false
  editor.blocks.render({
    blocks: editorData.value.blocks,
  })
  setInterval(() => {
    editor.save().then((outputData) => {
      outputData.blocks = getCleanBlockData(outputData.blocks)
      if (dbTitle.value !== title.value) { // Title Changed
        console.log('Title Changed', dbTitle.value !== title.value)
        save(outputData)
      }
      else if (tempData && !deepEqual(tempData.blocks, outputData.blocks)) { // Blocks Changed
        console.log('Blocks Changed', tempData && !deepEqual(tempData.blocks, outputData.blocks))
        save(outputData)
      }
      tempData = outputData
    })
  }, 3000)
  setupMentionListener()
})

const revertNote = () => {
  editor.blocks.render({
    blocks: unChangedBlocks.value.blocks,
  })
  title.value = loadedTitle.value
  utilStore.showSuccessMessage('note_reverted_successfully')
}

const setNoteData = (noteData: NoteHistory) => {
  editor.blocks.render({
    blocks: noteData.blocks,
  })
  title.value = noteData.title
  utilStore.showSuccessMessage('history_applied_successfully')
}

const addBlocksToNote = (blocks: OutputBlockData[]) => {
  editor.save().then((outputData) => {
    editor.blocks.render({
      blocks: [...outputData.blocks, ...blocks],
    })
  })
}

const exportNoteInfo = () => {
  loading.value = true
  editor.save().then((outputData) => {
    downloadJsonFile(outputData, title.value + '.json')
    setTimeout(() => {
      loading.value = false
    }, 500)
  })
}

definePageMeta({
  layout: 'note',
})
</script>
<!-- <script>
window.onbeforeunload = confirmExit;
function confirmExit() {
    return "Some task is in progress. Are you sure, you want to close?";
}
</script> -->

<style>
.left-overly-editor .v-overlay__content {
    padding-left: 15px;
    padding-top: -30px;
}

mark:not(.cdx-marker) {
    background: #795548;
    color: #fff;
    padding: 3px 7px;
    margin: 0 5px;
    border-radius: 5px;
}
</style>

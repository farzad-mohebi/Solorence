<template>
  <div>
    <v-container max-width="1340">
      <TemplateToolbar @revert-template="revertTemplate"
                       @enable-loading="loading = true"
                       @disable-loading="loading = false"
      />
      <v-card color="transparent"
              :disabled="loading || cardLoading"
              :loading="loading || cardLoading"
              elevation="0"
      >
        <template #loader="{ isActive }">
          <v-progress-linear :active="isActive"
                             color="primary"
                             height="4"
                             indeterminate
          />
        </template>
        <v-form ref="form"
                @submit.prevent="saveContent"
        >
          <v-card-text>
            <v-text-field v-model="title"
                          :rules="FormRules.notEmpty"
                          variant="underlined"
                          :placeholder="$t('template_title')"
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
          <v-card-actions />
        </v-form>
      </v-card>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import type { OutputData } from '@editorjs/editorjs'
import type EditorJS from '@editorjs/editorjs'

import { useUtilsStore } from '~/store/utils'
import type { Template } from '~/composables/models/Template.js'
import { type EditorData, EditorDataDefaultValue } from '~/composables/models/EditorData.js'
import { FormRules } from '~/composables/FormRules'

const utilStore = useUtilsStore()
const route = useRoute()
const loading = ref<boolean>(true)
const cardLoading = ref<boolean>(false)
const title = ref<string>('')
const loadedTitle = ref<string>('')
const dbTitle = ref<string>('')
const unChangedBlocks = ref<EditorData>({ ...EditorDataDefaultValue })
const form = ref() // Auto Find Form ref
const editorData = ref<EditorData>({ ...EditorDataDefaultValue })

const { error, data } = await useAuthAPIFetch<Template>(`/api/v1/template/${route.params.id}`, {
  method: 'GET',
})
if (error.value) {
  throw createError({
    message: 'This template is unavailable!',
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
  if (!formValidation.valid) return

  const { error, data } = await useAuthAPIFetch<Template>(`/api/v1/template/${route.params.id}/`, {
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
  else {
    // utilStore.showSuccessMessage();
    // navigateTo(localePath('/'))
  }
}
const saveContent = () => {
  editor.save().then((outputData: OutputData) => {
    console.log('Article data:', outputData)
    save(outputData)
  }).catch((error: any) => {
    console.log('Saving failed: ', error)
    utilStore.showErrorMessage()
  })
}

const { locale } = useI18n()
let editor: EditorJS

onMounted(async () => {
  const { $editorjs } = useNuxtApp()
  editor = $editorjs('editorjs', {
    locale: locale.value,
    hide: ['meet', 'task'],
  })
  await editor.isReady
  loading.value = false
  if (editorData.value.blocks && editorData.value.blocks.length > 0)
    editor.blocks.render({
      blocks: editorData.value.blocks,
    })
  let tempData: OutputData = {
    blocks: [],
  }
  setInterval(() => {
    editor.save().then((outputData: OutputData) => {
      if (dbTitle.value !== title.value) { // Title Changed
        save(outputData)
      }
      else if (tempData && !deepEqual(tempData.blocks, outputData.blocks)) { // Blocks Changed
        save(outputData)
      }
      tempData = outputData
    })
  }, 3000)
})
const revertTemplate = () => {
  if (unChangedBlocks.value.blocks)
    editor.blocks.render({
      blocks: unChangedBlocks.value.blocks,
    })
  title.value = loadedTitle.value
  utilStore.showSuccessMessage('template_reverted_successfully')
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

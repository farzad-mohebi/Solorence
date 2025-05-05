<template>
  <div>
    <v-card v-if="hasAccess"
            color="transparent"
            :disabled="loading || cardLoading"
            :class="[data.access === 3 ? '' : 'viewer-content']"
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
      <v-form ref="form">
        <v-card-text>
          <template v-if="data.access === 3">
            <v-text-field v-model="title"
                          class="mb-4"
                          :rules="FormRules.notEmpty"
                          variant="outlined"
                          label="Note name"
            />
            <div class="mb-2 text-body-1">
              {{ $t('rule') }}:
              <span class="text-primary font-weight-bold text-uppercase">
                {{ $t('access_type_' + data.access) }}
              </span>
            </div>
          </template>
          <template v-else>
            <h1 class="mb-2">
              {{ title }}
            </h1>
            <p class="pb-2">
              <v-icon size="small">
                mdi-calendar-clock
              </v-icon>
              <strong> Last Update: </strong>
              {{ stringifyDatetime(data.updated_at) }}
            </p>
          </template>
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
          <div class="mt-5 d-flex justify-space-between">
            <div>
              <v-btn v-if="data.access === 3"
                     class="me-2"
                     variant="elevated"
                     color="primary"
                     type="submit"
              >
                {{ $t('update') }}
              </v-btn>
              <!-- <v-btn class="me-2" :to="localePath('/')">{{ $t('back') }}</v-btn> -->
            </div>
          </div>
        </v-card-text>
        <v-card-actions />
      </v-form>
    </v-card>
    <NoteRequestAccess v-else />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '~/store/auth'
import { FormRules } from '~/composables/FormRules'

const { locale } = useI18n()
const authStore = useAuthStore()
const route = useRoute()
const hasAccess = ref<boolean>(false)
const isRequestSent = useState<boolean>('isRequestSent', () => false)
definePageMeta({
  layout: 'guest',
})
const data = ref({})
if (!authStore.isAuthenticated) {
  const { error, data: result } = await useAPIFetch(`/api/v1/note/get_data/${route.params.link}/`, {
    method: 'GET',
  })
  if (error.value) {
    throw createError({
      message: error.value?.data?.detail,
      statusCode: error.value.statusCode,
    })
  }
  else if (result.value) {
    data.value = result.value
    hasAccess.value = true
  }
}
else {
  const { error, data: result } = await useAuthAPIFetch(`/api/v1/note/get_data/${route.params.link}/`, {
    method: 'GET',
  })
  if (error.value) {
    throw createError({
      message: error.value?.data?.detail,
      statusCode: 404,
    })
  }
  console.log('result.value', result.value)
  if (result.value.access) {
    hasAccess.value = true
  }
  else {
    isRequestSent.value = result.value.request_sent
    hasAccess.value = false
  }
  data.value = result.value
}

const loading = ref(true)
const cardLoading = ref(false)
const title = ref('')
const form = ref(null) // Auto Find Form ref
const editorData = ref({
  blocks: [],
  time: new Date().getTime(),
  version: '2.30.6',
})
title.value = data.value.title
useHead(seoConfig(title.value))
editorData.value.blocks = data.value.editor_data
editorData.value.time = new Date(data.value.editor_time).getTime()
editorData.value.version = data.value.editor_version

// const save = async (content: OutputData) => {
//   const formValidation = await form.value?.validate()
//   if (!formValidation.valid) return
//   if (!valid) return

//   const { error } = await useAuthAPIFetch(`/api/v1/note/update_other_note/${data.value.id}/`, {
//     method: 'PUT',
//     body: {
//       title: title.value,
//       editor_data: content.blocks,
//       editor_version: content.version,
//       editor_time: new Date(content.time).toLocaleString('en'),
//     },
//   })
//   if (error.value) {
//     utilStore.showApiError(error.value)
//   }
//   else {
//     utilStore.showSuccessMessage()
//     navigateTo(localePath('/'))
//   }
// }
let editor: EditorJS

const scrollToBlock = route?.hash
onMounted(async () => {
  if (hasAccess.value) {
    const { $editorjs } = useNuxtApp()
    editor = $editorjs('editorjs', {
      saveInGoogleCalendar: saveInGoogleCalendar,
      // createMeet: getGoogleMeetLink,
      locale: locale.value,
      readOnly: data?.value?.access !== 3,
    })
    await editor.isReady
    if (editorData.value.blocks)
      await editor.blocks.render({
        blocks: editorData.value.blocks,
      })
    loading.value = false
    if (scrollToBlock) {
      setTimeout(() => {
        const scrollBlock = document.querySelector(`.ce-block[data-id="${scrollToBlock.replace('#', '')}"]`)
        scrollBlock.scrollIntoView({
          behavior: 'smooth',
        })
        scrollBlock.style.transition = '1s all ease-in'
        scrollBlock.classList.add('bg-brown-lighten-4')
        setTimeout(() => {
          scrollBlock.classList.remove('bg-brown-lighten-4')
        }, 3000)
      }, 500)
    }
  }
  else {
    loading.value = false
  }
})
</script>

<style>
.codex-editor__redactor {
    padding-top: 50px !important;
    border-radius: 4px;
    overflow: visible;
    width: 100%;
}

@media (min-width: 768px) {

    .viewer-content .ce-block__content,
    .viewer-content .ce-toolbar__content {
        max-width: 100% !important;
    }
}

.viewer-content .codex-editor__redactor {
    padding: 0 !important;
}
</style>

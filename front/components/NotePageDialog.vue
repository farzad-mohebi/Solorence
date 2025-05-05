<template>
  <div>
    <v-dialog v-model="pageData.show"
              max-width="1300"
              persistent
    >
      <v-card :loading="pageLoading"
              min-height="700px"
      >
        <template #loader="{ isActive }">
          <v-progress-linear :active="isActive"
                             color="green"
                             height="4"
                             indeterminate
          />
        </template>
        <v-form ref="pageForm">
          <v-card-text>
            <div class="d-flex align-center">
              <v-text-field v-model="pageData.title"
                            :rules="FormRules.notEmpty"
                            variant="underlined"
                            :placeholder="$t('page_title')"
              />
              <v-btn class="ms-2 mb-2"
                     variant="flat"
                     color="red"
                     @click="revertDialog = true"
              >
                {{ $t('revert_changes') }}
              </v-btn>
              <v-btn class="ms-2 mb-2"
                     variant="flat"
                     color="green"
                     @click="closePageDialog"
              >
                {{ $t('done') }}
              </v-btn>
            </div>
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
            <div id="pageEditor"
                 :class="[loading ? 'd-none' : '']"
            />
          </v-card-text>
        </v-form>
      </v-card>
    </v-dialog>

    <v-dialog v-model="revertDialog"
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
                 @click="revertDialog = false"
          >
            {{ $t('cancel') }}
          </v-btn>
          <v-btn variant="elevated"
                 color="red"
                 @click="revertChanges()"
          >
            {{ $t('yes_revert_it') }}
          </v-btn>
        </template>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { useUtilsStore } from '~/store/utils'
import { FormRules } from '~/composables/FormRules'

const utilStore = useUtilsStore()
const { t, locale } = useI18n()

const pageData = useState('showPageDialog', () => {
  return {
    show: false,
    uid: '',
    title: '',
    blocks: [],
  }
})
const pageLoading = ref(false)
const revertDialog = ref(false)
const initData = ref()
const closePageDialog = () => {
  pageLoading.value = true
  setTimeout(() => {
    pageLoading.value = false
    pageData.value.show = false
  }, 500)
}

const showPage = computed(() => {
  return pageData.value.show
})

let interval
watch(showPage, () => {
  if (pageData.value.show) {
    loadPageEditor()
  }
  else {
    clearInterval(interval)
  }
})

let editor
const lastUpdate = {}
const loadPageEditor = async () => {
  console.log('loadPageEditor', pageData.value)

  pageLoading.value = true
  const { $editorjs } = useNuxtApp()
  editor = $editorjs('pageEditor', {
    saveInGoogleCalendar: saveInGoogleCalendar,
    // createMeet: getGoogleMeetLink,
    showShareBlock: showShareBlock,
    locale: locale.value,
    showCreateTask: showCreateTask,
    showTask: showTask,
    uploadFile: uploadFile,
    showCreateMeet: showCreateMeet,
    showMeet: showMeet,
  })
  await editor.isReady
  editor.blocks.render({
    blocks: pageData.value.blocks,
  })
  interval = setInterval(() => {
    editor.save().then((outputData) => {
      if (lastUpdate.title != pageData.value.title || !deepEqual(lastUpdate.blocks, outputData.blocks))
        window['changePageData_' + pageData.value.uid](pageData.value.title || t('untitled'), outputData.blocks || [])
      lastUpdate.title = pageData.value.title
      lastUpdate.blocks = outputData.blocks
    })
  }, 500)
  pageLoading.value = false
  initData.value = { ...pageData.value }
}
const revertChanges = async () => {
  pageLoading.value = true
  editor.blocks.render({
    blocks: initData.value.blocks,
  })
  pageData.value.title = initData.value.title
  setTimeout(() => {
    pageLoading.value = false
    revertDialog.value = false
    utilStore.showSuccessMessage('reverted_successfully')
  }, 500)
}
</script>

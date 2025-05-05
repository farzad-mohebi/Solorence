<template>
  <div>
    <v-dialog v-model="boardData.show"
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
              <v-text-field v-model="boardData.title"
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
            <div ref="excalidraw"
                 :class="[loading ? 'd-none' : '']"
                 classe="excalidraw"
            >
              Loading...
            </div>
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

<script setup lang="ts">
import type { ExcalidrawElement } from '@excalidraw/excalidraw/types/element/types'
import { onUnmounted, ref } from 'vue'
import { FormRules } from '~/composables/FormRules'
import { defaultBoardData, type BoardData } from '~/composables/models/EditorData'
import { useUtilsStore } from '~/store/utils'

const loading = ref<boolean>(false)

const excalidraw = ref(null) // Element of exiclDraw

let drawer: any

onUnmounted(() => {
  if (drawer) {
    drawer.unmount()
  }
})

const utilStore = useUtilsStore()
const { t } = useI18n()

const boardData = useState<BoardData>('boardData', () => {
  return { ...defaultBoardData }
})
const startBoardData = ref<BoardData>({ ...defaultBoardData })
const pageLoading = ref<boolean>(false)
const revertDialog = ref(false)
const initData = ref()
const closePageDialog = () => {
  pageLoading.value = true
  setTimeout(() => {
    pageLoading.value = false
    boardData.value.show = false
  }, 500)
}

const showPage = computed(() => {
  return boardData.value.show
})

let interval: ReturnType<typeof setInterval>
watch(showPage, () => {
  if (boardData.value.show) {
    loadPageEditor()
  }
  else {
    clearInterval(interval)
  }
})

const loadPageEditor = async () => {
  console.log('loadPageEditor', boardData.value)

  pageLoading.value = true
  // @ts-expect-error this is node modules
  const { createRoot } = await import('react-dom/client')
  // @ts-expect-error this is node modules
  const React = await import('react')
  const { Excalidraw } = await import('@excalidraw/excalidraw')

  drawer = createRoot(excalidraw.value)
  drawer.render(React.createElement(Excalidraw, {
    // props
    initialData: {
      elements: boardData.value?.elements || [],
    },
    onChange: (excalidrawElements: ExcalidrawElement[]) => {
      boardData.value.elements = excalidrawElements
    },

  }),
  )
  interval = setInterval(() => {
    // @ts-expect-error: 'changeBoardData_UID' is not typed on the Window object
    window['changeBoardData_' + boardData.value.uid](boardData.value.title || t('untitled'), boardData.value.elements || [])
  }, 500)
  pageLoading.value = false
  initData.value = { ...boardData.value }
}
const revertChanges = async () => {
  console.log('soon...', startBoardData.value)
  // pageLoading.value = true
  // editor.elements.render({
  //   elements: initData.value.elements,
  // })
  // boardData.value.title = initData.value.title
  // setTimeout(() => {
  //   pageLoading.value = false
  //   revertDialog.value = false
  utilStore.showSuccessMessage('reverted_successfully')
  // }, 500)
}
</script>

<style>
  .excalidraw {
    height: 100%;
    width: 100%;
    min-height: 650px;
  }
  .excalidraw.excalidraw-modal-container{
    z-index: 100000 !important;
  }
  .excalidraw .Stack.Stack_vertical.App-menu_top__left > div > div > div > div.dropdown-menu-group,
  .excalidraw .Stack.Stack_vertical.App-menu_top__left > div > div > div > div:nth-child(8){
    display: none;
  }
</style>

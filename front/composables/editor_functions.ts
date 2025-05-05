import type { OutputBlockData, OutputData } from '@editorjs/editorjs'
import type { ExcalidrawElement } from '@excalidraw/excalidraw/types/element/types'
import type { NoteAttachment, NoteSecurityConfig } from './models/Note'
import { EventModelDefaultValue, type EventModel, type GoogleCalendarMeet } from './models/Event'
import { defaultBoardData, type BoardData } from './models/EditorData'
import { useAuthStore } from '~/store/auth'
import { useUtilsStore } from '~/store/utils'

export const uploadFile = async (file: File) => {
  const route = useRoute()
  const formData = new FormData()
  formData.append('image', file)
  if (route.params.id) formData.append('note', route.params.id.toString())
  const { data } = await useAuthAPIFetch<NoteAttachment>('/api/v1/noteattachment/', {
    method: 'POST',
    body: formData,
  })
  if (data.value) {
    return {
      success: 1,
      file: {
        id: data.value.id,
        url: data.value.image,
        name: file.name,
        size: file.size,
        title: file.name,
      },
    }
  }
  else {
    return {
      success: 0,
    }
  }
}

export const saveInGoogleCalendar = async (meetData: GoogleCalendarMeet) => {
  const utilStore = useUtilsStore()
  const authStore = useAuthStore()
  const noteLoading = useState('mentionMenuTarget', () => false)
  noteLoading.value = true
  if (!authStore.getGoogleAccessToken) {
    return authStore.askGoogleToken()
  }
  const { error, data } = await useAuthAPIFetch(
    `/api/v1/google/create-event/`,
    {
      method: 'POST',
      body: {
        ...meetData,
        google_access_token: authStore.getGoogleAccessToken,
      },
    },
  )
  noteLoading.value = false
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else {
    utilStore.showSuccessMessage('schedule_google_calendar_successfully')
    return data.value
  }
}

// export const getGoogleMeetLink = async () => {
//   const utilStore = useUtilsStore()
//   const { error, data } = await useAuthAPIFetch('/api/v1/google/create-meet/', {
//     method: 'POST',
//   })
//   if (error.value || !data.value?.meeting_link)
//     utilStore.showApiError(error.value)
//   else return data.value.meeting_link
// }

export const showShareBlock = async (blockID: string) => {
  const route = useRoute()
  const utilStore = useUtilsStore()
  const { error, data } = await useAuthAPIFetch<NoteSecurityConfig>(
    `/api/v1/note/config/${route.params.id}`,
    {
      method: 'GET',
    },
  )
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else if (data.value) {
    utilStore.copyText(
      location.origin + '/note/link/' + data.value.link + '#' + blockID,
    )
  }
}
export const setupMentionListener = () => {
  const prevChar = useState('prevChar', () => null)
  const currentAnchor = useState<number | null>('currentAnchor', () => null)
  const selectedElement = useState<Element | null>('selectedElement', () => null)
  const selectedNode = useState<Node | null>('selectedNode', () => null)

  const mentionMenuTarget = useState('mentionMenuTarget', () => null)
  const mentionMenuShow = useState('mentionMenuShow', () => null)
  document.getElementById('editorjs')?.addEventListener('focusin', function () {
    selectedElement.value = document.activeElement
    selectedElement.value?.addEventListener('keydown', function (e: Event) {
      const selectedDocument = document.getSelection()
      if (selectedDocument) {
        currentAnchor.value = selectedDocument.anchorOffset
        selectedNode.value = selectedDocument.anchorNode
      }
      if (selectedNode.value && selectedNode.value.data) {
        prevChar.value = selectedNode.value.data[currentAnchor.value - 1]
      }
      else {
        prevChar.value = document.activeElement.innerText[currentAnchor.value - 1]
        selectedNode.value = null
      }
      if (e.key === '@' && (!prevChar.value || prevChar.value === ' ' || prevChar.value === ' ')) {
        e.preventDefault()
        mentionMenuTarget.value = selectedElement.value
        mentionMenuShow.value = true
      }
      else if (e.key === '@') {
        console.log('invalid', prevChar.value)
      }
    })
  })
}
export const getCleanBlockData = (blocks: OutputBlockData[]) => {
  return blocks.filter((block: OutputBlockData) => {
    if (block.type === 'mention' && !block?.data?.uid) {
      return false
    }
    if (block.type === 'meet' && !block?.data?.uid) {
      return false
    }
    if (block.type === 'task' && !block?.data?.uid) {
      return false
    }
    return true
  })
}

export const showCreateMeet = async () => {
  const meetDialog = useState('meetDialog', () => false)
  meetDialog.value = true
}
export const showMeet = async (meetID: number) => {
  const meetDialog = useState('meetDialog', () => false)
  const selectedEvent = useState<EventModel>('selectedEvent', () => {
    return { ...EventModelDefaultValue }
  })
  selectedEvent.value = { ...EventModelDefaultValue }
  selectedEvent.value.id = meetID
  meetDialog.value = true
}

export const showPage = (uid: string, title: string, pageEditorData: any) => {
  const pageData = useState('showPageDialog', () => {
    return {
      show: false,
      uid: '',
      title: '',
      blocks: [],
    }
  })
  pageData.value.uid = uid
  pageData.value.title = title
  pageData.value.blocks = pageEditorData
  pageData.value.show = true
}
export const showBoard = (uid: string, title: string, boardElements: ExcalidrawElement[]) => {
  const boardData = useState<BoardData>('boardData', () => {
    return { ...defaultBoardData }
  })
  boardData.value.uid = uid
  boardData.value.title = title
  boardData.value.elements = boardElements
  boardData.value.show = true
}

export const showCreateTask = async () => {
  const taskDialog = useState('taskDialog', () => false)
  taskDialog.value = true
}
export const showTask = async (taskID) => {
  const taskDialog = useState('taskDialog', () => false)
  const selectedTask = useState('selectedTask', () => {
    return {}
  })
  selectedTask.value = { id: taskID }
  taskDialog.value = true
}

export const placeIcon = {
  0: `<i style="width: 32px;" class="mdi-laptop-account text-blue mdi v-icon notranslate v-theme--light v-icon--size-x-large" aria-hidden="true" density="default"></i>`,
  1: `<svg style="width: 32px;" xmlns="http://www.w3.org/2000/svg" aria-label="Google Meet" role="img" viewBox="0 0 512 512"><rect width="512" height="512" rx="15%" fill="#ffffff"/><path d="M166 106v90h-90" fill="#ea4335"/><path d="M166 106v90h120v62l90-73v-49q0-30-30-30" fill="#ffba00"/><path d="M164 406v-90h122v-60l90 71v49q0 30-30 30" fill="#00ac47"/><path d="M286 256l90-73v146" fill="#00832d"/><path d="M376 183l42-34c9-7 18-7 18 7v200c0 14-9 14-18 7l-42-34" fill="#00ac47"/><path d="M76 314v62q0 30 30 30h60v-92" fill="#0066da"/><path d="M76 196h90v120h-90" fill="#2684fc"/></svg>`,
  2: `<svg style="width: 32px;" xmlns="http://www.w3.org/2000/svg" height="45" viewBox="0 0 472.4 472.4" width="45"><circle cx="236.2" cy="236.2" fill="#4a8cff" r="236.2"/><path d="m84.65 162.25v111a45.42 45.42 0 0 0 45.6 45.2h161.8a8.26 8.26 0 0 0 8.3-8.2v-111a45.42 45.42 0 0 0 -45.6-45.2h-161.75a8.26 8.26 0 0 0 -8.35 8.2zm226 43.3 66.8-48.8c5.8-4.81 10.3-3.6 10.3 5.1v148.8c0 9.9-5.5 8.7-10.3 5.09l-66.8-48.69z" fill="#fff"/><script xmlns=""/></svg>`,
  3: `<i style="width: 32px;" class="mdi-map-marker text-blue mdi v-icon notranslate v-theme--light v-icon--size-x-large" aria-hidden="true" density="default"></i>`,
  4: `<i style="width: 32px;" class="mdi-link mdi text-blue v-icon notranslate v-theme--light v-icon--size-x-large" aria-hidden="true" density="default"></i>`,
}

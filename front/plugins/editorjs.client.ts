import EditorJS from '@editorjs/editorjs'
import Header from '@editorjs/header'
import Checklist from '@editorjs/checklist'
import LinkTool from '@editorjs/link'
import RawTool from '@editorjs/raw'
import ImageTool from '@editorjs/image'
import Quote from '@editorjs/quote'
import Embed from '@editorjs/embed'
import Table from '@editorjs/table'
import Marker from '@editorjs/marker'
import Delimiter from '@editorjs/delimiter'
import Underline from '@editorjs/underline'
import NestedList from '@editorjs/nested-list'
import Warning from '@editorjs/warning'
import InlineCode from '@editorjs/inline-code'
import AttachesTool from '@editorjs/attaches'
import Meet from './editor_classes/meet.js'
import Share from './editor_classes/share-tool.js'
import Task from './editor_classes/task-tool.js'
import { editorMessages } from './editor_classes/tools-i18n.js'
import EditorPage from './editor_classes/editor-page.js'
import BoardPage from './editor_classes/board-page.js'
import type { EditorJSFunctions } from '~/composables/models/EditorData'

export default defineNuxtPlugin((nx) => {
  nx.provide('editorjs', (selector: string, nuxtApp: EditorJSFunctions = {}): EditorJS => {
    const tools: { [key: string]: object } = {
      image: {
        class: ImageTool,
        config: {
          uploader: {
            uploadByFile: nuxtApp.uploadFile,
          },
        },
      },
      attaches: {
        class: AttachesTool,
        config: {
          uploader: {
            uploadByFile: nuxtApp.uploadFile,
          },
        },
      },
      board: {
        class: BoardPage,
        config: {
          nuxtApp: nuxtApp,
        },
      },
      page: {
        class: EditorPage,
        config: {
          nuxtApp: nuxtApp,
        },
      },
      meet: {
        class: Meet,
        config: {
          nuxtApp: nuxtApp,
        },
      },
      header: Header,
      list: {
        class: NestedList,
        inlineToolbar: true,
        config: {
          defaultStyle: 'ordered',
        },
      },
      checklist: {
        class: Checklist,
        inlineToolbar: true,
      },
      linkTool: {
        class: LinkTool,
        config: {
          endpoint: 'http://localhost:8008/fetchUrl', // Your backend endpoint for url data fetching,
        },
      },
      raw: RawTool,
      quote: Quote,
      table: Table,
      Marker: {
        class: Marker,
        shortcut: 'CMD+SHIFT+M',
      },
      delimiter: Delimiter,
      share: {
        class: Share,
        config: {
          nuxtApp: nuxtApp,
        },
      },
      task: {
        class: Task,
        config: {
          nuxtApp: nuxtApp,
        },
      },
      underline: Underline,
      inlineCode: {
        class: InlineCode,
        shortcut: 'CMD+SHIFT+M',
      },
      warning: {
        class: Warning,
        inlineToolbar: true,
        shortcut: 'CMD+SHIFT+W',
        config: {
          titlePlaceholder: 'Title',
          messagePlaceholder: 'Message',
        },
      },
      embed: {
        class: Embed,
        config: {
          services: {
            youtube: true,
            coub: true,
          },
        },
      },
    }
    if (nuxtApp.hide) for (const key of nuxtApp.hide) if (tools && tools[key]) delete tools[key]

    const editor = new EditorJS({
      readOnly: nuxtApp.readOnly,
      holder: selector,
      placeholder: editorMessages[nuxtApp.locale || 'en'].placeholder,
      tools: tools,
      i18n: {
        direction: nuxtApp.locale === 'fa' ? 'rtl' : 'ltr',
        messages: editorMessages[nuxtApp.locale || 'en'],
      },
    })
    return editor
  })
})

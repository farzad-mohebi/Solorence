import type { OutputBlockData } from '@editorjs/editorjs'
import type { ExcalidrawElement } from '@excalidraw/excalidraw/types/element/types'

export interface EditorData {
  time: number
  blocks?: OutputBlockData[]
  version: string
};
export const EditorDataDefaultValue: EditorData = {
  blocks: [],
  time: new Date().getTime(),
  version: '2.30.6',
}
export interface EditorJSFunctions {
  uploadFile?: any
  readOnly?: boolean
  locale?: string
  hide?: string[]
}
export interface BoardData {
  show: boolean
  uid: string
  title: string
  elements: ExcalidrawElement[]
}

export const defaultBoardData: BoardData = {
  show: false,
  uid: '',
  title: '',
  elements: [],
}

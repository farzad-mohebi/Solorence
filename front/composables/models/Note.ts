import type { OutputBlockData } from '@editorjs/editorjs'

export interface Note {
  id?: number
  title: string
  editor_data?: OutputBlockData[]
};
export const NoteDefaultValue: Note = {
  title: '',
  editor_data: [],
}

export interface NoteAttachment {
  id?: number
  title: string
  editor_data?: OutputBlockData[]
  note: number | any | null
  image: string
};

export interface NoteSecurityConfig {
  note?: number
  status: number
  public_joiners_access: number
  link?: string
}

export interface NoteHistory {
  title: string
  blocks: OutputBlockData[]
  is_read_only?: boolean
  time: number
}

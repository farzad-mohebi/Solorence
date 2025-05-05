import type { OutputBlockData } from '@editorjs/editorjs'

export interface Template {
  id?: number
  title: string
  editor_data?: OutputBlockData[]
};
export const TemplateDefaultValue: Template = {
  title: '',
  editor_data: [],
}

import type EditorJS from '@editorjs/editorjs'

declare module '#app' {
  interface NuxtApp {
    $editorjs: (id: string, options: any) => EditorJS
  }
}

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $editorjs: (id: string, options: any) => EditorJS
  }
}

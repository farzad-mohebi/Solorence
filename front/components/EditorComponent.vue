<template>
  <div>
    <div id="editorjs" />
    <button @click="saveContent">
      Save Content
    </button>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

let editor

onMounted(() => {
  const { $editorjs } = useNuxtApp()

  editor = $editorjs('editorjs')
})

const saveContent = () => {
  editor.save().then((outputData) => {
    console.log('Article data:', outputData)
  }).catch((error) => {
    console.log('Saving failed: ', error)
  })
}
</script>

<style scoped>
/* Add any specific styles for the editor */
#editorjs {
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 4px;
}
</style>

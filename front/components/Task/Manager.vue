<template>
  <div>
    <MeetDialog />
    <v-dialog v-model="taskDialog"
              max-width="600"
    >
      <v-card prepend-icon="mdi-check-circle-outline"
              :title="selectedTask.id ? $t('update_task') : $t('add_new_task')"
      >
        <v-card-text class="mt-2">
          <v-text-field v-model="selectedTask.title"
                        name="title"
                        :label="$t('title')"
                        required
          />
          <v-row>
            <v-col md="6">
              <v-select v-model="selectedTask.status"
                        hide-details
                        name="status"
                        class="task-status"
                        :items="[{ name: $t('open'), value: 0 }, { name: $t('in_progress'), value: 1 }, { name: $t('task_done'), value: 2 }]"
                        item-title="name"
                        item-value="value"
                        :label="$t('status')"
              />
            </v-col>
            <v-col md="6">
              <v-date-input id="task-due-date"
                            v-model="due_date"
                            hide-actions
                            clearable
                            :label="$t('due_date')"
                            hide-details
                            @click:clear="due_date = null"
              />
            </v-col>
          </v-row>
          <div id="task-editor" />
        </v-card-text>
        <v-divider />
        <v-card-actions>
          <v-btn v-if="selectedTask.id"
                 color="red"
                 variant="flat"
                 @click="deleteDialog = true"
          >
            {{
              $t('delete')
            }}
          </v-btn>
          <v-spacer />
          <v-btn :text="$t('cancel')"
                 variant="plain"
                 @click="taskDialog = false"
          />
          <v-btn color="primary"
                 :text="selectedTask.id ? $t('update') : $t('save')"
                 variant="flat"
                 @click="selectedTask.id ? updateTask() : createTask()"
          />
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="deleteDialog"
              width="auto"
              persistent
              max-width="400"
    >
      <v-card :loading="loading"
              max-width="400"
              prepend-icon="mdi-alert"
              :text="$t('delete_sure')"
              :title="$t('deleting') + '!'"
      >
        <template #actions>
          <v-spacer />
          <v-btn variant="plain"
                 @click="deleteDialog = false"
          >
            {{ $t('cancel') }}
          </v-btn>
          <v-btn variant="elevated"
                 color="red"
                 @click="deleteTask()"
          >
            {{ $t('yes_delete_it') }}
          </v-btn>
        </template>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import type EditorJS from '@editorjs/editorjs'
import { useUtilsStore } from '~/store/utils'
import { TaskDefaultValue, type Task } from '~/composables/models/Task.js'

const utilStore = useUtilsStore()
const route = useRoute()

const due_date = ref<Date | null>(null)
const loading = ref<any>(false)

const selectedTask = useState<Task>('selectedTask', () => {
  return { ...TaskDefaultValue }
})
let editor: EditorJS
const taskDialog = useState<boolean>('taskDialog', () => false)
const tasks = useState<Task[]>('tasks', () => [])
const deleteDialog = ref(false)
const createTask = async () => {
  if (!selectedTask.value) {
    return
  }
  loading.value = true
  const { blocks } = await editor.save()
  selectedTask.value.editor_data = blocks
  const { error, data } = await useAuthAPIFetch('/api/v1/task/', {
    method: 'POST',
    body: {
      title: selectedTask.value.title,
      editor_data: selectedTask.value.editor_data,
      due_date: due_date.value ? due_date.value.toISOString().split('T')[0] : null,
      status: selectedTask.value.status,
      note: route.params?.id,
    },
  })
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else {
    utilStore.showSuccessMessage('created_successfully')

    // @ts-expect-error: 'set_task_state' is not typed on the Window object
    if (window['set_task_state']) window['set_task_state']('set', data.value)
    tasks.value = [data.value as Task, ...tasks.value]
    selectedTask.value = { ...TaskDefaultValue }

    taskDialog.value = false
  }
  loading.value = false
}
const updateTask = async () => {
  loading.value = true
  const { blocks } = await editor.save()
  selectedTask.value.editor_data = blocks
  const { error, data } = await useAuthAPIFetch<Task>(`/api/v1/task/${selectedTask.value.id}/`, {
    method: 'PUT',
    body: {
      ...selectedTask.value,
      due_date: due_date.value ? due_date.value.toISOString().split('T')[0] : null,
    },
  })
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else if (data.value) {
    utilStore.showSuccessMessage('updated_successfully')
    tasks.value = tasks.value.map((task: Task) => {
      if (task.id === data.value?.id) {
        return { ...data.value } as Task
      }
      return task
    })
    selectedTask.value = { ...TaskDefaultValue }
    due_date.value = null
    taskDialog.value = false
    // @ts-expect-error: 'update_task_TASKID' is not typed on the Window object
    if (window['update_task_' + data.value.id]) window['update_task_' + data.value.id](data.value)
  }
  loading.value = false
}
const loadTask = async () => {
  loading.value = true
  const { error, data } = await useAuthAPIFetch<Task>(`/api/v1/task/${selectedTask.value.id}/`)
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else if (data.value) {
    selectedTask.value = data.value
    if (selectedTask.value.due_date)
      due_date.value = new Date(selectedTask.value.due_date)
  }
  loading.value = false
}
const deleteTask = async () => {
  loading.value = true
  const { error } = await useAuthAPIFetch(`/api/v1/task/${selectedTask.value.id}/`, {
    method: 'DELETE',
  })
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else {
    utilStore.showSuccessMessage('deleted_successfully')
    tasks.value = tasks.value.filter(task => task.id !== selectedTask.value.id)

    // @ts-expect-error: 'set_task_state' is not typed on the Window object
    if (window['update_task_' + selectedTask.value.id]) window['update_task_' + selectedTask.value.id]('deleted')

    selectedTask.value = { ...TaskDefaultValue }
    taskDialog.value = false
    deleteDialog.value = false
  }
  loading.value = false
}
watch(taskDialog, async () => {
  if (selectedTask.value.id && !selectedTask.value.title) {
    await loadTask()
  }
  if (taskDialog.value === false) {
    // @ts-expect-error: 'set_task_state' is not typed on the Window object
    if (window['set_task_state']) window['set_task_state']('cancel')
  }
  if (selectedTask.value.due_date)
    due_date.value = new Date(selectedTask.value.due_date)
  else
    due_date.value = null
  if (!taskDialog.value) {
    selectedTask.value = { ...TaskDefaultValue }
    due_date.value = null
  }
  if (taskDialog.value) {
    const { $editorjs } = useNuxtApp()
    editor = $editorjs('task-editor', {
      uploadFile: uploadFile,
      showCreateMeet: showCreateMeet,
      showMeet: showMeet,
      hide: [
        'page',
        'linkTool',
        'share',
      ],
    })
    await editor.isReady
    loading.value = false
    if (selectedTask.value.editor_data)
      editor.blocks.render({
        blocks: selectedTask.value.editor_data,
      })
  }
})
</script>

<style></style>

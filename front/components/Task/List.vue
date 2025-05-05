<template>
  <v-card elevation="0">
    <template v-if="loading">
      <v-skeleton-loader v-for="_ in 10"
                         :key="_"
                         type="list-item-avatar"
                         width="400"
                         max-width="100%"
                         class="mt-1"
      />
    </template>
    <v-list v-else
            max-height="400"
            lines="one"
            select-strategy="leaf"
    >
      <v-list-item id="add-task"
                   @click="taskDialog = true; selectedTask = { ...TaskDefaultValue }"
      >
        <template #prepend>
          <v-icon icon="mdi-plus" />
        </template>
        <template #title>
          <div>
            {{ $t('new_task') }}
          </div>
        </template>
      </v-list-item>
      <v-list-item v-for="task in tasks"
                   :key="task.id"
                   class="task"
      >
        <template #title>
          <div class="cursor-pointer"
               :class="task.status === 2 ? 'text-decoration-line-through' : ''"
               @click="taskDialog = true; selectedTask = { ...task }"
          >
            {{ task.title }}
            <v-icon v-if="task.status === 1"
                    title="in progress"
            >
              mdi-progress-clock
            </v-icon>
            <span v-if="task.due_date && task.status !== 2"
                  class="text-red"
            >
              <span
                v-if="new Date(task.due_date) > new Date()"
                :class="dayDistance(new Date(task.due_date)) > 2 ? 'text-grey' : 'text-orange'"
              >
                (
                {{ dayDistance(new Date(task.due_date)) + 1 }}
                {{ $t('days_remaining') }}
                )
              </span>
              <strong v-else
                      class="text-red ms-2"
              >
                {{ $t('passed') }}!
              </strong>
            </span>
          </div>
        </template>
        <template #prepend>
          <v-list-item-action start>
            <v-checkbox-btn :model-value="task.status === 2"
                            @update:model-value="doneTask(task)"
            />
          </v-list-item-action>
        </template>
      </v-list-item>
    </v-list>
    <TaskManager />
  </v-card>
</template>

<script setup lang="ts">
import { useUtilsStore } from '~/store/utils'
import { TaskDefaultValue, type Task } from '~/composables/models/Task.js'
import { dayDistance } from '~/composables/custom_functions.js'

const selectedTask = useState<Task>('selectedTask', () => {
  return { ...TaskDefaultValue }
})

const taskDialog = useState<boolean>('taskDialog', () => false)
const tasks = useState<Task[]>('tasks', () => [])
const utilStore = useUtilsStore()
const loading = ref<boolean>(true)

const doneTask = async (task: Task): Promise<void> => {
  const { error, data } = await useAuthAPIFetch<Task>(`/api/v1/task/${task.id}/`, {
    method: 'PATCH',
    body: {
      status: task.status !== 2 ? 2 : 0,
    },
  })
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else if (data.value) {
    task.status = data.value?.status
  }
}

const getTasks = async (): Promise<void> => {
  loading.value = true
  const { error, data } = await useAuthAPIFetch<Task[]>('/api/v1/task/')

  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else if (data.value) {
    tasks.value = data.value
  }
  loading.value = false
}

getTasks()
</script>

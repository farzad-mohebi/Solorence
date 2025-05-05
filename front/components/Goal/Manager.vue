<template>
  <div>
    <MeetDialog />
    <v-dialog v-model="goalDialog"
              max-width="600"
    >
      <v-card prepend-icon="mdi-check-circle-outline"
              :title="selectedGoal.id ? $t('update_goal') : $t('add_new_goal')"
      >
        <v-card-text class="mt-2">
          <v-text-field v-model="selectedGoal.title"
                        name="title"
                        :label="$t('title')"
                        required
          />
          <v-textarea v-model="selectedGoal.description"
                      name="description"
                      :label="$t('description')"
          />
          <!-- <v-row>
            <v-col md="6">
              <v-select v-model="selectedGoal.status"
                        hide-details
                        name="status"
                        class="goal-status"
                        :items="[{ name: $t('open'), value: 0 }, { name: $t('in_progress'), value: 1 }, { name: $t('done'), value: 2 }]"
                        item-title="name"
                        item-value="value"
                        :label="$t('status')"
              />
            </v-col>
            <v-col md="6">
              <v-date-input id="goal-due-date"
                            v-model="due_date"
                            hide-actions
                            clearable
                            :label="$t('due_date')"
                            hide-details
                            @click:clear="due_date = null"
              />
            </v-col>
          </v-row> -->
          <!-- <v-slider class="mt-10"
                    :min="0"
                    :max="100"
                    :step="5"
                    color="black"
                    thumb-label="always"
          /> -->
          <div id="goal-editor" />
        </v-card-text>
        <v-divider />
        <v-card-actions>
          <v-btn v-if="selectedGoal.id"
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
                 @click="goalDialog = false"
          />
          <v-btn color="primary"
                 :text="selectedGoal.id ? $t('update') : $t('save')"
                 variant="flat"
                 @click="selectedGoal.id ? updateGoal() : createGoal()"
          />
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { useUtilsStore } from '~/store/utils'
import { GoalDefaultValue, type Goal } from '~/composables/models/Goal.js'

const utilStore = useUtilsStore()

const due_date = ref<Date | null>(null)
const loading = ref<any>(false)

const selectedGoal = useState<Goal>('selectedGoal', () => {
  return { ...GoalDefaultValue }
})
const dashboardGoal = useState<Goal>('dashboardGoal', () => {
  return { ...GoalDefaultValue }
})
const goalDialog = useState<boolean>('goalDialog', () => false)
const goals = useState<Goal[]>('goals', () => [])
const deleteDialog = ref(false)
const createGoal = async () => {
  if (!selectedGoal.value) {
    return
  }
  loading.value = true
  const { error, data } = await useAuthAPIFetch('/api/v1/goal/', {
    method: 'POST',
    body: {
      title: selectedGoal.value.title,
      description: selectedGoal.value.description,
    },
  })
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else {
    utilStore.showSuccessMessage('created_successfully')
    goals.value = [data.value as Goal, ...goals.value]
    selectedGoal.value = { ...GoalDefaultValue }

    goalDialog.value = false
  }
  loading.value = false
}
const updateGoal = async () => {
  loading.value = true
  const { error, data } = await useAuthAPIFetch<Goal>(`/api/v1/goal/${selectedGoal.value.id}/`, {
    method: 'PUT',
    body: {
      ...selectedGoal.value,
      due_date: due_date.value ? due_date.value.toISOString().split('T')[0] : null,
    },
  })
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else if (data.value) {
    utilStore.showSuccessMessage('updated_successfully')
    goals.value = goals.value.map((goal: Goal) => {
      if (goal.id === data.value?.id) {
        return { ...data.value } as Goal
      }
      return goal
    })
    selectedGoal.value = { ...GoalDefaultValue }
    if (dashboardGoal.value?.id === data.value.id) {
      dashboardGoal.value = { ...data.value }
    }
    due_date.value = null
    goalDialog.value = false
  }
  loading.value = false
}
const loadGoal = async () => {
  loading.value = true
  const { error, data } = await useAuthAPIFetch<Goal>(`/api/v1/goal/${selectedGoal.value.id}/`)
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else if (data.value) {
    selectedGoal.value = data.value
  }
  loading.value = false
}
watch(goalDialog, async () => {
  if (selectedGoal.value.id && !selectedGoal.value.title) {
    await loadGoal()
  }
  if (!goalDialog.value) {
    selectedGoal.value = { ...GoalDefaultValue }
    due_date.value = null
  }
  if (goalDialog.value) {
    loading.value = false
  }
})
</script>

<style></style>

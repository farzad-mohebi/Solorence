<template>
  <div>
    <v-dialog v-model="goalTargetDialog"
              max-width="600"
    >
      <v-card prepend-icon="mdi-check-circle-outline"
              :loading="loading"
              :title="selectedGoalTarget.id ? $t('update_goalTarget') : $t('add_new_goalTarget')"
      >
        <v-card-text class="mt-2">
          <v-text-field v-model="selectedGoalTarget.title"
                        name="title"
                        :label="$t('title')"
                        required
          />
          <v-textarea v-model="selectedGoalTarget.description"
                      name="description"
                      :label="$t('description')"
          />
          <v-row class="align-center">
            <v-col md="6">
              <v-date-input id="goal-target-deadline"
                            v-model="deadlineDate"
                            hide-actions
                            clearable
                            :label="$t('deadlineDate')"
                            hide-details
                            @click:clear="deadlineDate = null"
              />
            </v-col>
            <v-col md="6">
              <v-slider
                v-model="selectedGoalTarget.progress"
                hide-details
                :label="'progress: '+ selectedGoalTarget.progress+ '%'"
                :min="0"
                :max="100"
                :step="10"
                color="primary"
              />
            </v-col>
          </v-row>
        </v-card-text>
        <v-divider />
        <v-card-actions>
          <v-btn v-if="selectedGoalTarget.id"
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
                 @click="goalTargetDialog = false"
          />
          <v-btn color="primary"
                 :text="selectedGoalTarget.id ? $t('update') : $t('save')"
                 variant="flat"
                 @click="selectedGoalTarget.id ? updateGoalTarget() : createGoalTarget()"
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
                 @click="deleteGoalTarget()"
          >
            {{ $t('yes_delete_it') }}
          </v-btn>
        </template>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { useUtilsStore } from '~/store/utils'
import { GoalDefaultValue, GoalTargetDefaultValue, type Goal, type GoalTarget } from '~/composables/models/Goal.js'

const utilStore = useUtilsStore()
const emit = defineEmits(['targetUpdate'])

const deadlineDate = ref<Date | null>(null)
const loading = ref<any>(false)
const dashboardGoal = useState<Goal>('dashboardGoal', () => {
  return { ...GoalDefaultValue }
})
const selectedGoalTarget = useState<GoalTarget>('selectedGoalTarget', () => {
  return { ...GoalTargetDefaultValue }
})
const goalTargetDialog = useState<boolean>('goalTargetDialog', () => false)
const goalTargets = useState<GoalTarget[]>('targets', () => [])
const deleteDialog = ref(false)
const createGoalTarget = async () => {
  if (!selectedGoalTarget.value) {
    return
  }
  loading.value = true
  const { error, data } = await useAuthAPIFetch<GoalTarget>('/api/v1/goaltarget/', {
    method: 'POST',
    body: {
      ...selectedGoalTarget.value,
      deadline_at: deadlineDate.value ? deadlineDate.value.toISOString().split('T')[0] : null,
      goal: dashboardGoal.value.id,
    },
  })
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else if (data.value) {
    utilStore.showSuccessMessage('created_successfully')
    goalTargets.value = [data.value, ...goalTargets.value]
    selectedGoalTarget.value = { ...GoalTargetDefaultValue }
    goalTargetDialog.value = false
  }
  loading.value = false
  emit('targetUpdate')
}
const updateGoalTarget = async () => {
  loading.value = true
  const { error, data } = await useAuthAPIFetch<GoalTarget>(`/api/v1/goaltarget/${selectedGoalTarget.value.id}/`, {
    method: 'PUT',
    body: {
      ...selectedGoalTarget.value,
      deadline_at: deadlineDate.value ? deadlineDate.value.toISOString().split('T')[0] : null,
    },
  })
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else if (data.value) {
    utilStore.showSuccessMessage('updated_successfully')
    goalTargets.value = goalTargets.value.map((goalTarget: GoalTarget) => {
      if (goalTarget.id === data.value?.id) {
        return { ...data.value } as GoalTarget
      }
      return goalTarget
    })
    selectedGoalTarget.value = { ...GoalTargetDefaultValue }
    deadlineDate.value = null
    goalTargetDialog.value = false
  }
  loading.value = false
  emit('targetUpdate')
}
// const loadGoal = async () => {
//   loading.value = true
//   const { error, data } = await useAuthAPIFetch<GoalTarget>(`/api/v1/goaltarget/${selectedGoalTarget.value.id}/`)
//   if (error.value) {
//     utilStore.showApiError(error.value)
//   }
//   else if (data.value) {
//     selectedGoalTarget.value = data.value
//   }
//   loading.value = false
// }

const deleteGoalTarget = async () => {
  loading.value = true
  const { error } = await useAuthAPIFetch(`/api/v1/goaltarget/${selectedGoalTarget.value.id}/`, {
    method: 'DELETE',
  })
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else {
    utilStore.showSuccessMessage('deleted_successfully')
    goalTargets.value = goalTargets.value.filter(goalTarget => goalTarget.id !== selectedGoalTarget.value.id)

    selectedGoalTarget.value = { ...GoalTargetDefaultValue }
    goalTargetDialog.value = false
    deleteDialog.value = false
  }
  loading.value = false
  emit('targetUpdate')
}

watch(goalTargetDialog, () => {
  if (goalTargetDialog.value) {
    if (selectedGoalTarget.value.id && selectedGoalTarget.value.deadline_at) {
      deadlineDate.value = new Date(selectedGoalTarget.value.deadline_at)
    }
  }
})
</script>

  <style></style>

<template>
  <div>
    <v-dialog
      v-model="dialog"
      transition="dialog-bottom-transition"
      fullscreen
    >
      <v-card :loading="loading">
        <v-toolbar color="primary">
          <v-btn
            icon="mdi-close"
            @click="dialog = false"
          />

          <v-toolbar-title>Settings</v-toolbar-title>

          <v-spacer />

          <v-toolbar-items>
            <v-btn
              prepend-icon="mdi-delete"
              text="Delete This Goal"
              variant="text"
              @click="deleteDialog = true;selectedGoal = { ...dashboardGoal }"
            />
            <v-btn
              prepend-icon="mdi-pencil"
              text="Update Information"
              variant="text"
              @click="goalDialog = true;dialog=false;selectedGoal = { ...dashboardGoal }"
            />
            <v-btn
              prepend-icon="mdi-content-save"
              text="Save and Close"
              variant="text"
              @click="dialog = false"
            />
          </v-toolbar-items>
        </v-toolbar>
        <v-list
          lines="two"
          subheader
        >
          <v-list-item>
            <div class="d-flex align-center">
              <v-progress-circular
                :size="80"
                :width="10"
                :model-value="dashboardGoal.progress"
                color="purple"
              >
                <strong>{{ dashboardGoal.progress }}%</strong>
              </v-progress-circular>
              <div class="ms-5">
                <div class="text-uppercase font-weight-bold text-h4">
                  {{ dashboardGoal.title }}
                </div>
                <p class="text-grey">
                  {{ dashboardGoal.description }}
                </p>
              </div>
            </div>
          </v-list-item>

          <v-divider class="my-5" />

          <v-list-subheader class="py-3">
            <v-icon class="me-1">
              mdi-bullseye-arrow
            </v-icon>
            Targets
            <v-btn color="primary"
                   variant="flat"
                   size="small"
                   class="ms-4"
                   prepend-icon="mdi-plus"
                   @click="goalTargetDialog=true;selectedGoalTarget={ ...GoalTargetDefaultValue }; "
            >
              {{ $t('add_target') }}
            </v-btn>
          </v-list-subheader>
          <template v-if="!targetsLoading">
            <v-list-item>
              <v-card v-for="target in targets"
                      :key="target.id"
                      class="target-card"
                      @click="selectedGoalTarget={ ...target }; goalTargetDialog=true"
              >
                <v-card-text class="text-medium-emphasis pa-3">
                  <div class="d-flex align-center justify-space-between">
                    <div class="w-100">
                      <div class="text-h6 mb-1 font-weight-bold ">
                        {{ target.title }}
                      </div>
                      <p class="text-muted">
                        {{ target.description }}
                      </p>
                    </div>
                    <div class="w-100"
                         style="max-width: 300px;"
                    >
                      <div class="text-h4 d-flex align-center justify-space-between font-weight-black mb-2">
                        {{ target.progress }}%
                        <v-chip
                          v-if="target.progress === 100"
                          color="green"
                          variant="text"
                        >
                          <v-icon>mdi-check</v-icon>
                        </v-chip>
                        <v-chip v-else-if="target.deadline_at && target.progress !== 100 && new Date(target.deadline_at) < new Date()"
                                color="red"
                                variant="flat"
                        >
                          {{ $t('passed') }}!
                        </v-chip>
                        <v-chip
                          v-else-if="target.deadline_at && new Date(target.deadline_at) > new Date()"
                          :color="dayDistance(new Date(target.deadline_at)) > 2 ? 'black' : 'orange'"
                        >
                          {{ dayDistance(new Date(target.deadline_at)) + 1 }}
                          {{ $t('days_remaining') }}
                        </v-chip>
                      </div>
                      <v-progress-linear
                        bg-color="surface-variant"
                        class="mb-3"
                        color="primary"
                        height="10"
                        :model-value="target.progress"
                      />
                    </div>
                  </div>
                </v-card-text>
              </v-card>
            </v-list-item>
          </template>
          <template v-else>
            <v-skeleton-loader v-for="_ in 5"
                               :key="_"
                               max-width="500"
                               type="list-item-two-line"
            />
          </template>
        </v-list>
      </v-card>
    </v-dialog>
    <GoalTargetManager @target-update="loadGoal" />
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
                 @click="deleteGoal()"
          >
            {{ $t('yes_delete_it') }}
          </v-btn>
        </template>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { type Goal, type GoalTarget, GoalDefaultValue, GoalTargetDefaultValue } from '~/composables/models/Goal'
import { useUtilsStore } from '~/store/utils'
import { dayDistance } from '~/composables/custom_functions.js'

const utilStore = useUtilsStore()
const loading = ref<boolean>(false)
const deleteDialog = ref<boolean>(false)
const targetsLoading = ref<boolean>(true)
const goalTargetDialog = useState<boolean>('goalTargetDialog', () => false)
const dashboardGoal = useState<Goal>('dashboardGoal', () => {
  return { ...GoalDefaultValue }
})

const selectedGoal = useState<Goal>('selectedGoal', () => {
  return { ...GoalDefaultValue }
})

const goalDialog = useState<boolean>('goalDialog', () => false)
const selectedGoalTarget = useState<GoalTarget>('selectedGoalTarget', () => {
  return { ...GoalTargetDefaultValue }
})

const dialog = ref<boolean>(false)

const targets = useState<GoalTarget[]>('targets', () => [])

const loadTargets = async (): Promise<void> => {
  targetsLoading.value = true

  const { error, data } = await useAuthAPIFetch<GoalTarget[]>('/api/v1/goaltarget/goal/' + dashboardGoal.value.id)

  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else if (data.value) {
    targets.value = data.value
  }
  targetsLoading.value = false
}
const goals = useState<Goal[]>('goals', () => [])
const loadGoal = async (): Promise<void> => {
  loading.value = true

  const { error, data } = await useAuthAPIFetch<Goal>('/api/v1/goal/' + dashboardGoal.value.id)

  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else if (data.value) {
    dashboardGoal.value = data.value
    goals.value = goals.value.map((goal: Goal) => {
      if (goal.id === data.value?.id)
        return { ...data.value } as Goal
      return goal
    })
  }
  loading.value = false
}
const showGoal = (clickedGoal: Goal) => {
  dashboardGoal.value = { ...clickedGoal }
  dialog.value = true
  loadTargets()
}

const deleteGoal = async () => {
  loading.value = true
  const { error } = await useAuthAPIFetch(`/api/v1/goal/${dashboardGoal.value.id}/`, {
    method: 'DELETE',
  })
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else {
    console.log(goals.value)
    utilStore.showSuccessMessage('deleted_successfully')
    console.log(goals.value)
    goals.value = goals.value.filter(goal => goal.id !== dashboardGoal.value.id)

    dashboardGoal.value = { ...GoalDefaultValue }
    goalTargetDialog.value = false
    dialog.value = false
    deleteDialog.value = false
  }
  loading.value = false
}
defineExpose({ showGoal })
</script>

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
            select-strategy="leaf"
    >
      <v-list-item id="add-goal"
                   @click="goalDialog = true; selectedGoal = { ...GoalDefaultValue }"
      >
        <template #prepend>
          <v-icon icon="mdi-plus" />
        </template>
        <template #title>
          <div>
            {{ $t('new_goal') }}
          </div>
        </template>
      </v-list-item>
      <v-list-item v-for="goal in goals"
                   :key="goal.id"
                   class="goal cursor-pointer py-3"
                   @click="goalDashboard.showGoal(goal)"
      >
        <template #title>
          <div class="ms-3">
            <div :class="'text-'+ getPercentColor(goal.progress||0)"
                 class="text-uppercase font-weight-bold text-h5"
            >
              {{ goal.title }}
            </div>
            <p class="text-grey">
              {{ goal.description }}
            </p>
          </div>
        </template>
        <template #prepend>
          <v-list-item-action start>
            <v-progress-circular
              :size="65"
              :width="8"
              :model-value="goal.progress"
              :color="getPercentColor(goal.progress||0)"
            >
              <strong>{{ goal.progress }}%</strong>
            </v-progress-circular>
          </v-list-item-action>
        </template>
      </v-list-item>
    </v-list>
    <GoalManager />
    <GoalDashboard ref="goalDashboard" />
  </v-card>
</template>

<script setup lang="ts">
import { useUtilsStore } from '~/store/utils'
import { GoalDefaultValue, type Goal } from '~/composables/models/Goal.js'
import { getPercentColor } from '~/composables/custom_functions.js'

const goalDashboard = ref()
const selectedGoal = useState<Goal>('selectedGoal', () => {
  return { ...GoalDefaultValue }
})

const goalDialog = useState<boolean>('goalDialog', () => false)
const goals = useState<Goal[]>('goals', () => [])
const utilStore = useUtilsStore()
const loading = ref<boolean>(true)

const getGoals = async (): Promise<void> => {
  loading.value = true
  const { error, data } = await useAuthAPIFetch<Goal[]>('/api/v1/goal/')

  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else if (data.value) {
    goals.value = data.value
  }
  loading.value = false
}

getGoals()
</script>

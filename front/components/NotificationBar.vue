<script setup lang="ts">
import { onMounted, nextTick } from 'vue'

import { useUtilsStore } from '~/store/utils'
import type { NotificationModel } from '~/composables/models/Notification.js'

const utilStore = useUtilsStore()
const localePath = useLocalePath()

const menu = ref(false)

const notificationLoading = ref(true)
const notifications = ref<NotificationModel[]>([])
const unSeenCount = ref(0)

const loadData = async () => {
  const { error, data } = await useAuthAPIFetch<NotificationModel[]>(`/api/v1/notification/`)
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else if (data.value) {
    notifications.value = data.value
    unSeenCount.value = notifications.value.filter(notif => notif.is_seen === false).length
  }
  notificationLoading.value = false
}

const goToNotification = async (notification: NotificationModel) => {
  notificationLoading.value = true
  const { error, data } = await useAuthAPIFetch<any>(`/api/v1/notification/seen/${notification.id}/`, {
    method: 'PUT',
  })
  notificationLoading.value = false
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else if (data.value) {
    menu.value = false
    if (notification.is_seen === false) {
      notification.is_seen = true
      unSeenCount.value -= 1
    }
    await navigateTo(localePath('/note/link/' + data.value.link))
  }
}
onMounted(async () => {
  await nextTick()
  await loadData()
})
</script>

<template>
  <div>
    <v-menu v-model="menu"
            transition="scale-transition"
            :close-on-content-click="false"
    >
      <template #activator="{ props }">
        <v-btn
          icon
          variant="text"
          v-bind="props"
        >
          <v-badge v-if="unSeenCount"
                   color="error"
                   :content="unSeenCount"
          >
            <v-icon>mdi-bell</v-icon>
          </v-badge>
          <v-icon v-else>
            mdi-bell
          </v-icon>
        </v-btn>
      </template>

      <v-card class="mx-auto"
              width="350"
      >
        <v-toolbar color="brown-lighten-1">
          <v-toolbar-title>{{ $t('notifications') }}</v-toolbar-title>

          <v-spacer />

          <v-btn icon="mdi-bell-outline"
                 variant="text"
          />
        </v-toolbar>

        <v-list v-if="notifications.length"
                class="less-prepend-space py-0"
                max-height="500"
                lines="two"
        >
          <v-list-item v-for="(notification, i) in notifications"
                       :key="i"
                       :value="notification"
                       color="white"
                       @click="goToNotification(notification)"
          >
            <template #prepend>
              <v-icon v-if="notification.is_seen"
                      icon="mdi-account-circle"
                      color="grey-lighten-1"
                      size="40"
              />
              <v-badge v-else
                       dot
                       color="red"
              >
                <v-icon icon="mdi-account-circle"
                        color="primary"
                        size="40"
                />
              </v-badge>
            </template>
            <template #title>
              <div :class="notification.is_seen ? 'text-grey-darken-1' : ''">
                <strong class=" me-1 text-uppercase">
                  @{{ notification.user.username }}
                </strong>
                <span>{{ $t('mentioned_you') }}</span>
              </div>
            </template>
            <template #subtitle>
              {{ notification.text }}
            </template>
          </v-list-item>
        </v-list>
        <p v-else
           class="text-center py-5  text-grey"
        >
          {{ $t('no_notification') }}
        </p>
      </v-card>
    </v-menu>
  </div>
</template>

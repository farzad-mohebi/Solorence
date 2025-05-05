<template>
  <div name="google-calendar-dialog">
    <v-dialog v-model="authStore.showGoogleCalendarAuth"
              width="auto"
    >
      <v-card max-width="400"
              :loading="loading"
              :disabled="loading"
              prepend-icon="mdi-update"
              text="You need to Access our application to your google calendar to send Data."
              title="Google Calendar Authenticate"
      >
        <template #actions>
          <v-btn text="Cancel"
                 @click="dialog = false"
          />
          <v-btn color="green"
                 variant="elevated"
                 text="Authenticate"
                 @click="askCalendarAccess"
          />
        </template>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { useAuthStore } from '~/store/auth'
import { useUtilsStore } from '~/store/utils'

const config = useRuntimeConfig()
let tokenClient
const loading = ref(false)
const authStore = useAuthStore()
const utilStore = useUtilsStore()

// const DISCOVERY_DOC = 'https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest'
const SCOPES = 'https://www.googleapis.com/auth/calendar.events https://www.googleapis.com/auth/calendar'

const askCalendarAccess = async () => {
  loading.value = true

  gapi.load('client', () => {
    tokenClient = google.accounts.oauth2.initTokenClient({
      client_id: config.public.googleClientID,
      scope: SCOPES,
      callback: async (resp) => {
        loading.value = false
        if (resp.error !== undefined) {
          throw (resp)
        }
        authStore.setGoogleCalendarToken(resp.access_token)
        utilStore.showSuccessMessage('google_calendar_connected')
      },
    })
    if (gapi.client.getToken() === null) {
      tokenClient.requestAccessToken({ prompt: 'consent' })
    }
    else {
      tokenClient.requestAccessToken({ prompt: '' })
    }
  })
}
</script>

<style>
.v-snack__wrapper,
div[name="snackbars"] {
    z-index: 99999999 !important;
}
</style>

<template>
  <v-app>
    <v-locale-provider :rtl="isRTL">
      <MessageComponent />
      <GoogleCalendarDialog />
      <v-main>
        <v-container max-width="1340">
          <v-card elevation="0"
                  class="mb-5 border rounded-lg"
          >
            <v-card-text>
              <div class="d-flex align-center justify-space-between">
                <div class="text-h6 my-2 d-flex align-center justify-space-between">
                  <div class="d-flex align-center justify-content-between">
                    <div>
                      <v-icon class="mb-1"
                              color="primary"
                              size="x-large"
                      >
                        mdi-account-circle
                      </v-icon>
                    </div>
                    <div class="text-start ms-3">
                      <div class="text-caption text-primary">
                        {{ $t('welcome') }},
                      </div>
                      <div class="text-uppercase mt-n1">
                        {{ authStore.info?.first_name }} {{ authStore.info?.last_name }}
                      </div>
                    </div>
                  </div>
                </div>
                <div class="d-flex ga-4 align-center justify-center">
                  <div class="">
                    <LanguageChange />
                  </div>
                  <NotificationBar />
                  <v-btn
                    icon
                    variant="text"
                    @click="toggleTheme"
                  >
                    <v-icon :icon="cookieTheme === 'dark' ? 'mdi-weather-sunny' : 'mdi-weather-night'" />
                  </v-btn>
                  <v-btn position="relative"
                         color="primary"
                         icon="mdi-menu"
                         variant="tonal"
                         size="50"
                         @click="dialog = true"
                  />
                </div>
              </div>
            </v-card-text>
          </v-card>

          <slot />
        </v-container>
      </v-main>
      <v-dialog v-model="dialog"
                max-width="400"
      >
        <v-card>
          <v-card-text>
            <v-row>
              <v-col v-if="authStore.info"
                     cols="12"
              >
                <div class="text-center">
                  <v-avatar image="~/assets/image/user.webp"
                            size="120"
                  />
                  <div class="text-h5 mt-3">
                    {{ authStore.info.first_name }}
                    {{ authStore.info.last_name }}
                  </div>
                  <div class="text-grey">
                    {{ authStore.info.username }}
                  </div>
                </div>
              </v-col>
              <v-col>
                <v-card class="mx-2">
                  <v-card-text class="pa-3 text-center bg-green">
                    Profile
                    <v-icon class="ms-2">
                      mdi-account
                    </v-icon>
                  </v-card-text>
                </v-card>
                <v-card class="ma-2"
                        :to="localePath('/change_password')"
                        @click="dialog = false"
                >
                  <v-card-text class="pa-3 text-center text-white bg-primary">
                    {{ $t('change_password') }}
                    <v-icon class="ms-2">
                      mdi-key
                    </v-icon>
                  </v-card-text>
                </v-card>
                <v-card class="ma-2"
                        @click="authStore.logUserOut(navigate = true)"
                >
                  <v-card-text class="pa-3 text-center bg-red">
                    Logout
                    <v-icon class="ms-2">
                      mdi-logout
                    </v-icon>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-dialog>
    </v-locale-provider>
  </v-app>
</template>

<script setup>
import { useTheme } from 'vuetify'
import { useAuthStore } from '~/store/auth'

const theme = useTheme()
const cookieTheme = useCookie('theme')
theme.global.name.value = cookieTheme.value === 'dark' ? 'dark' : 'light'
const toggleTheme = () => {
  const cookieTheme = useCookie('theme')
  cookieTheme.value = cookieTheme.value === 'dark' ? 'light' : 'dark'
  theme.global.name.value = cookieTheme.value
}
const { locale } = useI18n()

const localePath = useLocalePath()

useHead({
  htmlAttrs: { dir: locale.value === 'fa' ? 'rtl' : 'ltr', lang: locale.value },
})

const isRTL = ref(locale.value === 'fa')

watch(locale, (newLocale) => {
  isRTL.value = newLocale === 'fa'
  useHead({
    htmlAttrs: { dir: locale.value === 'fa' ? 'rtl' : 'ltr', lang: locale.value },
  })
})
const authStore = useAuthStore()

if (!authStore.isAuthenticated) {
  navigateTo(localePath('/login'))
}
await authStore.getMyInfo()

if (!authStore.info.id) {
  authStore.logUserOut()
  navigateTo(localePath('/login'))
}
const dialog = ref(false)
</script>

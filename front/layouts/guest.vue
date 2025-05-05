<template>
  <v-app>
    <v-locale-provider :rtl="isRTL">
      <MessageComponent />
      <GoogleCalendarDialog v-if="authStore.isAuthenticated" />
      <v-main>
        <v-container max-width="1340">
          <div v-if="authStore.isAuthenticated"
               class="d-flex align-center justify-space-between mb-5"
          >
            <div class="text-h6 mb-3 mt-2 d-flex align-center justify-space-between ">
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
              <div class="mt-2">
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

              <v-btn color="black"
                     icon="mdi-home"
                     :to="localePath('/home')"
                     variant="text"
              />
              <v-btn position="relative"
                     color="primary"
                     icon="mdi-menu"
                     variant="tonal"
                     size="50"
                     @click="dialog = true"
              />
            </div>
          </div>
          <slot />
        </v-container>
      </v-main>
      <v-dialog v-if="authStore.isAuthenticated"
                v-model="dialog"
                max-width="500"
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
              <v-col cols="12"
                     md="4"
              >
                <v-card>
                  <v-card-text class="text-center bg-green">
                    Profile
                    <v-icon class="ms-2">
                      mdi-account
                    </v-icon>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12"
                     md="4"
              >
                <v-card>
                  <v-card-text class="text-center text-white bg-primary">
                    Security
                    <v-icon class="ms-2">
                      mdi-shield-account
                    </v-icon>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12"
                     md="4"
              >
                <v-card @click="authStore.logUserOut()">
                  <v-card-text class="text-center bg-red">
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

<script setup lang="ts">
import { ToggleTheme } from '@excalidraw/excalidraw/types/components/main-menu/DefaultItems'
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

if (authStore.isAuthenticated) {
  await authStore.getMyInfo()
}

const dialog = ref(false)
</script>

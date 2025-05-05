<template>
  <v-card :disabled="loading"
          :loading="loading"
          rounded
          class="mx-auto my-12"
          max-width="400"
  >
    <v-img height="200"
           src="~/assets/svg/login.svg"
           contain
    />

    <v-form ref="form"
            class=""
            fast-fail
            @submit.prevent="login"
    >
      <v-card-text class="pb-0">
        <h4 class="text-center pt-5 mt-5 mb-3">
          {{ $t('welcome') }},
        </h4>
        <h2 class="primary--text text-center mb-5">
          {{ $t('login__title') }}
        </h2>
        <v-text-field id="id_username"
                      v-model="username"
                      :rules="FormRules.notEmpty"
                      label="Username"
                      required
                      outlined
        />

        <v-text-field id="id_password"
                      v-model="password"
                      :rules="FormRules.notEmpty"
                      label="Password"
                      required
                      outlined
                      type="password"
        />
      </v-card-text>
      <v-card-actions class="px-5 pb-1 d-block">
        <v-btn type="submit"
               rounded
               size="large"
               block
               color="primary"
               variant="flat"
        >
          {{ $t('login') }}
        </v-btn>
        <div class="text-center d-flex justify-space-between mt-3">
          <v-btn :to="localePath('/signup')"
                 color="green"
                 variant="text"
          >
            {{ $t('signup') }}
          </v-btn>
          <v-btn :to="localePath('/forgot_password')"
                 color="red"
                 variant="text"
          >
            {{ $t('forgot_password') }}
          </v-btn>
        </div>
      </v-card-actions>
      <div class="text-center d-flex align-center justify-space-between px-5 mb-5">
        <LanguageChange />
        <GoogleSignInButton @success="handleLoginSuccess"
                            @error="handleLoginError"
        />
      </div>
    </v-form>
  </v-card>
</template>

<script setup lang="ts">
import { GoogleSignInButton } from 'vue3-google-signin'
import { useAuthStore } from '~/store/auth'
import { useUtilsStore } from '~/store/utils'
import type { AuthorizationToken } from '~/composables/models/Authentication.js'
import { FormRules } from '~/composables/FormRules'

useHead(seoConfig('login_page_title'))

const localePath = useLocalePath()

const userStore = useAuthStore()
const utilStore = useUtilsStore()
const handleLoginSuccess = async (googleToken: any) => {
  loading.value = true
  const { credential } = googleToken
  const { data, error } = await useAPIFetch<AuthorizationToken>('/api/v1/auth/google/', {
    method: 'POST',
    body: {
      credential: credential,
    },
  })
  loading.value = false
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else if (data.value) {
    userStore.setAuth(data.value)
    utilStore.showSuccessMessage('login_success')
    router.push(localePath('/home'))
  }
}

// handle an error event
const handleLoginError = () => {
  console.error('Login failed')
  utilStore.showErrorMessage('login_failed')
}

const router = useRouter()
const loading = ref<boolean>(false)
const username = ref<string>('')
const password = ref<string>('')
const login = async () => {
  loading.value = true
  const { data, error } = await useAPIFetch<AuthorizationToken>('api/v1/auth/token/', {
    method: 'POST',
    body: {
      username: username.value,
      password: password.value,
    },
  })
  if (error.value) {
    loading.value = false
    utilStore.showApiError(error.value)
  }
  else if (data.value) {
    userStore.setAuth(data.value)
    utilStore.showSuccessMessage('login_success')
    router.push(localePath('/home'))
  }
}

definePageMeta({
  layout: 'empty',

})
</script>

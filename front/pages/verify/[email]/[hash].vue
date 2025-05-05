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
    >
      <v-card-text class="pb-0">
        <h4 class="text-center pt-5 mt-5 mb-3">
          {{ $t('complete_signup__title') }}
        </h4>
        <h2 class="primary--text text-center mb-5">
          {{ route.params.email }}
        </h2>
        <v-row>
          <v-col cols="6">
            <v-text-field id="id_first_name"
                          v-model="first_name"
                          :rules="FormRules.notEmpty"
                          label="first name"
                          required
                          outlined
                          type="text"
            />
          </v-col>
          <v-col cols="6">
            <v-text-field id="id_last_name"
                          v-model="last_name"
                          :rules="FormRules.notEmpty"
                          label="last name"
                          required
                          outlined
                          type="text"
            />
          </v-col>
          <v-col cols="6">
            <v-text-field id="id_password"
                          v-model="password"
                          :rules="FormRules.notEmpty"
                          label="Password"
                          required
                          outlined
                          type="password"
            />
          </v-col>
          <v-col cols="6">
            <v-text-field id="id_repeat_password"
                          v-model="repeatPassword"
                          :rules="FormRules.notEmpty"
                          label="Repeat Password"
                          required
                          outlined
                          type="password"
            />
          </v-col>
        </v-row>
      </v-card-text>

      <v-card-actions class="px-5 pb-1 d-block">
        <v-btn rounded
               size="large"
               block
               color="primary"
               variant="flat"
               @click="signup()"
        >
          {{ $t('complete_signup') }}
        </v-btn>
        <div class="text-center d-flex justify-center mt-3" />
      </v-card-actions>
      <div class="text-center d-flex align-center justify-space-between px-5 mb-5">
        <LanguageChange />
        <v-btn :to="localePath('/login')"
               color="primary"
               variant="text"
        >
          {{ $t('back_to_login') }}
        </v-btn>
      </div>
    </v-form>
  </v-card>
</template>

<script setup lang="ts">
import { useUtilsStore } from '~/store/utils'
import { useAuthStore } from '~/store/auth'
import { FormRules } from '~/composables/FormRules'
import type { AuthorizationToken } from '~/composables/models/Authentication'

useHead(seoConfig('complete_signup_page_title'))

const localePath = useLocalePath()
const utilStore = useUtilsStore()
const userStore = useAuthStore()

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const first_name = ref('')
const last_name = ref('')
const password = ref('')
const repeatPassword = ref('')
const signup = async () => {
  loading.value = true
  const { error, data } = await useAPIFetch<AuthorizationToken>('api/v1/user/signup/', {
    method: 'POST',
    body: {
      email: route.params.email,
      hash_code: route.params.hash,
      first_name: first_name.value,
      last_name: last_name.value,
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

const { error } = await useAPIFetch('api/v1/user/signup/', {
  method: 'POST',
  body: {
    state: 'check',
    email: route.params.email,
    hash_code: route.params.hash,
  },
})
if (error.value) {
  throw createError({
    message: error.value.detail,
    statusCode: error.value.statusCode,
  })
}
definePageMeta({
  layout: 'empty',
})
</script>

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
          {{ $t('forgot_password__pretitle') }},
        </h4>
        <h2 class="primary--text text-center mb-5">
          {{ $t('forgot_password__title') }}
        </h2>
        <v-text-field id="id_email"
                      v-model="email"
                      :rules="emailRules"
                      label="Email"
                      required
                      type="email"
                      outlined
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
          {{ $t('send_link') }}
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

<script setup>
import { useAuthStore } from '~/store/auth'
import { useUtilsStore } from '~/store/utils'

useHead(seoConfig('forgot_password_page_title'))

const localePath = useLocalePath()
const utilStore = useUtilsStore()

const router = useRouter()
const loading = ref(false)
const email = ref('')
const emailRules = ref([v => !!v || 'Email is required'])
const login = async () => {
  loading.value = true
  const { error } = await useAPIFetch('api/v1/user/send_forgot_password/', {
    method: 'POST',
    body: {
      email: email.value,
    },
  })
  if (error.value) {
    loading.value = false
    utilStore.showApiError(error.value)
  }
  else {
    utilStore.showSuccessMessage('sent_succcessfully')
    router.push(localePath('/login'))
  }
}

definePageMeta({
  layout: 'empty',

})
</script>

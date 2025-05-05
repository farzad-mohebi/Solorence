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
            @submit.prevent="changePassword"
    >
      <v-card-text class="pb-0">
        <h4 class="text-center pt-5 mt-5 mb-3">
          {{ $t('change_password__pretitle') }},
        </h4>
        <h2 class="primary--text text-center mb-5">
          {{ $t('change_password__title') }}
        </h2>
        <v-text-field id="id_password"
                      v-model="password"
                      :rules="FormRules.notEmpty"
                      label="New Password"
                      required
                      outlined
                      type="password"
        />
        <v-text-field id="id_repeat_password"
                      v-model="repeatPassword"
                      class="mt-4"
                      :rules="FormRules.notEmpty"
                      label="Repeat Password"
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
          {{ $t('change_password') }}
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
import { FormRules } from '~/composables/FormRules'

useHead(seoConfig('forgot_password_page_title'))

const localePath = useLocalePath()
const utilStore = useUtilsStore()

const router = useRouter()
const route = useRoute()
const loading = ref<boolean>(false)
const password = ref<string>('')
const repeatPassword = ref<string>('')
const changePassword = async () => {
  loading.value = true
  const { error } = await useAPIFetch('api/v1/user/change_forgot_password/', {
    method: 'PUT',
    body: {
      new_password: password.value,
      hash_code: route.params.hash,
      hash_id: route.params.id,
    },
  })
  if (error.value) {
    loading.value = false
    utilStore.showApiError(error.value)
  }
  else {
    utilStore.showSuccessMessage('changed_succcessfully')
    router.push(localePath('/login'))
  }
}

definePageMeta({
  layout: 'empty',

})
</script>

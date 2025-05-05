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
        <h2 class="text-center my-5 ">
          {{ $t('change_password__title') }}
        </h2>

        <v-text-field id="id_current_password"
                      v-model="currentPassword"
                      :rules="passwordRules"
                      label="Current Password"
                      required
                      outlined
                      type="password"
        />

        <v-text-field id="id_new_password"
                      v-model="newPassword"
                      class="mt-2"
                      :rules="passwordRules"
                      label="New Password"
                      required
                      outlined
                      type="password"
        />

        <v-text-field id="id_repeat_password"
                      v-model="repeatPassword"
                      class="mt-2"
                      :rules="passwordRules"
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
      <div class="text-center d-flex align-center justify-center px-5 mb-5">
        <v-btn :to="localePath('/')"
               color="primary"
               variant="text"
        >
          {{ $t('back_to_home') }}
        </v-btn>
      </div>
    </v-form>
  </v-card>
</template>

<script setup>
import { useUtilsStore } from '~/store/utils'

useHead(seoConfig('forgot_password_page_title'))

const localePath = useLocalePath()
const utilStore = useUtilsStore()

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const currentPassword = ref('')
const newPassword = ref('')
const repeatPassword = ref('')
const passwordRules = ref([v => !!v || 'This field is required'])
const changePassword = async () => {
  loading.value = true
  const { error } = await useAuthAPIFetch('api/v1/user/change_password/', {
    method: 'PUT',
    body: {
      old_password: currentPassword.value,
      new_password: newPassword.value,
    },
  })
  if (error.value) {
    loading.value = false
    utilStore.showApiError(error.value)
  }
  else {
    utilStore.showSuccessMessage('password_changed_succcessfully')
    router.push(localePath('/'))
  }
}

definePageMeta({

})
</script>

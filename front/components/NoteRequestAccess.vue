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
    <v-card-text v-if="!isRequestSent">
      <p class="text-center mt-10 mb-2 text-h5 font-weight-bold text-primary">
        {{ $t('you_need_access') }}
      </p>
      <p class="text-center mt-2 mb-4">
        {{ $t('you_need_access_description') }}.
      </p>
      <v-textarea v-model="memberMessage"
                  variant="outlined"
                  :label="$t('message') + ' (' + $t('optional') + ')'"
      />
      <div class="text-center">
        <v-btn class=""
               variant="flat"
               color="primary"
               @click="requestAccess"
        >
          {{ $t('request_access') }}
        </v-btn>
      </div>
    </v-card-text>
    <v-card-text v-else>
      <p class="text-center mt-10 mb-2 text-h5 font-weight-bold text-primary">
        {{ $t('request_sent') }}
      </p>
      <p class="text-center mt-2 mb-4">
        {{ $t('request_access_sent_description') }}.
      </p>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { useUtilsStore } from '~/store/utils'

const route = useRoute()

const utilStore = useUtilsStore()
const isRequestSent = useState<boolean>('isRequestSent', () => false)
const loading = ref<boolean>(false)

const memberMessage = ref<string>('')
const requestAccess = async () => {
  loading.value = true

  const { error } = await useAuthAPIFetch(`/api/v1/note/request_access/${route.params.link}/`, {
    method: 'POST',
    body: {
      member_message: memberMessage.value,
    },
  })
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else {
    utilStore.showSuccessMessage('request_sent')
    isRequestSent.value = true
  }
  loading.value = false
}
</script>

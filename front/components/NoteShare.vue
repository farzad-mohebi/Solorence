<template>
  <div>
    <v-btn-group class="me-2"
                 color="purple"
                 density="comfortable"
                 rounded="pill"
                 divided
    >
      <v-btn class="pe-2"
             prepend-icon="mdi-account-multiple-outline"
             variant="flat"
             @click="dialog = true"
      >
        <div class="text-none font-weight-regular">
          {{ $t('share') }}
        </div>

        <v-dialog v-model="dialog"
                  max-width="500"
        >
          <v-card :loading="loading"
                  :disabled="loading"
                  rounded="lg"
          >
            <v-card-title class="d-flex justify-space-between align-center">
              <div class="text-h6 font-weight-bold ps-2">
                {{ $t('access_list') }}
              </div>
              <v-btn icon="mdi-close"
                     variant="text"
                     @click="dialog = false"
              />
            </v-card-title>

            <v-divider class="mb-4" />

            <v-card-text>
              <div class="text-medium-emphasis mb-1">
                {{ $t('grant_access_with_email') }}
              </div>
              <div class="d-flex align-center ">
                <v-btn v-if="!showGrantBox"
                       icon
                       class="me-3"
                       :disabled="grantAccess.email.length === 0 || !isValidEmail"
                       :color="grantAccess.email.length > 0 ? 'primary' : ''"
                       variant="flat"
                       @click="toggleGrantBox()"
                >
                  <v-icon icon="mdi-account-check" />
                </v-btn>
                <v-text-field v-model="grantAccess.email"
                              type="email"
                              label="Email"
                              class="ltr text-left mt-4"
                              :readonly="showGrantBox"
                              :prepend-icon="'mdi-at'"
                              variant="underlined"
                />
              </div>
              <div v-if="showGrantBox">
                <v-select v-model="grantAccess.access"
                          :label="$t('rule')"
                          class="mb-3"
                          item-value="id"
                          item-title="name"
                          hide-details
                          :items="[
                            { id: 1, name: $t('access_type_1') },
                            { id: 2, name: $t('access_type_2') },
                            { id: 3, name: $t('access_type_3') },
                          ]"
                          variant="outlined"
                />
                <v-checkbox v-model="grantAccess.is_notify"
                            color="primary"
                            :label="$t('notify_user')"
                            @change="grantAccess.owner_message = ''"
                />
                <v-textarea v-if="grantAccess.is_notify"
                            v-model="grantAccess.owner_message"
                            variant="outlined"
                            :label="$t('message_text')"
                />
              </div>
              <div v-else>
                <v-divider />
                <div class="font-weight-bold mb-2 mt-4">
                  {{ $t('people_with_access') }}:
                </div>
                <div v-if="loading" />
                <div v-for="access in accessUsers"
                     :key="access.id"
                     class="text-medium-emphasis mb-1"
                     style="max-height: 500px;"
                >
                  <div class="text-h6 mb-3 ltr mt-3 d-flex align-center justify-space-between ">
                    <div class="d-flex w-100 ltr align-center justify-content-between">
                      <div>
                        <v-icon class="mb-1"
                                color="primary"
                                size="45"
                        >
                          mdi-account-circle
                        </v-icon>
                      </div>
                      <div class="text-start ms-2">
                        <div class="text-body-1 text-black text-uppercase">
                          {{ access.user.username }}
                        </div>
                        <div class=" text-body-2">
                          {{ access.user.email }}
                        </div>
                      </div>
                      <div class="ms-auto">
                        <v-select v-model="access.access"
                                  width="140"
                                  :label="$t('rule')"
                                  class="my-2 text-caption"
                                  item-value="id"
                                  item-title="name"
                                  hide-details
                                  density="compact"
                                  :items="[
                                    { id: 1, name: $t('access_type_1') },
                                    { id: 2, name: $t('access_type_2') },
                                    { id: 3, name: $t('access_type_3') },
                                    { id: -1, name: $t('delete') },
                                  ]"
                                  variant="outlined"
                                  @update:model-value="(newValue) => updateAccess(access, newValue)"
                        />
                      </div>
                    </div>
                  </div>
                </div>
                <v-divider v-if="requestUsers.length" />
                <div v-if="requestUsers.length"
                     class="font-weight-bold mt-4"
                >
                  {{ $t('request_access') }}:
                </div>
                <div v-for="request in requestUsers"
                     :key="request.user.id"
                     class="text-medium-emphasis mb-1"
                     style="max-height: 500px;"
                >
                  <div class="text-h6 ltr mt-3 d-flex align-center justify-space-between ">
                    <div class="d-flex w-100 ltr align-center justify-content-between">
                      <div>
                        <v-icon class="mb-1"
                                color="orange"
                                size="45"
                        >
                          mdi-account-circle
                        </v-icon>
                      </div>
                      <div class="text-start ms-2">
                        <div class="text-body-1 text-black text-uppercase">
                          {{ request.user.username }}
                        </div>
                        <div class=" text-body-2">
                          {{ request.user.email }}
                        </div>
                      </div>
                      <div class="ms-auto d-flex ga-2">
                        <v-btn color="red"
                               size="small"
                               @click="answerRequest('reject', request)"
                        >
                          {{ $t('reject') }}
                        </v-btn>
                        <v-btn color="green"
                               size="small"
                               @click="answerRequest('accept', request)"
                        >
                          {{ $t('accept') }}
                        </v-btn>
                      </div>
                    </div>
                  </div>
                  <div v-if="request.member_message"
                       class=" text-body-2 mb-3"
                  >
                    <strong class="text-black"> {{ $t('message') }}: </strong>
                    {{ request.member_message }}
                  </div>
                </div>
                <v-divider />
                <div class="font-weight-bold mb-2 mt-4">
                  {{ $t('general_access') }}:
                </div>
                <v-select v-if="!loading"
                          v-model="noteConfig.status"
                          item-value="id"
                          item-title="name"
                          density="compact"
                          hide-details
                          :items="[{ id: 1, name: $t('private') }, { id: 2, name: $t('public') }]"
                          variant="outlined"
                />
                <p class="my-4 text-body-2 text-black">
                  <v-icon>
                    {{ noteConfig.status === 2 ? 'mdi-alert text-orange'
                      : 'mdi-shield-account text-green'
                    }}
                  </v-icon>
                  {{ noteConfig.status === 2 ? $t('public_description') : $t('private_description')
                  }}.
                </p>
                <v-select v-if="noteConfig.status === 2"
                          v-model="noteConfig.public_joiners_access"
                          :label="$t('rule')"
                          class="mb-3"
                          item-value="id"
                          item-title="name"
                          hide-details
                          density="compact"
                          :items="[
                            { id: 1, name: $t('access_type_1') },
                            { id: 2, name: $t('access_type_2') },
                            { id: 3, name: $t('access_type_3') },
                          ]"
                          variant="outlined"
                />
              </div>
            </v-card-text>

            <v-divider class="mt-2" />

            <v-card-actions v-if="showGrantBox"
                            class="my-2 d-block"
            >
              <v-btn class="text-none"
                     color="primary"
                     variant="flat"
                     @click="submitGrantAccess"
              >
                {{ $t('send') }}
              </v-btn>
              <v-btn class="text-none ms-2"
                     color="primary"
                     variant="tonal"
                     @click="showGrantBox = false"
              >
                {{ $t('cancel') }}
              </v-btn>
            </v-card-actions>
            <v-card-actions v-else
                            class="my-2 d-flex justify-end"
            >
              <v-btn class="text-none"
                     color="primary"
                     variant="flat"
                     @click="dialog = false"
              >
                {{ $t('done') }}
              </v-btn>
              <v-spacer />
              <v-btn class="text-none"
                     color="primary"
                     variant="outlined"
                     @click="utilStore.copyText(noteConfig.full_link, $t('copied_successfully'))"
              >
                {{ $t('copy_link') }}
                <v-icon class="ms-2">
                  mdi-link
                </v-icon>
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-btn>

      <v-btn size="small"
             icon
      >
        <v-icon icon="mdi-menu-down" />
        <v-menu activator="parent"
                location="bottom end"
                transition="fade-transition"
        >
          <v-list density="compact"
                  min-width="250"
                  rounded="lg"
                  slim
          >
            <v-list-item prepend-icon="mdi-link"
                         title="Copy link"
                         link
            />

            <v-divider class="my-2" />

            <v-list-item min-height="24">
              <template #subtitle>
                <div class="text-caption">
                  Shared with John + 1 more
                </div>
              </template>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-btn>
    </v-btn-group>
  </div>
</template>

<script setup lang="ts">
import { useUtilsStore } from '~/store/utils'

const route = useRoute()
const noteID = route.params.id

const utilStore = useUtilsStore()

const accessUsers = ref([])
const requestUsers = ref([])
const noteConfig = reactive({
  status: 1, // Private: 1   //   Public: 2
  public_joiners_access: 1, // Viewer: 1
  full_link: '',
})
const loading = ref(true)
const usersLoaded = ref(false)

const dialog = ref(false)
const isValidEmail = ref(false)
const showGrantBox = ref(false)
const grantAccess = reactive({
  email: '',
  is_notify: true,
  owner_message: '',
  access: 1,
})

watch(grantAccess, (newValue) => {
  isValidEmail.value = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(newValue.email)
  if (!newValue.is_notify && newValue.owner_message)
    grantAccess.owner_message = ''
}, {
  deep: true,
})
const watchNoteChange = ref(false)
watch(noteConfig, async () => {
  if (!watchNoteChange.value) {
    return
  }
  if (noteConfig.status === 1 && noteConfig.public_joiners_access !== 1) {
    noteConfig.public_joiners_access = 1
    return
  }
  loading.value = true
  const { error, data } = await useAuthAPIFetch(`/api/v1/note/${noteID}/update_security/`, {
    method: 'PUT',
    body: {
      status: noteConfig.status,
      public_joiners_access: noteConfig.public_joiners_access,
    },
  })
  loading.value = false
  if (error.value) {
    return utilStore.showApiError(error.value)
  }
  else {
    utilStore.showSuccessMessage('updated_successfully')
    noteConfig['status'] = data.value.status
    noteConfig['public_joiners_access'] = data.value.public_joiners_access
    noteConfig['link'] = data.value.link
  }
}, {
  deep: true,
})
const submitGrantAccess = async () => {
  if (!isValidEmail.value)
    return utilStore.showErrorMessage('invalid_email_error')
  loading.value = true
  const { error } = await useAuthAPIFetch(`/api/v1/note/${noteID}/grant_user/`, {
    method: 'POST',
    body: {
      email: grantAccess.email,
      is_notify: grantAccess.is_notify,
      owner_message: grantAccess.owner_message,
      access: grantAccess.access,
    },
  })
  loading.value = false
  if (error.value) {
    return utilStore.showApiError(error.value)
  }
  else {
    utilStore.showSuccessMessage('user_granted')
    grantAccess['email'] = ''
    grantAccess['is_notify'] = true
    grantAccess['owner_message'] = ''
    grantAccess['access'] = 1
    showGrantBox.value = false
    await loadUsers()
  }
}
const toggleGrantBox = () => {
  showGrantBox.value = true
}
const updateAccess = async (access, newValue) => {
  loading.value = true
  const { error } = await useAuthAPIFetch(`/api/v1/note/update_access/${access.id}/`, {
    method: 'PUT',
    body: {
      access: newValue,
    },
  })
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else {
    utilStore.showSuccessMessage('updated_successfully')
  }
  await loadUsers()
}
const loadUsers = async () => {
  loading.value = true
  watchNoteChange.value = false
  const { error, data } = await useAuthAPIFetch(`/api/v1/note/get_access_config/${noteID}/`)
  loading.value = false
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else {
    usersLoaded.value = true
    accessUsers.value = data.value.users
    requestUsers.value = data.value.requests
    noteConfig.status = data.value.config.status
    noteConfig.public_joiners_access = data.value.config.public_joiners_access

    if (data.value.config.link)
      noteConfig.full_link = location.origin + '/note/link/' + data.value.config.link
  }
}

const answerRequest = async (answer, request) => {
  loading.value = true
  const { error } = await useAuthAPIFetch(`/api/v1/note/answer_request_access/${request.id}/`, {
    method: 'POST',
    body: {
      answer,
    },
  })
  loading.value = false
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else {
    utilStore.showSuccessMessage('done_successfully')
  }
  loadUsers()
}

watch(dialog, async (newValue) => {
  if (newValue && !usersLoaded.value) {
    await loadUsers()
    if (watchNoteChange.value === false) {
      watchNoteChange.value = true
    }
  }
})
</script>

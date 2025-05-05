<template>
  <div class="d-flex align-center justify-space-between mb-5 px-3 py-2 bg-white border rounded-lg">
    <div class="text-h6 my-2  d-flex align-center justify-space-between ">
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
            {{ authStore.info.first_name }} {{
              authStore.info.last_name }}
          </div>
        </div>
      </div>
    </div>
    <div class="d-flex ga-4 align-center justify-center">
      <v-dialog v-model="dialog"
                width="auto"
                persistent
                max-width="400"
      >
        <v-card :loading="loading"
                max-width="400"
                prepend-icon="mdi-alert"
                :text="$t('delete_sure')"
                :title="$t('deleting') + '!'"
        >
          <template #actions>
            <v-spacer />
            <v-btn variant="plain"
                   @click="dialog = false"
            >
              {{ $t('cancel') }}
            </v-btn>
            <v-btn variant="elevated"
                   color="red"
                   @click="removeTemplate"
            >
              {{ $t('yes_delete_it') }}
            </v-btn>
          </template>
        </v-card>
      </v-dialog>
      <div class="mt-2" />
      <LanguageChange />
      <TemplateShare />
      <v-menu>
        <template #activator="{ props }">
          <v-btn id="id-show-template-toolbar"
                 icon="mdi-dots-vertical"
                 variant="text"
                 v-bind="props"
          />
        </template>

        <v-list class="less-prepend-space">
          <!-- <v-list-item @click="duplicateTemplate">
                        <template v-slot:prepend>
                            <v-icon>mdi-content-duplicate</v-icon>
                        </template>
                        <v-list-item-title>
                            {{ $t('duplicate_note') }}
                        </v-list-item-title>
                    </v-list-item> -->
          <v-list-item @click="redoChanges">
            <template #prepend>
              <v-icon color="orange">
                mdi-redo
              </v-icon>
            </template>
            <v-list-item-title class="text-orange">
              {{ $t('revert_changes') }}
            </v-list-item-title>
          </v-list-item>
          <v-list-item id="id-template-delete"
                       @click="dialog = true"
          >
            <template #prepend>
              <v-icon color="red">
                mdi-delete
              </v-icon>
            </template>
            <v-list-item-title class="text-red">
              {{ $t('delete') }}
            </v-list-item-title>
          </v-list-item>
          <!-- <v-list-item>
                        <template v-slot:prepend>
                            <v-icon>mdi-cogs</v-icon>
                        </template>
                        <v-list-item-title>
                            {{ $t('settings') }}
                        </v-list-item-title>
                    </v-list-item> -->
        </v-list>
      </v-menu>
      <v-btn color="black"
             icon="mdi-home"
             :to="localePath('/home')"
             variant="text"
      />
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '~/store/auth'
import { useUtilsStore } from '~/store/utils'

const utilStore = useUtilsStore()
const route = useRoute()
const dialog = ref(false)
const localePath = useLocalePath()
const authStore = useAuthStore()
const emit = defineEmits(['revertTemplate', 'enableLoading', 'disableLoading'])

const removeTemplate = async () => {
  emit('enableLoading')
  const { error } = await useAuthAPIFetch(`/api/v1/template/${route.params.id}/`, {
    method: 'DELETE',
  })
  if (error.value) {
    utilStore.showApiError(error.value)
    emit('disableLoading')
  }
  else {
    utilStore.showSuccessMessage('deleted_successfully')
    navigateTo(localePath('/home'))
  }
}

const redoChanges = async () => {
  emit('revertTemplate')
}
</script>

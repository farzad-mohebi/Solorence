<template>
  <div>
    <v-dialog v-model="showNoteAttachments"
              max-width="500"
    >
      <v-card :loading="loading"
              :disabled="loading"
              rounded="lg"
      >
        <v-card-title class="d-flex justify-space-between align-center">
          <div class="text-h6 font-weight-bold ps-2">
            {{ $t('attachments') }}
          </div>
          <v-btn icon="mdi-file-document-multiple-outline"
                 variant="text"
                 @click="showNoteAttachments = false"
          />
        </v-card-title>

        <v-divider class="mb-4" />

        <v-card-text />

        <v-divider class="mt-2" />

        <v-card-actions class="my-2 d-block">
          <v-btn class="text-none"
                 color="primary"
                 variant="flat"
          >
            {{ $t('send') }}
          </v-btn>
          <v-btn class="text-none ms-2"
                 color="primary"
                 variant="tonal"
                 @click="showNoteAttachments = false"
          >
            {{ $t('cancel') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
const showNoteAttachments = useState('showNoteAttachments', () => false)

const loading = ref(true)
</script>

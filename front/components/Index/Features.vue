<template>
  <v-container max-width="1200">
    <v-slide-group
      v-model="selectedSlide"
      class="mt-10"
      show-arrows
      centered
    >
      <v-slide-group-item
        v-for="item in slideList"
        :key="item.key"
        v-slot="{ isSelected, toggle }"
        center-active
        centered
      >
        <div class="text-center mx-5">
          <div>
            <v-btn
              color="primary"
              :variant="isSelected ? 'flat' : 'tonal'"
              class="ma-2"
              icon
              rounded="xl"
              size="x-large"
              @click="toggle"
            >
              <v-icon size="large">
                mdi-{{ item.icon }}
              </v-icon>
            </v-btn>
          </div>
          <div>
            {{ $t(item.key) }}
          </div>
        </div>
      </v-slide-group-item>
    </v-slide-group>
    <div class="mt-5">
      <!-- <v-img width="100%"
             min-height="400"
             src="image/index-features/paragraph.png"
      /> -->
      <VCard class="mt-10">
        <v-img
          aspect-ratio="1920/1080"
          :src="`/images/index-features/${slideList[selectedSlide].key}.jpg`"
        />
      </VCard>
    </div>
  </v-container>
</template>

<script setup lang="ts">
const selectedSlide = ref(0)
const slideList = ref([
  { key: 'paragraph', icon: 'format-paragraph' },
  { key: 'image', icon: 'image' },
  { key: 'attachment', icon: 'attachment' },
  { key: 'goal', icon: 'target' },
  { key: 'journey', icon: 'road-variant' },
  { key: 'meet', icon: 'account-group' },
  { key: 'tasks', icon: 'checkbox-marked' },
  { key: 'calendar', icon: 'calendar-month' },
  { key: 'shared_notes', icon: 'notebook-outline' },
  { key: 'board', icon: 'artboard' },
  { key: 'table', icon: 'table' },
])
</script>

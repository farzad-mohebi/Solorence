<template>
  <v-menu v-model="mentionMenuShow"
          class="w-100 left-overly-editor"
          :close-on-content-click="false"
          location="start"
          :target="mentionMenuTarget"
          min-width="400"
  >
    <v-container max-width="1340">
      <v-card class="w-100"
              :loading="loading"
              :disabled="loading"
      >
        <div v-if="!loading && !mentionableUsers.length">
          <v-card-text class="text-center text-red font-weight-bold pb-0 fs-3">
            No user founded !
          </v-card-text>
        </div>
        <template v-if="!loading">
          <v-card-text class="pb-0">
            <v-text-field ref="searchInput"
                          v-model="search"
                          hide-details=""
                          density="compact"
                          placeholder="Search here ..."
                          prepend-inner-icon="mdi-magnify"
                          variant="outlined"
            />
          </v-card-text>
          <v-list v-model:selected="selectedUsers"
                  select-strategy="leaf"
          >
            <v-list-item v-for="(user, i) in filteredUsers"
                         :key="i"
                         class="py-2"
                         :title="user.name"
                         :value="user"
                         :subtitle="user.username"
            >
              <template #prepend="{ isSelected }">
                <v-list-item-action start>
                  <v-checkbox-btn :model-value="isSelected"
                                  @input="checkSelectAll"
                  />
                  <!-- <v-avatar :image="user.prependAvatar"></v-avatar> -->
                </v-list-item-action>
              </template>
            </v-list-item>
          </v-list>
        </template>
        <div v-else>
          <v-skeleton-loader v-for="_ in 5"
                             :key="_"
                             type="list-item-avatar"
          />
        </div>
        <v-card-actions v-if="loading || mentionableUsers.length">
          <v-checkbox-btn v-model="selectAllState"
                          label="all"
                          @update:model-value="selectAll"
          />
          <v-btn variant="text"
                 @click="mentionMenuShow = false;"
          >
            Cancel
          </v-btn>
          <v-btn color="primary"
                 :disabled="selectedUsers.length === 0"
                 variant="flat"
                 @click="submitMention()"
          >
            Mention <template v-if="selectAllState && selectedUsers.length > 1">
              All
            </template>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-container>
  </v-menu>
</template>

<script setup>
import { useUtilsStore } from '~/store/utils'

const currentAnchor = useState('currentAnchor', () => null)
const selectedElement = useState('selectedElement', () => null)
const selectedNode = useState('selectedNode', () => null)

const utilStore = useUtilsStore()
const route = useRoute()
const loading = ref(true)
const search = ref('')
const searchInput = ref(null)
const mentionMenuTarget = useState('mentionMenuTarget', () => null)
const mentionMenuShow = useState('mentionMenuShow', () => null)
const selectAllState = ref(false)
const mentionableUsers = ref([])
const filteredUsers = ref([])
const selectedUsers = ref([])
const submitMention = async () => {
  loading.value = true
  const { error } = await useAuthAPIFetch(`/api/v1/notification/`, {
    method: 'POST',
    body: {
      note: route.params.id,
      receivers: selectedUsers.value.map(user => user.id),
      text: 'You Mentioned!',
    },
  })
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else {
    addMention(selectedUsers.value)
    mentionMenuShow.value = false
    utilStore.showSuccessMessage('mention_success')
  }
  loading.value = false
}
const loadUsers = async () => {
  search.value = ''
  const { error, data } = await useAuthAPIFetch(`/api/v1/note/get_users/${route.params.id}/`)
  loading.value = false
  if (error.value) {
    utilStore.showApiError(error.value)
  }
  else {
    mentionableUsers.value = data.value.map((user) => {
      return {
        id: user.id,
        name: user.first_name + ' ' + user.last_name,
        username: user.username,
        email: user.email,
      }
    })
    filteredUsers.value = mentionableUsers.value
    setTimeout(() => {
      console.log(searchInput.value)
      searchInput.value.focus()
    }, 300)
  }
}
const checkSelectAll = () => {
  if (selectedUsers.value.length === mentionableUsers.value.length)
    selectAllState.value = true
  else
    selectAllState.value = false
}
const selectAll = () => {
  if (selectAllState.value)
    selectedUsers.value = mentionableUsers.value
  else
    selectedUsers.value = []
}

watch(mentionMenuShow, () => {
  filteredUsers.value = mentionableUsers.value
  search.value = ''
  selectedUsers.value = []
  selectAllState.value = false
  if (mentionMenuShow.value === true && loading.value === true) {
    loadUsers()
  }
})
watch(search, () => {
  if (search.value) {
    filteredUsers.value = mentionableUsers.value.filter(user => JSON.stringify(user).includes(search.value))
  }
})
const addMention = (users) => {
  console.log('users', users)
  console.log('selectedNode', selectedNode.value)
  const textHTML = users.map(user => ` &nbsp; <mark>@${user.username}</mark> &nbsp; `)
  console.log('textHTML', textHTML)
  if (selectedNode.value) {
    // Get the parent element of the text node
    const parentNode = selectedNode.value.parentNode

    // Get the text before and after the insertion point
    const beforeText = selectedNode.value.data.slice(0, currentAnchor - 1)
    const afterText = selectedNode.value.data.slice(currentAnchor - 1) || ' '

    // Create a new span element to hold the HTML content
    const newNode = document.createElement('span')
    newNode.innerHTML = `${beforeText} ${textHTML} ${afterText}`
    // Replace the original text node with the new HTML element
    parentNode.replaceChild(newNode, selectedNode.value)
    // selectedNode.value.data = selectedNode.value.data.slice(0, currentAnchor - 1) + ` <mark>@${item.title}</mark> &nbsp;` + (selectedNode.value.data.slice(currentAnchor - 1) || ' ')
  }
  else {
    selectedElement.value.innerHTML = selectedElement.value.innerHTML.slice(0, currentAnchor - 1) + ` ${textHTML} ` + (selectedElement.value.innerHTML.slice(currentAnchor - 1) || ' ')
  }
}
</script>

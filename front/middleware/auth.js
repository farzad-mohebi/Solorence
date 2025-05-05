import { useAuthStore } from '~/store/auth'

export default defineNuxtRouteMiddleware(async () => {
  if (import.meta.client) return
  const authStore = useAuthStore()
  if (!authStore.isAuthenticated) {
    return navigateTo('/login')
  }
  await authStore.getMyInfo()
  if (!authStore.info.id) {
    authStore.logUserOut()
    return navigateTo('/login')
  }
})

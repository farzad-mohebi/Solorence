import { defineStore } from 'pinia'
import type { AuthorizationToken } from '~/composables/models/Authentication'
import type { UserInfo } from '~/composables/models/User'

const SESSION_KEY = 'session_key'
const GOOGLE_CALENDAR_ACCESS_KEY = 'google_calendar_key'
const REFRESH_KEY = 'refresh_key'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    authenticated: false as boolean,
    calendarAccess: false as boolean,
    loading: false as boolean,
    showGoogleCalendarAuth: false as boolean,
    info: null as UserInfo | null,
  }),
  actions: {
    setAuth(tokens: AuthorizationToken) {
      const token = useCookie(SESSION_KEY) // useCookie new hook in nuxt 3
      token.value = tokens.access // set token to cookie

      const refresh = useCookie(REFRESH_KEY) // useCookie new hook in nuxt 3
      refresh.value = tokens.refresh // set token to cookie

      this.authenticated = true // set authenticated  state value to true
    },
    setGoogleAuth(tokens: AuthorizationToken) {
      const token = useCookie(SESSION_KEY) // useCookie new hook in nuxt 3
      token.value = tokens.access // set token to cookie

      const refresh = useCookie(REFRESH_KEY) // useCookie new hook in nuxt 3
      refresh.value = tokens.refresh // set token to cookie

      this.authenticated = true // set authenticated  state value to true
    },
    setGoogleCalendarToken(access_token: string) {
      const token = useCookie(GOOGLE_CALENDAR_ACCESS_KEY)
      token.value = access_token
      this.calendarAccess = true
      this.showGoogleCalendarAuth = false
    },
    askGoogleToken() {
      this.showGoogleCalendarAuth = true
    },
    logUserOut(navigate = false) {
      const localePath = useLocalePath()
      const token = useCookie(SESSION_KEY) // useCookie new hook in nuxt 3
      const refreshToken = useCookie(REFRESH_KEY) // useCookie new hook in nuxt 3
      const calendarToken = useCookie(GOOGLE_CALENDAR_ACCESS_KEY)
      this.authenticated = false // set authenticated  state value to false
      token.value = null // clear the token cookie
      refreshToken.value = null // clear the token cookie
      calendarToken.value = null // clear the token cookie
      this.info = null
      this.calendarAccess = false
      this.showGoogleCalendarAuth = false
      if (navigate || import.meta.client) {
        navigateTo(localePath('/login'))
      }
    },
    // async authenticateUser({ username, password }) {
    //   // useFetch from nuxt 3
    //   const { data, pending } = await useFetch(
    //     "https://dummyjson.com/auth/login",
    //     {
    //       method: "post",
    //       headers: { "Content-Type": "application/json" },
    //       body: {
    //         username,
    //         password,
    //       },
    //     }
    //   );
    //   this.loading = pending;
    //   if (data.value) {
    //     const token = useCookie("token"); // useCookie new hook in nuxt 3
    //     token.value = data?.value?.token; // set token to cookie
    //     this.authenticated = true; // set authenticated  state value to true
    //   }
    // },
    async getMyInfo() {
      if (!this.info) {
        const { data, pending } = await useAuthAPIFetch('/api/v1/user/self/', {
          method: 'get',
        })
        this.loading = pending.value
        if (data.value) {
          this.info = data.value as unknown as UserInfo
        }
      }
    },
  },
  getters: {
    getToken: () => {
      const token = useCookie(SESSION_KEY)
      return token.value
    },
    getGoogleAccessToken: () => {
      const token = useCookie(GOOGLE_CALENDAR_ACCESS_KEY)
      return token.value
    },
    getInfo: (state) => {
      return state.info
    },
    isAuthenticated: (state) => {
      const token = useCookie(SESSION_KEY)
      state.authenticated = (token.value && token.value.length > 0) || false
      return state.authenticated
    },
  },
})

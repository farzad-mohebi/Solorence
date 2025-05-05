import type { UseFetchOptions } from '#app'
import { useAuthStore } from '~/store/auth'

export const useAPIFetch = <T>(path: string, options: UseFetchOptions<T> = {}) => {
  const config = useRuntimeConfig()
  options.baseURL = config.public.baseURL
  return useFetch<T>(path, options as object)
}

export const useAuthAPIFetch = <T>(path: string, options: UseFetchOptions<T> = {}) => {
  const config = useRuntimeConfig()
  const auth = useAuthStore()

  options.baseURL = config.public.baseURL
  options.headers = {
    ...options?.headers,
    authorization: `Bearer ${auth.getToken}`,
  }

  return useFetch<T>(path, options as object)
}

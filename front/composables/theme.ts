import { useTheme } from 'vuetify'

export const toggleTheme = () => {
  const cookieTheme = useCookie('theme')
  cookieTheme.value = cookieTheme.value === 'dark' ? 'light' : 'dark'

  const theme = useTheme()
  theme.global.name.value = cookieTheme.value
}

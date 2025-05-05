// import this after install `@mdi/font` package

import '@mdi/font/css/materialdesignicons.css'
import { VTimePicker } from 'vuetify/labs/VTimePicker'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import colors from 'vuetify/util/colors'
import { VCalendar } from 'vuetify/labs/VCalendar'
import { VDateInput } from 'vuetify/labs/VDateInput'
// @ts-ignore
// const data = myi18n()['messages'];

export default defineNuxtPlugin((app) => {
  const vuetify = createVuetify({
    components: {
      VCalendar,
      VTimePicker,
      VDateInput,
    },
    locale: {
      locale: 'en',
      fallback: 'en',
      messages: {
        fa: {
          open: 'باز کردن',
          close: 'بستن',
          loading: 'درحال بارگذاری',

        },
      },
      rtl: {
        fa: true,
      },
    },
    theme: {
      themes: {
        light: {
          dark: false,
          colors: {
            background: '#fafafa',
            primary: colors.brown.base,
            accent: colors.grey.darken3,
            secondary: colors.amber.darken3,
            info: colors.teal.lighten1,
            warning: colors.amber.base,
            error: colors.deepOrange.accent4,
            success: colors.green.accent3,
          },
        },
        dark: {
          dark: true,
          colors: {
            primary: colors.brown.base,
            accent: colors.grey.darken3,
            secondary: colors.amber.darken3,
            info: colors.teal.lighten1,
            warning: colors.amber.base,
            error: colors.deepOrange.accent4,
            success: colors.green.accent3,
          },
        },
      },
    },
  })
  app.vueApp.use(vuetify)
})

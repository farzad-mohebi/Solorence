// https://nuxt.com/docs/api/configuration/nuxt-config
import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'

export default defineNuxtConfig({
  modules: [
    '@nuxt/eslint',
    '@unlok-co/nuxt-stripe',
    '@nuxtjs/i18n',
    'nuxt-vue3-google-signin',
    '@pinia/nuxt',
    (_options, nuxt) => {
      nuxt.hooks.hook('vite:extendConfig', (config) => {
        // @ts-ignore
        config.plugins.push(vuetify({ autoImport: true }))
      })
    },
    // ...
  ],
  plugins: [
  ],
  devtools: { enabled: true },
  app: {
    head: {
      script: [
        {
          src: 'https://apis.google.com/js/api.js', async: true, defer: true,
          // onload: 'gapiLoaded()'
        },
        {
          src: 'https://accounts.google.com/gsi/client', async: true, defer: true,
          //  onload: 'gisLoaded()'
        },
      ],
    },
    layoutTransition: {
      name: 'layout',
      mode: 'out-in',
    },
    pageTransition: { name: 'page', mode: 'out-in' },
  },
  css: [
    '@/assets/css/main.css',
  ],
  runtimeConfig: {
    public: {
      baseURL: process.env.BACKEND_URL,
      googleClientID: process.env.GOOGLE_CLIENT_ID,
    },
  },
  build: {
    transpile: ['vuetify'],
  },
  routeRules: {
    // Admin dashboard renders only on client-side
    '/ssrf/**': { ssr: false },
  },
  compatibilityDate: '2024-04-03',
  vite: {
    vue: {
      template: {
        transformAssetUrls,
      },
    },
  },
  eslint: {
    config: {
      stylistic: true, // <---
    },
  },
  googleSignIn: {
    clientId: process.env.GOOGLE_CLIENT_ID,

  },
  i18n: {
    baseUrl: 'https://consultnote.com',
    vueI18n: './i18n.config.ts',
    locales: [
      { code: 'en', iso: 'en-US' },
      { code: 'fa', iso: 'fa-IR' },
      { code: 'fi', iso: 'fi-FI' },
    ],
    defaultLocale: 'en',
  },
  stripe: {
    client: {
      key: process.env.STRIPE_PUBLISHABLE_KEY,
      options: {},
    },
  },
})

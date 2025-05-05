import { defineStore } from 'pinia'

export const useUtilsStore = defineStore('utils', {
  state: () => ({
    message: {
      text: '',
      color: 'primary',
      timeout: 5000,
      show: false,
    },
  }),
  actions: {
    showMessage(text: any, color = 'primary', timeout = 5000) {
      this.message = {
        text,
        color: color,
        timeout,
        show: true,
      }
    },
    showSuccessMessage(text = 'Operation done successfully!', timeout = 5000) {
      this.showMessage(text, 'green', timeout)
    },
    showErrorMessage(text = 'Some error happened!', timeout = 5000) {
      this.showMessage(text, 'red', timeout)
    },
    showApiError(error: any, timeout = 5000) {
      console.log('showApiError', error)
      if (error.data) {
        if (error.data.detail) {
          this.showErrorMessage(error.data.detail)
        }
        else {
          this.showErrorMessage(error.data)
        }
      }
      else {
        this.showErrorMessage(error)
      }
    },
    copyText(text: string, success_message = 'Copied successfully!') {
      navigator.clipboard.writeText(text)
      this.showSuccessMessage(success_message)
    },
  },
  getters: {
    getMessage: (state) => {
      return state.message
    },
    formRules: () => {
      return {
        notEmpty: [(v: string | null) => !!v || 'This field is required'],
      }
    },
  },
})

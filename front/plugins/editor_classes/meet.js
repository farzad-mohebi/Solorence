import { stringifyDatetime } from '~/composables/custom_functions'

export default class Meet {
  static get isReadOnlySupported() {
    return true
  }

  static get toolbox() {
    return {
      title: 'Meet',
      icon: '<i class="mdi-check-circle-outline mdi v-icon notranslate text-black v-theme--light" aria-hidden="true" style="font-size: 18px; height: 18px; width: 18px;"></i>',
    }
  }

  constructor({ data, api, config, readOnly }) {
    this.readOnly = readOnly
    this.data = data

    if (!this.data?.uid) {
      this.data = {
        uid: null,
        data: {},
      }
    }
    this.api = api
    this.config = config
    this.wrapper = undefined
  }

  _initHTML() {
    if (!this.data.uid) {
      this.wrapper.innerHTML = ``
      return
    }
    const statusPlace = {
      0: 'None',
      1: 'Google Meet',
      2: 'Zoom',
      3: 'Location',
      4: 'Link',
    }
    const placeIcon = {
      0: `<i style="width: 45px;margin-right: 10px;" class="mdi-laptop-account text-blue mdi v-icon notranslate v-theme--light v-icon--size-x-large" aria-hidden="true" density="default"></i>`,
      1: `<svg style="width: 45px;margin-right: 10px;" xmlns="http://www.w3.org/2000/svg" aria-label="Google Meet" role="img" viewBox="0 0 512 512"><rect width="512" height="512" rx="15%" fill="#ffffff"/><path d="M166 106v90h-90" fill="#ea4335"/><path d="M166 106v90h120v62l90-73v-49q0-30-30-30" fill="#ffba00"/><path d="M164 406v-90h122v-60l90 71v49q0 30-30 30" fill="#00ac47"/><path d="M286 256l90-73v146" fill="#00832d"/><path d="M376 183l42-34c9-7 18-7 18 7v200c0 14-9 14-18 7l-42-34" fill="#00ac47"/><path d="M76 314v62q0 30 30 30h60v-92" fill="#0066da"/><path d="M76 196h90v120h-90" fill="#2684fc"/></svg>`,
      2: `<svg style="width: 45px;margin-right: 10px;" xmlns="http://www.w3.org/2000/svg" height="45" viewBox="0 0 472.4 472.4" width="45"><circle cx="236.2" cy="236.2" fill="#4a8cff" r="236.2"/><path d="m84.65 162.25v111a45.42 45.42 0 0 0 45.6 45.2h161.8a8.26 8.26 0 0 0 8.3-8.2v-111a45.42 45.42 0 0 0 -45.6-45.2h-161.75a8.26 8.26 0 0 0 -8.35 8.2zm226 43.3 66.8-48.8c5.8-4.81 10.3-3.6 10.3 5.1v148.8c0 9.9-5.5 8.7-10.3 5.09l-66.8-48.69z" fill="#fff"/><script xmlns=""/></svg>`,
      3: `<i style="width: 45px;margin-right: 10px;" class="mdi-map-marker text-blue mdi v-icon notranslate v-theme--light v-icon--size-x-large" aria-hidden="true" density="default"></i>`,
      4: `<i style="width: 45px;margin-right: 10px;" class="mdi-link mdi text-blue v-icon notranslate v-theme--light v-icon--size-x-large" aria-hidden="true" density="default"></i>`,
    }
    this.wrapper.innerHTML = `
  <div class="meet-card v-card v-theme--light v-card--density-default bg-light-blue-lighten-5 my-2" data-id="${
    this.data.uid
  }">
    <div class="v-card-item">
      <div class="v-card-item__prepend">
        ${placeIcon[this.data.place]}
      </div>
      <div class="v-card-item__content">
        <div class="v-card-title">
          ${this.data.title}
        </div>
        <div class="v-card-subtitle font-weight-bold text-light-blue-darken-3">
          Start At: ${stringifyDatetime(new Date(this.data.start_at))}
        </div>
      </div>
    </div>
    <div class="v-card-text ${!this.data.description ? 'd-none' : ''}">
      ${this.data.description}
    </div>
    <div class="v-card-text pt-0 ${
      this.data.address && [1, 2, 4].includes(this.data.place) ? '' : 'd-none'
    }">
      <a href="${this.data.address}" target="_blank">
        ${this.data.address}
      </a>
    </div>
    <div class="v-card-text pt-0 ${
      this.data.address && [0, 3].includes(this.data.place) ? '' : 'd-none'
    }">
        Location: ${this.data.address}
    </div>
  </div>      
            `
    this.wrapper.querySelector('.meet-card').onclick = () => {
      const meetID = this.wrapper
        .querySelector('.meet-card')
        .getAttribute('data-id')
      window['update_meet_' + meetID] = (result) => {
        if (result === 'deleted') {
          this.wrapper.remove()
          this.data = {}
        }
        else {
          result.uid = result.id
          delete result.id
          this.data = result
          this._initHTML()
        }
      }
      this.config.nuxtApp.showMeet(meetID)
    }
  }

  render() {
    this.wrapper = document.createElement('div')
    this.wrapper.setAttribute('class', 'meet-holder')
    if (!this.data?.uid) {
      this.wrapper.innerHTML = `Waiting for meet...`
      window['set_meet_state'] = (state, result = null) => {
        console.log('set_meet_state', state, result)
        if (state === 'cancel') {
          try {
            this.wrapper.remove()
            this.data = {}
          }
          catch (e) {
            console.log(e)
          }
        }
        else if (state === 'set') {
          result.uid = result.id
          delete result.id
          this.data = result
          this._initHTML()
        }
        delete window['set_meet_state']
      }
      this.config.nuxtApp.showCreateMeet()
    }
    else {
      this._initHTML()
    }
    return this.wrapper
  }

  destroy() {
    console.log('destroy wrf')
  }

  save(blockContent) {
    return this.data
  }
}

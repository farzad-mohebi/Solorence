export default class GoogleMeet {
  static get isReadOnlySupported() {
    return true
  }

  static get toolbox() {
    return {
      title: 'Google Meet',
      icon: '<svg xmlns="http://www.w3.org/2000/svg" aria-label="Google Meet" role="img" viewBox="0 0 512 512"><rect width="512" height="512" rx="15%" fill="#ffffff"/><path d="M166 106v90h-90" fill="#ea4335"/><path d="M166 106v90h120v62l90-73v-49q0-30-30-30" fill="#ffba00"/><path d="M164 406v-90h122v-60l90 71v49q0 30-30 30" fill="#00ac47"/><path d="M286 256l90-73v146" fill="#00832d"/><path d="M376 183l42-34c9-7 18-7 18 7v200c0 14-9 14-18 7l-42-34" fill="#00ac47"/><path d="M76 314v62q0 30 30 30h60v-92" fill="#0066da"/><path d="M76 196h90v120h-90" fill="#2684fc"/></svg>',
    }
  }

  constructor({ data, api, config, readOnly }) {
    this.readOnly = readOnly
    this.data = data
    this.api = api
    this.config = config
    this.wrapper = undefined
  }

  render() {
    this.wrapper = document.createElement('div')
    this.wrapper.setAttribute('class', 'pa-3 mb-5 bg-white border')
    this.wrapper.innerHTML = `
      <div class="v-card-item google-meet-card" style="">
        <div class="v-card-item__prepend">
          <div class="v-avatar v-theme--light me-2 v-avatar--density-default v-avatar--variant-flat" style="width: 50px; height: 50px;"><div class="v-responsive v-img" aria-label="">
            <div class="v-responsive__sizer" style="padding-bottom: 100%;"></div>
            <img class="v-img__img v-img__img--cover" src="/svg/google-meet.svg" alt="" style="">
          </div>
          <span class="v-avatar__underlay"></span></div>
        </div>
        <form class="v-card-item__content meet-form overflow-visible" >
          <input required value="" size="1" type="text" placeholder="Meet title..." class="v-field__input input-meet-title pa-1 ma-1 d-complete-hide">
          <input value="" size="1" type="text" placeholder="meet.google.com/abc-mnop-xyz" class="v-field__input input-meet-link pa-1 ma-1 d-complete-hide">
          <button type="button" class="v-btn me-2 create-meet d-none text-decoration-none v-theme--light text-black v-btn--density-default v-btn--size-small v-btn--variant-tonal" target="_blank">
            <span class="v-btn__overlay"></span>
            <span class="v-btn__underlay"></span>
            <span class="v-btn__content" data-no-activator="">
              Generate a Link
            </span>
          </button>
          <div class="d-flex">
            <input required value="" size="1" type="date" placeholder="Pick a Date..." class="v-field__input input-meet-date pa-1 ma-1 d-complete-hide">
            <input required value="" size="1" type="time" placeholder="Pick a Time..." class="v-field__input input-meet-time pa-1 ma-1 d-complete-hide">
            <div class="d-complete-hide align-center">
              <input required value="45" style="width: 35px" size="1" type="text" placeholder="" class="v-field__input input-meet-duration pa-1 mx-1 d-complete-hide">
              Minutes
            </div>
          </div>
          <button type="submit" class="v-btn d-complete-hide my-2 v-btn--elevated v-theme--light bg-primary v-btn--density-default v-btn--size-small v-btn--variant-elevated me-2" style="">
            <span class="v-btn__overlay"></span>
            <span class="v-btn__underlay"></span>
            <span class="v-btn__content" data-no-activator="">
              Set Meet
            </span>
          </button>
          <div class="v-card-title d-complete-show meet-title" style=""></div>
          <div class="v-card-subtitle d-complete-show" style=""><strong class="me-2 meet-time"></strong> at Google Meet</div>
          <button type="button" class="v-btn d-scheduled-hide set-in-calendar mt-2 v-theme--light mb-2 bg-green v-btn--density-default v-btn--size-small me-2" style="">
            <span class="v-btn__overlay"></span>
            <span class="v-btn__underlay"></span>
            <span class="v-btn__content" data-no-activator="">
              Schedule at Google Calendar
            </span>
          </button>
          <div class="v-card-subtitle d-scheduled-show" style="">Scheduled in your Google Calendar</div>
        </form>
        <div class="d-flex">
          <button type="button" class="v-btn me-2 meet-edit d-complete-show text-decoration-none v-btn--icon v-theme--light text-black v-btn--density-default v-btn--size-small v-btn--variant-tonal" target="_blank">
            <span class="v-btn__overlay"></span>
            <span class="v-btn__underlay"></span>
            <span class="v-btn__content" data-no-activator="">
              <i class="mdi-pencil mdi v-icon notranslate v-theme--light v-icon--size-large" aria-hidden="true"></i>
            </span>
          </button>
          <a class="v-btn d-complete-show text-decoration-none v-btn--icon v-theme--light meet-link-href text-black v-btn--density-default v-btn--size-small v-btn--variant-tonal" href="/" target="_blank">
            <span class="v-btn__overlay"></span>
            <span class="v-btn__underlay"></span>
            <span class="v-btn__content" data-no-activator="">
              <i class="mdi-open-in-new mdi v-icon notranslate v-theme--light v-icon--size-large" aria-hidden="true"></i>
            </span>
          </a>
        </div>
      </div>`
    if (this.data.googleCalendarData?.id) {
      this.wrapper
        .querySelector('.google-meet-card')
        .classList.add('scheduled')
    }
    this.wrapper
      .querySelector('.meet-form')
      .addEventListener('submit', (event) => {
        event.preventDefault()
        this._complete()
      })

    this.wrapper.querySelector('.meet-edit').addEventListener('click', () => {
      this._edit()
    })

    this.wrapper
      .querySelector('.set-in-calendar')
      .addEventListener('click', () => {
        this._setToCalendar()
      })

    // this.wrapper
    //   .querySelector(".create-meet")
    //   .addEventListener("click", async () => {
    //     const link = await this.config.nuxtApp.createMeet();
    //     if (link) {
    //       this.wrapper.querySelector(".create-meet").classList.add("d-none");
    //       this.wrapper.querySelector(".create-meet").value = link;
    //     }
    //   });

    if (this.data.show) {
      this._fillWrapperForm()
      this._complete()
    }
    else {
      this.wrapper.querySelector('.input-meet-date').value = new Date()
        .toISOString('en')
        .split('T')[0]
      this.data.date = this.wrapper.querySelector('.input-meet-date').value
      this.wrapper.querySelector('.input-meet-time').value
        = new Date().getHours() + 1 + ':00' + ' (' + this.data.duration + 'min)'
      this.data.time = this.wrapper.querySelector('.input-meet-time').value
    }
    if (this.readOnly) {
      this._complete()
      this.wrapper.querySelector('.meet-edit').remove()
    }
    return this.wrapper
  }

  _updateDate(show = false) {
    this.data = {
      title: this.wrapper.querySelector('.input-meet-title').value,
      link: this.wrapper.querySelector('.input-meet-link').value,
      date: this.wrapper.querySelector('.input-meet-date').value,
      time: this.wrapper.querySelector('.input-meet-time').value,
      duration: this.wrapper.querySelector('.input-meet-duration').value,
      googleCalendarData: this.data.googleCalendarData,
      show,
    }
  }

  _fillWrapperForm() {
    this.wrapper.querySelector('.input-meet-title').value = this.data.title
    this.wrapper.querySelector('.input-meet-link').value = this.data.link
    this.wrapper.querySelector('.input-meet-date').value = this.data.date
    this.wrapper.querySelector('.input-meet-time').value = this.data.time
    this.wrapper.querySelector('.input-meet-duration').value
      = this.data.duration

    if (this.data?.googleCalendarData?.htmlLink) {
      this.wrapper.querySelector('.meet-link-href').href
        = this.data?.googleCalendarData?.htmlLink
    }
  }

  _edit() {
    this.wrapper
      .querySelector('.google-meet-card')
      .classList.remove('complete')
    this._updateDate()
  }

  _complete() {
    this._updateDate(true)
    this.wrapper.querySelector('.google-meet-card').classList.add('complete')
    this.wrapper.querySelector('.meet-time').innerHTML
      = this.data.date
      + ' '
      + this.data.time
      + ' ('
      + this.data.duration
      + 'min)'
    this.wrapper.querySelector('.meet-title').innerHTML = this.data.title
  }

  async _setToCalendar() {
    this._complete(true)
    const result = await this.config.nuxtApp.saveInGoogleCalendar(this.data)
    if (result) {
      console.log('Event Set Data:', result)

      this.data.googleCalendarData = result
      this.wrapper
        .querySelector('.google-meet-card')
        .classList.add('scheduled')
      this.data.link = result.hangoutLink
      this._fillWrapperForm()
    }
  }

  save(blockContent) {
    return this.data
  }
}

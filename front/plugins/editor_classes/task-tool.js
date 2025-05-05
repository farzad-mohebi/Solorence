export default class Task {
  static get isReadOnlySupported() {
    return true
  }

  static get toolbox() {
    return {
      title: 'Task',
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
    const statusColor = {
      0: 'red',
      1: 'orange',
      2: 'green',
    }
    const statusText = {
      0: 'Open',
      1: 'Doing',
      2: 'Done',
    }
    const statusIcon = {
      0: 'close-circle-outline text-red',
      1: 'progress-clock text-orange',
      2: 'check-circle-outline text-green',
    }
    this.wrapper.innerHTML = `
  <div class="task-card v-card v-theme--light v-card--density-default bg-${
    statusColor[this.data.status]
  }-lighten-5 my-2" data-id="${this.data.uid}">
    <div class="v-card-item">
      <div class="v-card-item__prepend">
        <i class="mdi-${
          statusIcon[this.data.status]
        } mdi v-icon notranslate v-theme--light v-icon--size-x-large" aria-hidden="true" density="default"></i>
      </div>
      <div class="v-card-item__content">
        <div class="v-card-title">
          ${this.data.title}
        </div>
        <div class="v-card-subtitle font-weight-bold text-${
          statusColor[this.data.status]
        }-darken-3">
          Status: ${statusText[this.data.status]}
        </div>
      </div>
    </div>
    <div class="v-card-text ${!this.data.description ? 'd-none' : ''}">
      ${this.data.description}
    </div>
  </div>      
            `
    this.wrapper.querySelector('.task-card').onclick = () => {
      const taskID = this.wrapper
        .querySelector('.task-card')
        .getAttribute('data-id')
      window['update_task_' + taskID] = (result) => {
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
      this.config.nuxtApp.showTask(taskID)
    }
  }

  render() {
    this.wrapper = document.createElement('div')
    this.wrapper.setAttribute('class', 'task-holder')
    if (!this.data?.uid) {
      this.wrapper.innerHTML = `Waiting for task...`
      window['set_task_state'] = (state, result = null) => {
        console.log('set_task_state', state, result)
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
        delete window['set_task_state']
      }
      this.config.nuxtApp.showCreateTask()
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

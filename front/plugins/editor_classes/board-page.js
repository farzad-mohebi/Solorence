export default class BoardPage {
  static get isReadOnlySupported() {
    return true
  }

  static get toolbox() {
    return {
      title: 'Board',
      icon: '<i class="mdi-artboard mdi v-icon notranslate text-black v-theme--light" aria-hidden="true" style="font-size: 18px; height: 18px; width: 18px;"></i>',
    }
  }

  constructor({ data, api, config, readOnly }) {
    this.readOnly = readOnly
    if (!this.uid) {
      this.uid = Math.random().toString(16).slice(2)
    }
    this.data = data
    if (!this.data.title) {
      this.data = {
        title: 'New Board',
        blocks: [],
      }
    }
    this.api = api
    this.config = config
    this.wrapper = undefined
  }

  render() {
    this.wrapper = document.createElement('div')
    this.wrapper.setAttribute('class', 'edit-board-holder')
    this.wrapper.innerHTML = `
        <div class="my-2">
          <div class="v-card w-100 bg-pink-lighten-5  v-card--density-default elevation-0 v-card--variant-elevated" data-uid="${this.uid}">
            <div class="v-card-text text-center align-center d-flex">
              <i class="mdi-artboard mdi v-icon notranslate text-pink " aria-hidden="true" style="font-size: 18px; height: 18px; width: 18px;"></i>
              <div class="text-start ms-2">
                <div class="text-body-1 mt-1 font-weight-bold text-pink board-title">
                  ${this.data.title}
                </div>
              </div>
            </div>
          </div>
        </div>
      `
    window['changeBoardData_' + this.uid] = (title, blocks) => {
      this.data = {
        title: title,
        blocks: blocks,
      }
      this.wrapper.querySelector('.board-title').innerHTML = title
    }

    this.wrapper.addEventListener('click', () => {
      console.log('HERE IS OK')
      this.config.nuxtApp.showBoard(this.uid, this.data.title, this.data.blocks)
    })

    return this.wrapper
  }

  save(blockContent) {
    return this.data
  }
}

import { defineStore } from 'pinia';

export const useNotificationStore = defineStore('notification', {
  state: () => ({
    message: '',
    type: 'success', // success, error, info
    visible: false,
  }),
  actions: {
    show(message, type = 'success') {
      this.message = message;
      this.type = type;
      this.visible = true;
      
      // Tu dong an sau 3 giay
      setTimeout(() => {
        this.visible = false;
      }, 3000);
    },
    hide() {
      this.visible = false;
    }
  }
});

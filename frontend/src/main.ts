import '@/styles/main.scss'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { usePermissionStore } from '@/stores/permission'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')

// TODO: 权限接口
const { setPermissions } = usePermissionStore()
setPermissions(['global-delete-auth'])

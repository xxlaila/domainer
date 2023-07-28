import { ref } from 'vue'
import { defineStore } from 'pinia'

export const usePermissionStore = defineStore('permission', () => {
  const permissions = ref<string[]>([])
  const setPermissions = (perm: string[]) => (permissions.value = perm)
  const hasPermissions = (perm: string) => {
    if (!perm) return false

    return permissions.value.includes(perm)
  }

  // 全局删除权限
  const hasGlobalDelPerm = computed(() => hasPermissions('global-delete-auth'))

  return { permissions, hasPermissions, setPermissions, hasGlobalDelPerm }
})

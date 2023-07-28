import { HomeFilled, ChromeFilled, Setting } from '@element-plus/icons-vue'
import type { MenuItemType, PickKeys } from '@/types'

export const initialRoutes: MenuItemType[] = [
  {
    path: '/home',
    name: 'home',
    title: '首页',
    icon: HomeFilled,
    hidden: false,
    component: () => import('@/views/home/WelcomeHome.vue')
  },
  {
    name: 'PublicDomain',
    title: '域名管理',
    icon: ChromeFilled,
    hidden: false,
    children: [
      {
        path: '/public',
        name: 'PublicDomainList',
        title: '公有解析',
        icon: null,
        hidden: false,
        component: () => import('@/views/public/PublicDomainList.vue')
      },
      {
        path: '/public/:ids',
        name: 'PublicDomainDetail',
        title: '域名解析-',
        icon: null,
        hidden: true,
        component: () => import('@/views/public/PublicDomainDetail.vue')
      }
    ]
  },
  {
    name: 'settings',
    title: '系统设置',
    icon: Setting,
    hidden: false,
    children: [
      {
        path: '/settings/skey-manage',
        name: 'skeyManage',
        title: '云密钥管理',
        icon: null,
        hidden: false,
        component: () => import('@/views/settings/skey-manage/skeyManageList.vue')
      }
    ]
  }
]

export const pickMenuProperties = <
  T extends { children?: T[]; hidden: boolean },
  K extends keyof T
>(
  menu: T[],
  keys: (K | 'children')[],
  filter = false
): PickKeys<T, K | 'children'>[] => {
  const res = filter ? menu.filter((item) => !item.hidden) : menu

  return (res || []).map((item) => {
    const result = {} as PickKeys<T, K | 'children'>

    if (item.children && item.children.length > 0) {
      const children = pickMenuProperties(item.children, keys, filter)

      if (children.length > 0) {
        result.children = children as T[]
      }
    }

    keys.forEach((key) => {
      if (key !== 'children') {
        if (Object.prototype.hasOwnProperty.call(item, key)) {
          result[key] = item[key]
        }
      }
    })

    return result
  })
}

export const menus = pickMenuProperties(initialRoutes, ['path', 'name', 'title', 'icon'], true)
export const routes = pickMenuProperties(initialRoutes, ['path', 'name', 'component'])

import type { Component } from 'vue'

export type PickKeys<T, K extends keyof T> = {
  [P in K]: T[P]
}

export type MenuProps = PickKeys<MenuItemType, 'name' | 'title' | 'path' | 'children' | 'icon'>

export interface MenuItemType {
  title: string
  name: string
  path?: string
  icon: Component | null
  component?: Component | null
  hidden: boolean
  children?: MenuItemType[]
}

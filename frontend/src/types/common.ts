import type { Ref, ShallowRef } from 'vue'


export type ListParamType<T = null> = {
  page: number
  size: number
} & T

export type CommonAPIReturn<T> = {
  code: number
  msg: string
  data: T
}

export interface ListReturn<T> {
  page: Ref<number>
  size: Ref<number>
  count: Ref<number>
  list: ShallowRef<T[]>
  setPage: (val: number) => number
  setSize: (val: number) => number
  loading: Ref<boolean>
  error: ShallowRef<any>
  retry: () => Promise<void>
}

export type PartialKeyOf<T, V> = Partial<{ [P in keyof T]: V }>



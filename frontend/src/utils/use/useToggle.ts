export function useToggle<T = true | false>(initialValue: Ref<T>): (value?: T) => T
export function useToggle<T = true | false>(initialValue?: T): [Ref<T>, (value?: T) => T]

export function useToggle(initialValue: Ref<boolean> | boolean = false) {
  const valueIsRef = isRef(initialValue)
  const _value = ref(initialValue) as Ref<boolean>

  function toggle(value?: boolean) {
    // has arguments
    if (arguments.length) {
      _value.value = value!
      return _value.value
    } else {
      const truthy = toValue(true)
      _value.value = _value.value === truthy ? toValue(false) : truthy
      return _value.value
    }
  }

  if (valueIsRef) return toggle
  else return [_value, toggle] as const
}

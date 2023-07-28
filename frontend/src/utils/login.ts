/**
 * 获取登录地址
 * @returns string 登录url
 */
export const getOALoginUrl = () => {
  const { protocol, href } = window.location

  return `${protocol}//${import.meta.env.VITE_LOGIN_HOST}/login/index?redirect=${encodeURIComponent(
    href
  )}`
}

import Cookies from 'js-cookie'

const TokenKey = 'Admin-Token'
const TokenKeyX = 'X-Token'

export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token) {
  return Cookies.set(TokenKey, token)
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}

export function getTokenX() {
  return Cookies.get(TokenKeyX)
}

export function setTokenX(token) {
  return Cookies.set(TokenKeyX, token)
}

export function removeTokenX() {
  return Cookies.remove(TokenKeyX)
}

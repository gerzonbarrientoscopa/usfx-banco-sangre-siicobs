import request from '@/utils/request'

const URL_PATH = '/reasons/'

export function getReasons(query) {
  return request({
    url: URL_PATH,
    method: 'get',
    params: query
  })
}

export function createReason(data) {
  return request({
    url: URL_PATH,
    method: 'post',
    data
  })
}

export function updateReason(id, data) {
  return request({
    url: URL_PATH + id + '/',
    method: 'put',
    data
  })
}

export function deleteReason(id) {
  return request({
    url: URL_PATH + id + '/',
    method: 'delete'
  })
}

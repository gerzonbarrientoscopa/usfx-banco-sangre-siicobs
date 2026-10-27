import request from '@/utils/request'

const URL_PATH = '/immunohematologies/'

export function printImmunohematology(id) {
  return request({
    url: URL_PATH + id + '/pdf/',
    method: 'get',
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Content-Type': 'application/pdf',
      'Accept': 'application/pdf',
      'Content-Disposition': 'attachment'
    },
    responseType: 'arraybuffer'
  })
}

export function reportToday(query) {
  return request({
    url: '/immunohematology-today-pdf/',
    method: 'get',
    params: query,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Content-Type': 'application/pdf',
      'Accept': 'application/pdf',
      'Content-Disposition': 'attachment'
    },
    responseType: 'arraybuffer'
  })
}

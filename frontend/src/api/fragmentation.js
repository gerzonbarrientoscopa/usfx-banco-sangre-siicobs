import request from '@/utils/request'

const URL_PATH = '/fragmentations/'

export function printFragmentation(id) {
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

export function printRoadMap() {
  return request({
    url: URL_PATH + 'road-map' + '/pdf/',
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
    url: '/fragmentation-today-pdf/',
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


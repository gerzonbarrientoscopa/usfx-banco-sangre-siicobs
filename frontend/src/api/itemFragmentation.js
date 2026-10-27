import request from '@/utils/request'

// const URL_PATH = '/item-fragmentations/'

export function printBloodBag(id) {
  return request({
    url: 'laboratories/bloodbag/' + id + '/pdf/',
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
    url: '/production-today-pdf/',
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

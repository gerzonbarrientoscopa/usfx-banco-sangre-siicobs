import request from '@/utils/request'

const URL_PATH = '/extractions/'

export function printAutoexclude(id) {
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


import request from '@/utils/request'

const URL_PATH = '/billings/'

export function printBilling(id) {
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

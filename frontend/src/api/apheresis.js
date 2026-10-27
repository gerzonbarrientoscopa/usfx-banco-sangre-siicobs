import request from '@/utils/request'

const URL_PATH = '/apheresis/'

export function printApheresis(id) {
  return request({
    url: URL_PATH + id + '/pdf',
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

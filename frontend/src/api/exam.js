import request from '@/utils/request'

const URL_PATH = '/exams/'

export function printPreSieveAll() {
  return request({
    url: URL_PATH + 'presieve' + '/pdf/',
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

import request from '@/utils/request'

const URL_PATH = '/clinical-histories/'

export function printClinicalHistoryAnswers(id) {
  return request({
    url: URL_PATH + id + '/pdf/answers',
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

import request from '@/utils/request'

const URL_PATH = '/questionnaire-convalescent-pdf/?id='

export function printQuestionnaireConvalescentPlasma(id) {
  return request({
    url: URL_PATH + id,
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

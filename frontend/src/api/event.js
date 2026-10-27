import request from '@/utils/request'

const URL_PATH = '/events/'

export function printPromotions(id) {
  return request({
    url: URL_PATH + 'donations/' + id + '/pdf/',
    method: 'get',
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Content-Type': 'application/pdf',
      'Accept': 'application/pdf',
      'Content-Disposition': 'attachment'
    },
    responseType: 'arraybuffer',
    params: { id }
  })
}

export function printDonorTicketVolunteer(id, type) {
  return request({
    url: '/donor-volunteer-tickets/' + id + '/pdf/?type=' + type,
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

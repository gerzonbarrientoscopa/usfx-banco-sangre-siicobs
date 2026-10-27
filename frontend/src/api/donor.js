import request from '@/utils/request'

const URL_PATH = '/donors/'

export function printDonorVolunteer(id) {
  return request({
    url: '/donor-volunteer/' + id + '/pdf/',
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

export function updateImageDonor(id, data) {
  return request({
    url: URL_PATH + 'upload-image/' + id + '/',
    method: 'put',
    data
  })
}


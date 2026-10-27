import request from '@/utils/request'

export function graphqlRequest(data) {
  return request({
    url: '/graphql/',
    method: 'post',
    data,
    params: { from: data.from ? data.from : 'undefined', service: data.service ? data.service : 'undefined' }
  })
}

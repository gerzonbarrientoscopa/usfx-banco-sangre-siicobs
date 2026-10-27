import request from '@/utils/request'

const URL_PATH = '/reports/'

export function buildReport(data) {
  return request({
    url: URL_PATH,
    method: 'post',
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Content-Type': 'application/pdf',
      'Accept': 'application/pdf',
      'Content-Disposition': 'attachment'
    },
    responseType: 'arraybuffer',
    data
  })
}

export function printReportGeneral(query) {
  return request({
    url: '/reports-pdf/',
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

export function printReportGeneralDonation(query) {
  return request({
    url: '/reports-donation-pdf/',
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

export function printReportGeneralExam(query) {
  return request({
    url: '/reports-exam-pdf/',
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

export function printReportGeneralPhysicalAnalysis(query) {
  return request({
    url: '/reports-physical-analysis-pdf/',
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

const URL_REPORT = '/reports/by-year/'

export function getReportsTotalYear(year) {
  return request({
    url: URL_REPORT,
    method: 'get',
    params: { year }
  })
}

export function printGeneralListRelease(query) {
  return request({
    url: '/reports-releases-list-pdf/',
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

export function printGeneralRelease(query) {
  return request({
    url: '/reports-releases-pdf/',
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
export function printGeneralDiscard(query) {
  return request({
    url: '/reports-discards-pdf/',
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

export function printGeneralImmunoserology(query) {
  return request({
    url: '/reports-immunoserologies-pdf/',
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

export function printGeneralImmunohematology(query) {
  return request({
    url: '/reports-immunohematologies-pdf/',
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

export function printGeneralDistribution(query) {
  return request({
    url: '/reports-distributions-pdf/',
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

export function printGeneralDistributionItemfragmentation(query) {
  return request({
    url: '/reports-distribution-itemfragmentations-pdf/',
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

export function printGeneralInventory(query) {
  return request({
    url: '/availability-products-pdf/',
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

export function printGeneralPurchaseInventory(query) {
  return request({
    url: '/purchase-products-pdf/',
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

export function printGeneralOrderInventory(query) {
  return request({
    url: '/order-products-pdf/',
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

export function printGeneralMyOrderInventory(query) {
  return request({
    url: '/my-order-products-pdf/',
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

export function reportDonationTimeline(query) {
  return request({
    url: '/donation-timeline-pdf/',
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

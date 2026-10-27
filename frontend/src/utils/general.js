export function buildBarcodeFilter(tempListQuery, field){
  if((tempListQuery.search).length === 14){
    tempListQuery[field] = parseInt((tempListQuery.search).substring(2,14))
    tempListQuery.search = ''
  }else{
    delete tempListQuery[field]
  }
  return tempListQuery
}

export function buildRegisterAtFilter(tempListQuery){
  tempListQuery.register_at__gte = null
  tempListQuery.register_at__lte = null

  if (tempListQuery.date_range !== null) {
    tempListQuery.register_at__gte = tempListQuery.date_range[0]
    tempListQuery.register_at__lte = tempListQuery.date_range[1]
  }
  return tempListQuery
}

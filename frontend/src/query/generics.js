const generics = {
  buildParams(listQuery) {
    let query = 'ordering: "' + listQuery.ordering + '"'

    if (listQuery.institution_id) {
      query += ', institution_id: ' + listQuery.institution_id
    }

    if (listQuery.id !== undefined) {
      query += ', id: ' + listQuery.id
    } else {
      if (listQuery.search !== '') {
        query += ', search: "' + listQuery.search + '"'
      }
    }

    if (listQuery['date_init'] && listQuery['date_end'] && listQuery['date_init'] !== '' && listQuery['date_end'] !== '') {
      const queryParams = 'register_at__gte: "' + listQuery['date_init'] + '", register_at__lte: "' + listQuery['date_end'] + '"'
      if (query !== '') {
        query += ', ' + queryParams
      } else {
        query = queryParams
      }
    }

    if (listQuery['date_range'] && listQuery['date_range'] !== '' && listQuery['date_range'].length === 2) {
      const queryParams = 'register_at__gte: "' + listQuery['date_range'][0] + '", register_at__lte: "' + listQuery['date_range'][1] + '"'
      if (query !== '') {
        query += ', ' + queryParams
      } else {
        query = queryParams
      }
    }

    if (listQuery['extra'] && listQuery['extra']['date_init'] !== '') {
      query += (query !== '' ? ',' : '') + 'register_at__gte: "' + listQuery['extra']['date_init'] + '"'
    }
    if (listQuery['extra'] && listQuery['extra']['date_end'] !== '') {
      query += (query !== '' ? ',' : '') + 'register_at__lte: "' + listQuery['extra']['date_end'] + '"'
    }

    return query
  },
  buildShowParams(listQuery) {
    let query = ''

    if (listQuery.id !== undefined) {
      query += 'id: ' + listQuery.id
    }

    return query
  },
  buildGraphqlParams(paramsGraphqlArgument) {
    const finalParams = []
    paramsGraphqlArgument = paramsGraphqlArgument.replace(/\s/g, '')

    paramsGraphqlArgument.split(',').forEach(function(item) {
      const $param_name = item.split(':')[0]
      finalParams.push($param_name.substring(1, $param_name.length) + ': ' + $param_name)
    })
    return finalParams.join(', ')
  }
}

export default generics

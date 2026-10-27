import generics from './generics'

const MODEL = 'typehemocomponents'

const typeSolutions = {
  list(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `     id
            name
            acronym
            register_at
      }
      }
      }`
  },
  package_select(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `     id
            acronym
            name
      }
      }
      }`
  },
  requestRelease(listQuery) {
    let query = generics.buildParams(listQuery)
    query += (query !== '' ? ',' : '') + 'show_in_request_release: true'

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `     id
            acronym
            name
      }
      }
      }`
  },
  fragmentation_select(listQuery) {
    let query = generics.buildParams(listQuery)
    query += (query !== '' ? ',' : '') + 'show_in_fragmentation: true'

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `     id
            acronym
            description
            expiration_day
            name
            position
            is_pediatric
            can_add_bags
            max_expiration_days
            typediscards {
              id
              name
            }
            typecoagulation
            temperature_save
            show_in_request_release
            show_in_billing
            show_in_fragmentation
      }
      }
      }`
  }
}

export default typeSolutions

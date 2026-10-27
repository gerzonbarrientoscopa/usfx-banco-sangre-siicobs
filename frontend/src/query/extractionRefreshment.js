import generics from './generics'

const MODEL = 'extractionrefreshments'
const SINGLE_MODEL = 'extractionrefreshment'

const extractionRefreshments = {
  list(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `     id
            register_at
            menu {
              id
              name
            }
            extraction {
              id
              donation
              {
                  id
                  donor
                  {
                      id
                      code
                      first_name
                      middle_name
                      last_name
                  }
              }
            }
            employee {
              id
              first_name
              middle_name
              last_name
            }
      }
      }
      }`
  },

  createExtractionRefreshment() {
    return this.buildExtractionRefreshment('create')
  },
  updateExtractionRefreshment() {
    return this.buildExtractionRefreshment('update')
  },
  deleteExtractionRefreshment() {
    return this.buildExtractionRefreshment('delete')
  },
  buildExtractionRefreshment(action) {
    let paramsGraphqlArgument = '$employee_id: Int!, $extraction_id: Int!, $menu_id: Int!, $register_at: Date!'
    if (action === 'update') {
      paramsGraphqlArgument = '$employee_id: Int, $extraction_id: Int, $id: Int!, $menu_id: Int, $register_at: Date'
    } else if (action === 'delete') {
      paramsGraphqlArgument = '$id: Int!'
    }
    const paramsResolve = generics.buildGraphqlParams(paramsGraphqlArgument)

    return `
    mutation ${action}ExtractionRefreshment(${paramsGraphqlArgument} ) {
      ${action}_${SINGLE_MODEL}(${paramsResolve}) {
        ${SINGLE_MODEL} {
          id
        }
      }
    }
    `
  }
}

export default extractionRefreshments

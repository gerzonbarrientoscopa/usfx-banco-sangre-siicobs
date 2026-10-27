import generics from './generics'

const MODEL = 'refreshments'
const SINGLE_MODEL = 'refreshment'

const refreshments = {
  list(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `   id
          name
          type
      }
      }
      }`
  },
  createRefreshment() {
    return this.buildRefreshment('create')
  },
  updateRefreshment() {
    return this.buildRefreshment('update')
  },
  buildRefreshment(action) {
    let paramsGraphqlArgument = '$name: String!, $type: String!'
    if (action === 'update') {
      paramsGraphqlArgument = '$id: Int!, $name: String, $type: String'
    }
    const paramsResolve = generics.buildGraphqlParams(paramsGraphqlArgument)

    return `
    mutation ${action}Refreshment(${paramsGraphqlArgument} ) {
      ${action}_${SINGLE_MODEL}(${paramsResolve}) {
        ${SINGLE_MODEL} {
          id
        }
      }
    }
    `
  }
}

export default refreshments

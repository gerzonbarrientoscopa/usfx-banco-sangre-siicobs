import generics from './generics'

const MODEL = 'reasons'
const SINGLE_MODEL = 'reason'

const reason = {
  list(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `     id
            type
            name
      }
      }
      }`
  },
  exam_select(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `     id
            type
            name
      }
      }
      }`
  },
  physicalAnalysis_select(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `     id
            type
            name
      }
      }
      }`
  },
  donationEdit_select(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `     id
            type
            name
      }
      }
      }`
  },
  createReason() {
    return this.buildReason('create')
  },
  updateReason() {
    return this.buildReason('update')
  },
  buildReason(action) {
    let paramsGraphqlArgument = '$name: String!, $type: String!'
    if (action === 'update') {
      paramsGraphqlArgument = '$id: Int!, $name: String, $type: String'
    }
    const paramsResolve = generics.buildGraphqlParams(paramsGraphqlArgument)

    return `
    mutation ${action}Reason(${paramsGraphqlArgument} ) {
      ${action}_${SINGLE_MODEL}(${paramsResolve}) {
        ${SINGLE_MODEL} {
          id
        }
      }
    }
    `
  }
}

export default reason

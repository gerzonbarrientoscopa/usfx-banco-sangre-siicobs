import generics from './generics'

const MODEL = 'serologyprotocols'
const SINGLE_MODEL = 'serologyprotocol'

const serologyProtocols = {
  listSerologyProtocols(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `     id
      method
      kit
      due_date_at
      lot
      industry
      test
      type
      register_at
      cutt_off
      cutt_off_max
      cutt_off_min
      employee {
        id
        first_name
        middle_name
        last_name
      }
      values
      }
      }
    }`
  },
  createSerologyProtocol() {
    return this.buildSerologyProtocol('create')
  },
  updateSerologyProtocol() {
    return this.buildSerologyProtocol('update')
  },
  deleteSerologyProtocol() {
    return this.buildSerologyProtocol('delete')
  },
  buildSerologyProtocol(action) {
    let paramsGraphqlArgument = '$cutt_off: String, $cutt_off_max: String, $cutt_off_min: String, $due_date_at: Date!, $employee_id: Int!, $industry: String!, $kit: String!, $lot: String!, $method: String!, $register_at: Date, $test: Int!, $type: String!, $values: GenericScalar!'
    if (action === 'update') {
      paramsGraphqlArgument = '$cutt_off: String, $cutt_off_max: String, $cutt_off_min: String, $due_date_at: Date, $employee_id: Int, $id: Int!, $industry: String, $kit: String, $lot: String, $method: String, $register_at: Date, $test: Int, $type: String, $values: GenericScalar'
    } else if (action === 'delete') {
      paramsGraphqlArgument = '$id: Int!'
    }
    const paramsResolve = generics.buildGraphqlParams(paramsGraphqlArgument)

    return `
    mutation ${action}SerologyProtocol(${paramsGraphqlArgument} ) {
      ${action}_${SINGLE_MODEL}(${paramsResolve}) {
        ${SINGLE_MODEL} {
          id
        }
      }
    }
    `
  }
}

export default serologyProtocols

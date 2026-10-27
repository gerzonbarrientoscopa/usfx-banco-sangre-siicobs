import generics from './generics'

const MODEL = 'rejecteds'
const SINGLE_MODEL = 'rejected'

const rejecteds = {
  list(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `    id
           resource
           resource_id
           observations
           register_at
           donation {
             type_donation
             last_donation_at
             register_at
             donor {
               id
               first_name
               middle_name
               last_name
               code
             }
           }
           reason {
            id
            name
            type
           }
           employee {
           first_name
           middle_name
           last_name
           }
      }
      }
      }`
  },

  createRejected() {
    return this.buildRejected('create')
  },
  updateRejected() {
    return this.buildRejected('update')
  },
  deleteRejected() {
    return this.buildRejected('delete')
  },
  buildRejected(action) {
    let paramsGraphqlArgument = '$donation_id: Int!, $employee_id: Int!, $observations: String, $reason_id: Int!, $register_at: Date!, $resource: String!, $resource_id: Int!'
    if (action === 'update') {
      paramsGraphqlArgument = '$donation_id: Int, $employee_id: Int, $id: Int!, $observations: String, $reason_id: Int, $register_at: Date, $resource: String, $resource_id: Int'
    } else if (action === 'delete') {
      paramsGraphqlArgument = '$id: Int!'
    }
    const paramsResolve = generics.buildGraphqlParams(paramsGraphqlArgument)

    return `
    mutation ${action}Rejected(${paramsGraphqlArgument} ) {
      ${action}_${SINGLE_MODEL}(${paramsResolve}) {
        ${SINGLE_MODEL} {
          id
        }
      }
    }
    `
  }
}

export default rejecteds

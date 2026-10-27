import generics from './generics'

const MODEL = 'employees'
const SINGLE_MODEL = 'employee'

const employees = {
  list(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `     id
            ci
            code_licence
            first_name
            gender
            home_address
            last_name
            middle_name
            mobile_phone
            register_at
            institution {
              id
              name
            }
            user {
              id
              is_active
              username
              groups {
                id
                name
                permissions {
                  id
                }
              }
            }
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
            ci
            first_name
            last_name
            middle_name
      }
      }
      }`
  },
  selectReportFragmentation(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `     id
            ci
            first_name
            last_name
            middle_name
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
            ci
            first_name
            last_name
            middle_name
      }
      }
      }`
  },
  extraction_select(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `     id
            ci
            first_name
            last_name
            middle_name
      }
      }
      }`
  },
  phlebotomy_select(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `     id
            ci
            first_name
            last_name
            middle_name
      }
      }
      }`
  },
  createEmployee() {
    return this.buildEmployee('create')
  },
  updateEmployee() {
    return this.buildEmployee('update')
  },
  buildEmployee(action) {
    let paramsGraphqlArgument = '$ci: Int!, $code_licence: String, $first_name: String!, $gender: String!, $home_address: String, $institution_id: Int!, $last_name: String, $middle_name: String, $mobile_phone: Int'

    if (action === 'update') {
      paramsGraphqlArgument = '$id: Int!, $ci: Int, $code_licence: String, $first_name: String, $gender: String, $home_address: String, $institution_id: Int, $last_name: String, $middle_name: String, $mobile_phone: Int'
    }

    const paramsResolve = generics.buildGraphqlParams(paramsGraphqlArgument)

    return `
    mutation ${action}Employee(${paramsGraphqlArgument}) {
      ${action}_${SINGLE_MODEL}(${paramsResolve} ) {
        ${SINGLE_MODEL} {
          id
        }
      }
    }
    `
  }
}

export default employees

import generics from './generics'

const MODEL = 'selfexclusions'
const SINGLE_MODEL = 'selfexclusion'

const selfExclusion = {
  listSelfExclusion(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `     id
            observations
            register_at
            employee {
                    id
                    first_name
                    middle_name
                    last_name
            }
            register {
                    id
                    first_name
                    middle_name
                    last_name
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
      }
      }
      }`
  },
  createSelfExclusion() {
    return this.buildSelfExclusion('create')
  },
  updateSelfExclusion() {
    return this.buildSelfExclusion('update')
  },
  buildSelfExclusion(action) {
    let paramsGraphqlArgument = '$employee_id: Int!, $extraction_id: Int!, $observations: String, $register_at: Date!, $register_id: Int!'
    if (action === 'update') {
      paramsGraphqlArgument = '$employee_id: Int, $extraction_id: Int, $id: Int!, $observations: String, $register_at: Date, $register_id: Int'
    }
    const paramsResolve = generics.buildGraphqlParams(paramsGraphqlArgument)

    return `
    mutation ${action}SelfExclusion(${paramsGraphqlArgument} ) {
      ${action}_${SINGLE_MODEL}(${paramsResolve}) {
        ${SINGLE_MODEL} {
          id
        }
      }
    }
    `
  }
}

export default selfExclusion

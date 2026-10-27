import generics from './generics'

const MODEL = 'adversereactions'
const SINGLE_MODEL = 'adversereaction'

const adverseReactions = {
  list(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `     id
            extraction_place
            evolution
            detection
            behavior_taken
            observations
            register_at
            type {
              id
              name
            }
            employee {
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
  createAdverseReaction() {
    return this.buildAdverseReaction('create')
  },
  updateAdverseReaction() {
    return this.buildAdverseReaction('update')
  },
  buildAdverseReaction(action) {
    let paramsGraphqlArgument = '$behavior_taken: String, $detection: String!, $employee_id: Int!, $evolution: String!, $extraction_id: Int!, $extraction_place: String!, $observations: String, $register_at: DateTime!, $type_id: GenericScalar!'
    if (action === 'update') {
      paramsGraphqlArgument = '$behavior_taken: String, $detection: String, $employee_id: Int, $evolution: String, $extraction_id: Int, $extraction_place: String, $id: Int!, $observations: String, $register_at: DateTime, $type_id: GenericScalar'
    }
    const paramsResolve = generics.buildGraphqlParams(paramsGraphqlArgument)

    return `
    mutation ${action}AdverseReaction(${paramsGraphqlArgument} ) {
      ${action}_${SINGLE_MODEL}(${paramsResolve}) {
        ${SINGLE_MODEL} {
          id
        }
      }
    }
    `
  }
}

export default adverseReactions

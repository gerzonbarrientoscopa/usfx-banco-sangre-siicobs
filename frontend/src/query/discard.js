import generics from './generics'

const MODEL = 'discards'
const SINGLE_MODEL = 'discard'

const discards = {
  list(listQuery) {
    let query = generics.buildParams(listQuery)
    if (listQuery.typehemocomponent_id !== '') {
      query += ', typehemocomponent_id: ' + listQuery.typehemocomponent_id
    }
    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `     id
            reason
            observations
            register_at
            itemfragmentation {
              id
              donor_code
              fragmentation {
                id
                extraction {
                  id
                  register_at
                }
              }
              typehemocomponent {
                id
                name
              }
              typediscard {
                id
                name
              }
              expiration_date
              weight
              status
              observations
            }
            employee
            {
                id
                first_name
                middle_name
                last_name
            }
      }
      }
      }`
  },
  listDiscardReport(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `     id
            observations
            register_at
            itemfragmentation {
              id
              donor_code
              expiration_date
              weight
              status
              observations
              fragmentation {
                extraction {
                  register_at,
                  donation {
                    id
                    immunohematology {
                      id
                    },
                    immunoserology {
                      id
                    }
                  }
                }
              }
              typehemocomponent {
                id
                name
              }
              typediscard {
                id
                name
              }
            }
            employee
            {
                id
                first_name
                middle_name
                last_name
            }
      }
      }
      }`
  },
  listDailyDiscardReport(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `     id
            observations
            register_at
            itemfragmentation {
              id
              donor_code
              expiration_date
              weight
              status
              observations
              fragmentation {
                extraction {
                  register_at,
                  donation {
                    immunohematology {
                      id
                    },
                    immunoserology {
                      id
                    }
                  }
                }
              }
              typehemocomponent {
                id
                name
              }
              typediscard {
                id
                name
              }
            }
            employee
            {
                id
                first_name
                middle_name
                last_name
            }
      }
      }
      }`
  },
  createDiscard() {
    return this.buildDiscard('create')
  },
  updateDiscard() {
    return this.buildDiscard('update')
  },
  createMassiveDiscard() {
    return this.buildDiscard('create_massive')
  },
  deleteDiscard() {
    return this.buildDiscard('delete')
  },
  buildDiscard(action) {
    let paramsGraphqlArgument = '$employee_id: Int!, $itemfragmentation_id: Int!, $observations: String, $reason: String!, $register_at: Date!, $register_id: Int!'
    if (action === 'update') {
      paramsGraphqlArgument = '$employee_id: Int, $id: Int!, $itemfragmentation_id: Int, $observations: String, $reason: String, $register_at: Date, $register_id: Int'
    } else if (action === 'create_massive') {
      paramsGraphqlArgument = '$employee_id: Int!, $hemocomponents: [MassiveDiscardItemInput], $observations: String, $reason: String!, $register_at: Date!, $register_id: Int!'
    } else if (action === 'delete') {
      paramsGraphqlArgument = '$id: Int!'
    }
    const paramsResolve = generics.buildGraphqlParams(paramsGraphqlArgument)

    return `
    mutation ${action}Discard(${paramsGraphqlArgument} ) {
      ${action}_${SINGLE_MODEL}(${paramsResolve}) {
        ${SINGLE_MODEL} {
          id
        }
      }
    }
    `
  }
}

export default discards

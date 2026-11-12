import generics from './generics'

const MODEL = 'releases'
const SINGLE_MODEL = 'release'

const releases = {
  list(listQuery) {
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
  listRelease(listQuery) {
    let query = generics.buildParams(listQuery)
    if (listQuery.typehemocomponent_id !== '') {
      query += ', typehemocomponent_id: ' + listQuery.typehemocomponent_id
    }
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
              distributionitemfragmentations {
                id
              }
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
  listReleaseReport(listQuery) {
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
  listDailyReleaseReport(listQuery) {
    let query = generics.buildParams(listQuery)
    if (listQuery.typehemocomponent_id && listQuery.typehemocomponent_id !== 'all') {
      query += (query !== '' ? ', ' : '') + 'typehemocomponent_id: ' + listQuery.typehemocomponent_id
    }

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
  createRelease() {
    return this.buildRelease('create')
  },
  updateRelease() {
    return this.buildRelease('update')
  },
  createMassiveRelease() {
    return this.buildRelease('create_massive')
  },
  deleteRelease() {
    return this.buildRelease('delete')
  },
  buildRelease(action) {
    let paramsGraphqlArgument = '$employee_id: Int!, $itemfragmentation_id: Int!, $observations: String, $register_at: Date!, $register_id: Int!'
    if (action === 'update') {
      paramsGraphqlArgument = '$employee_id: Int, $id: Int!, $itemfragmentation_id: Int, $observations: String, $register_at: Date, $register_id: Int'
    } else if (action === 'create_massive') {
      paramsGraphqlArgument = '$employee_id: Int!, $hemocomponents: [MassiveReleaseItemInput], $observations: String, $register_at: Date!, $register_id: Int!'
    } else if (action === 'delete') {
      paramsGraphqlArgument = '$id: Int!'
    }
    const paramsResolve = generics.buildGraphqlParams(paramsGraphqlArgument)

    return `
    mutation ${action}Release(${paramsGraphqlArgument} ) {
      ${action}_${SINGLE_MODEL}(${paramsResolve}) {
        ${SINGLE_MODEL} {
          id
        }
      }
    }
    `
  }
}
export default releases

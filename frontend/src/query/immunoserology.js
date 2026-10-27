import generics from './generics'

const MODEL = 'immunoserologies'
const SINGLE_MODEL = 'immunoserology'

const immunoserologies = {
  list(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{
      ${MODEL} ( ${query} ) {
      totalCount
      results(limit: ${listQuery.limit}, offset: ${listQuery.offset}) {
            id
            hiv
            hbsag
            hvc
            cheia
            chagas_hai
            rpr
            is_reactive
            history
            observations
            register_at
            employee {
                id
                first_name
                middle_name
                last_name
            }
            donation {
                id
                type_donation
                register_at
                last_donation_at
                extraction {
                    id
                }
                donor {
                    id
                    code
                    first_name
                    middle_name
                    last_name
                }
                rejected {
                    id
                    reason {
                      id
                      name
                      type
                    }
                }
            }
      }
      }
      }`
  },
  listReport(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{
      ${MODEL} ( ${query} ) {
      totalCount
      results(limit: ${listQuery.limit}, offset: ${listQuery.offset}) {
            id
            hiv
            hbsag
            hvc
            cheia
            chagas_hai
            rpr
            history
            observations
            register_at
            employee {
                id
                first_name
                middle_name
                last_name
            }
            donation {
                id
                type_donation
                register_at
                last_donation_at
                extraction {
                    id
                }
                donor {
                    id
                    code
                    first_name
                    middle_name
                    last_name
                }
                rejected {
                    id
                    reason {
                      id
                      name
                      type
                    }
                }
            }
      }
      }
      }`
  },
  get(id) {
    return `{
      ${SINGLE_MODEL} (id: ${id} ) {
            id
            hiv
            hbsag
            hvc
            cheia
            chagas_hai
            rpr
            history
            observations
            register_at
            employee {
                id
                first_name
                middle_name
                last_name
            }
            donation {
                id
                type_donation
                register_at
                last_donation_at
                extraction {
                    id
                }
                donor {
                    id
                    code
                    first_name
                    middle_name
                    last_name
                }
                rejected {
                    id
                    reason {
                      id
                      name
                      type
                    }
                }
            }
      }
      }`
  },
  createImmunoserology() {
    return this.buildImmunoserology('create')
  },
  updateImmunoserology() {
    return this.buildImmunoserology('update')
  },
  buildImmunoserology(action) {
    let paramsGraphqlArgument = '$chagas_hai: String, $cheia: String, $donation_id: Int!, $employee_id: Int!, $hbsag: String, $hiv: String, $hvc: String, $observations: String, $register_at: Date, $rpr: String'
    if (action === 'update') {
      paramsGraphqlArgument = '$chagas_hai: String, $cheia: String, $donation_id: Int, $employee_id: Int, $hbsag: String, $hiv: String, $hvc: String, $id: Int!, $observations: String, $register_at: Date, $rpr: String'
    }
    const paramsResolve = generics.buildGraphqlParams(paramsGraphqlArgument)

    return `
    mutation ${action}Immunoserology(${paramsGraphqlArgument} ) {
      ${action}_${SINGLE_MODEL}(${paramsResolve}) {
        ${SINGLE_MODEL} {
          id
        }
      }
    }
    `
  }
}

export default immunoserologies

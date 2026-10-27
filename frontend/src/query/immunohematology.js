import generics from './generics'

const MODEL = 'immunohematologies'
const SINGLE_MODEL = 'immunohematology'

const immunohematologies = {
  list(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{
      ${MODEL} ( ${query} ) {
      totalCount
      results(limit: ${listQuery.limit}, offset: ${listQuery.offset}) {
            id
            direct_abo
            inverse_abo
            factor_rh
            phenotype
            antikell
            alb
            liss
            coombs
            fsi
            p2fsi
            p2alb
            p2liss
            p2coombs
            p3alb
            p3fsi
            p3liss
            p3coombs
            exist_irregular_antibody
            type_irregular_antibody {
              id
            }
            employee {
                id
                first_name
                middle_name
                last_name
            }
            observations
            register_at
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
            direct_abo
            inverse_abo
            factor_rh
            phenotype
            antikell
            alb
            liss
            coombs
            fsi
            p2fsi
            p2alb
            p2liss
            p2coombs
            p3alb
            p3fsi
            p3liss
            p3coombs
            exist_irregular_antibody
            type_irregular_antibody {
              id
            }
            employee {
                id
                first_name
                middle_name
                last_name
            }
            observations
            register_at
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
  short_list(listQuery) {
    let query = generics.buildParams(listQuery)
    if (listQuery.donation__donor__id) {
      query += 'donation__donor__id: ' + listQuery.donation__donor__id
    }
    return `{
      ${MODEL} ( ${query} ) {
      totalCount
      results(limit: ${listQuery.limit}, offset: ${listQuery.offset}) {
            id
            direct_abo
            factor_rh
            phenotype
            alb
            fsi
            liss
            coombs
            fsi
            p2fsi
            p2alb
            p2liss
            p2coombs
            p3alb
            p3fsi
            p3liss
            p3coombs
            register_at
            type_irregular_antibody {
              id
              name
            }
            donation {
              donor {
                code
              }
              extraction {
                id
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
            direct_abo
            inverse_abo
            factor_rh
            phenotype
            antikell
            alb
            liss
            coombs
            fsi
            p2fsi
            p2alb
            p2liss
            p2coombs
            p3alb
            p3fsi
            p3liss
            p3coombs
            type_irregular_antibody {
              id
              name
            }
            employee {
                id
                first_name
                middle_name
                last_name
            }
            observations
            register_at
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
  createImmunohematology() {
    return this.buildImmunohematology('create')
  },
  updateImmunohematology() {
    return this.buildImmunohematology('update')
  },
  buildImmunohematology(action) {
    let paramsGraphqlArgument = '$alb: String, $antikell: String, $coombs: String, $direct_abo: String, $inverse_abo: String, $donation_id: Int!, $employee_id: Int!, $factor_rh: String, $fsi: String, $liss: String, $observations: String, $p2alb: String, $p2coombs: String, $p2fsi: String, $p2liss: String, $p3alb: String, $p3coombs: String, $p3fsi: String, $p3liss: String, $phenotype: String, $register_at: Date, $type_irregular_antibody_id: Int'
    if (action === 'update') {
      paramsGraphqlArgument = '$alb: String, $antikell: String, $coombs: String, $direct_abo: String, $inverse_abo: String, $donation_id: Int, $employee_id: Int, $factor_rh: String, $fsi: String, $id: Int!, $liss: String, $observations: String, $p2alb: String, $p2coombs: String, $p2fsi: String, $p2liss: String, $p3alb: String, $p3coombs: String, $p3fsi: String, $p3liss: String, $phenotype: String, $register_at: Date, $type_irregular_antibody_id: Int'
    }
    const paramsResolve = generics.buildGraphqlParams(paramsGraphqlArgument)

    return `
    mutation ${action}Immunohematology(${paramsGraphqlArgument} ) {
      ${action}_${SINGLE_MODEL}(${paramsResolve}) {
        ${SINGLE_MODEL} {
          id
        }
      }
    }
    `
  }
}

export default immunohematologies

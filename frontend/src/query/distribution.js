import generics from './generics'

const MODEL = 'distributions'
const SINGLE_MODEL = 'distribution'

const distributions = {
  listDistribution(listQuery) {
    let query = generics.buildParams(listQuery)

    if (listQuery.type_payment) {
      query += ', type_payment: ' + listQuery.type_payment
    }

    return `{
      ${MODEL}(${query}) {
      totalCount
      results(limit: ${listQuery.limit}, offset: ${listQuery.offset}) {
            id
            uuid
            is_donation
            type_payment
            status
            register_at
            medical {
              id
              first_name
              last_name
              middle_name
            }
            patient {
              id
              first_name
              last_name
              middle_name
            }
            institution {
              id
              name
              type
            }
            employee {
                id
                first_name
                middle_name
                last_name
            }
            total_itemfragmentations
      }
      }
      }`
  },
  getDistribution(id) {
    return `{
      ${SINGLE_MODEL}(id: ${id}) {
            id
            uuid
            is_donation
            type_payment
            observations
            register_at
            service_transfunctional
            medical {
              id
              first_name
              last_name
              middle_name
            }
            patient {
              id
              first_name
              last_name
              middle_name
            }
            institution {
              id
              name
            }
            employee {
                id
                first_name
                middle_name
                last_name
            }
            itemfragmentations {
              id
              itemfragmentation {
                id
                donor_code
                expiration_date
                weight
                status
                typehemocomponent {
                  id
                  name
                }
                fragmentation{
                id
                extraction{
                id
                tubing
              }
                }

              }

            }
      }
      }`
  },
  listInstitutionBilling(listQuery) {
    let query = generics.buildParams(listQuery)

    if (listQuery.type_payment) {
      query += ', type_payment: ' + listQuery.type_payment
    }

    return `{
      ${MODEL}(${query}) {
      totalCount
      results(limit: ${listQuery.limit}, offset: ${listQuery.offset}) {
            id
            uuid
            type_payment
            register_at
            medical {
              id
              first_name
              last_name
              middle_name
            }
            patient {
              id
              first_name
              last_name
              middle_name
            }
            institution {
              id
              name
            }
            employee {
                id
                first_name
                middle_name
                last_name
            }
            itemfragmentations {
              id
              itemfragmentation {
                id
                donor_code
                expiration_date
                weight
                status
                typehemocomponent {
                  id
                  name
                }
              }
            }
      }
      }
      }`
  },
  reportList(listQuery) {
    let query = generics.buildParams(listQuery)

    if (listQuery.employee_id && listQuery.employee_id !== '') {
      query += ', employee_id: ' + listQuery.employee_id
    }

    if (listQuery.type_payment && listQuery.type_payment !== '') {
      query += ', type_payment: "' + listQuery.type_payment +'"'
    }

    if (listQuery.institution__type && listQuery.institution__type !== '') {
      query += ', institution__type: "' + listQuery.institution__type +'"'
    }
    if (listQuery.etary && listQuery.etary !== '') {
      var etaryOption = listQuery.etary.split('-')
      query += 'age_patient_type: "Y", age_patient__gte: ' + etaryOption[0] + ', age_patient__lte: ' + etaryOption[1]
    }

    return `{
      ${MODEL}(${query}) {
      totalCount
      results(limit: ${listQuery.limit}, offset: ${listQuery.offset}) {
            id
            uuid
            is_donation
            type_payment
            age_patient
            age_patient_type
            observations
            register_at
            service_transfunctional
            medical {
              id
              first_name
              last_name
              middle_name
            }
            patient {
              id
              first_name
              last_name
              middle_name
              gender
            }
            institution {
              id
              name
              type
            }
            employee {
                id
                first_name
                middle_name
                last_name
            }
            itemfragmentations {
              id
              itemfragmentation {
                id
                donor_code
                expiration_date
                weight
                status
                typehemocomponent {
                  id
                  name
                }
              }
            }
      }
      }
      }`
  },
  createDistribution() {
    return this.buildDistribution('create')
  },
  updateDistribution() {
    return this.buildDistribution('update')
  },
  buildDistribution(action) {
    let paramsArgument = ' $employee_id: Int!, $institution_id: Int!, $is_donation: Boolean, $medical_id: Int!, $observations: String, $patient_id: Int, $register_at: DateTime!, $service_transfunctional: String, $status: String, $type_payment: String!, $itemfragmentations: [DistributionItemInput]'
    let paramIdResolve = ''
    if (action === 'update') {
      paramsArgument = '$id: Int!, $employee_id: Int, $institution_id: Int, $is_donation: Boolean, $medical_id: Int, $observations: String, $patient_id: Int, $register_at: DateTime, $service_transfunctional: String, $status: String, $type_payment: String, $itemfragmentations: [DistributionItemInput]'
      paramIdResolve = 'id: $id,'
    }

    return `
    mutation ${action}Distribution(${paramsArgument}) {
      ${action}_${SINGLE_MODEL}(
      ${paramIdResolve} employee_id: $employee_id, institution_id: $institution_id, is_donation: $is_donation,medical_id: $medical_id,observations: $observations, patient_id: $patient_id,register_at: $register_at, service_transfunctional: $service_transfunctional,status: $status, type_payment: $type_payment, itemfragmentations: $itemfragmentations) {
        ${SINGLE_MODEL} {
          id
        }
      }
    }
    `
  }
}
export default distributions

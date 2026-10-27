import generics from './generics'

const MODEL = 'clinicalhistoryanswers'
const SINGLE_MODEL = 'clinicalhistoryanswer'

const clinicalHistoryAnswers = {
  listClinicalHistory(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `    id
           responses
           observations
           register_at
           questionnaire {
              id
              title
              questions
              is_active
           }
           donation {
             id
             type_donation
             last_donation_at
             register_at
             rejected {
               id
               resource
               resource_id
               observations
               register_at
               reason {
                id
                name
                type
               }
             }
             donor {
               id
               first_name
               middle_name
               last_name
               code
             }
             place {
               name
               settingphysical {
                  hematocrit_min
                  hematocrit_max
                  hematocrit_min_m
                  hematocrit_max_m
                  systolic_min
                  systolic_max
                  diastolic_min
                  diastolic_max
                  pulse_min
                  pulse_max
                  weight_min
                  hemoglobin_factor
               }
             }
           }
           employee {
             id
             first_name
             middle_name
             last_name
           }
      }
      }
      }`
  },
  createClinicalHistory() {
    return this.buildClinicalHistory('create')
  },
  updateClinicalHistory() {
    return this.buildClinicalHistory('update')
  },
  buildClinicalHistory(action) {
    let paramsGraphqlArgument = '$donation_id: Int!, $employee_id: Int!, $observations: String, $questionnaire_id: Int!, $register_at: Date, $register_id: Int!, $responses: GenericScalar'
    if (action === 'update') {
      paramsGraphqlArgument = '$donation_id: Int, $employee_id: Int, $id: Int!, $observations: String, $questionnaire_id: Int, $register_at: Date, $register_id: Int, $responses: GenericScalar'
    }
    const paramsResolve = generics.buildGraphqlParams(paramsGraphqlArgument)

    return `
    mutation ${action}ClinicalHistory(${paramsGraphqlArgument} ) {
      ${action}_${SINGLE_MODEL}(${paramsResolve}) {
        ${SINGLE_MODEL} {
          id
        }
      }
    }
    `
  }
}

export default clinicalHistoryAnswers

import generics from './generics'

const MODEL = 'physicalanalyses'
const SINGLE_MODEL = 'physicalanalysis'

const physicalAnalysis = {
  list(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `    id
           systolic
           diastolic
           pulse
           tall
           weight
           temperature
           observations
           register_at
           donation {
             id
             type_donation
             last_donation_at
             register_at
             exam {
               hematocrit
               hemoglobin
             }
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
               can_donate
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
           register {
             id
             first_name
             middle_name
             last_name
           }
      }
      }
      }`
  },
  createPhysicalAnalysis() {
    return this.buildPhysicalAnalysis('create')
  },
  updatePhysicalAnalysis() {
    return this.buildPhysicalAnalysis('update')
  },
  buildPhysicalAnalysis(action) {
    let paramsGraphqlArgument = '$diastolic: Float, $donation_id: Int!, $employee_id: Int!, $observations: String, $pulse: Float, $register_at: Date!, $register_id: Int!, $systolic: Float, $tall: Float, $temperature: Float, $weight: Float'
    if (action === 'update') {
      paramsGraphqlArgument = '$diastolic: Float, $donation_id: Int, $employee_id: Int, $id: Int!, $observations: String, $pulse: Float, $register_at: Date, $register_id: Int, $systolic: Float, $tall: Float, $temperature: Float, $weight: Float'
    }
    const paramsResolve = generics.buildGraphqlParams(paramsGraphqlArgument)

    return `
    mutation ${action}PhysicalAnalysis(${paramsGraphqlArgument} ) {
      ${action}_${SINGLE_MODEL}(${paramsResolve}) {
        ${SINGLE_MODEL} {
          id
        }
      }
    }
    `
  }
}

export default physicalAnalysis

import generics from './generics'

const MODEL = 'exams'
const SINGLE_MODEL = 'exam'

const exams = {
  list(listQuery) {
    const query = generics.buildParams(listQuery)

    return `query listExams($id: Int, $ordering: String, $register_at: Date, $register_at__gte: Date, $register_at__lte: Date,
        $search: String, $limit: Int, $offset: Int){
        exams(id: $id, ordering: $ordering, register_at: $register_at, register_at__gte: $register_at__gte,
            register_at__lte: $register_at__lte, search: $search) {
            totalCount
            results(limit: $limit, offset: $offset) {
                id
                hematocrit
                hemoglobin
                blood_group
                chagas
                rpr
                observations
                register_at
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
                        gender
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
  createExam() {
    return this.buildExam('create')
  },
  updateExam() {
    return this.buildExam('update')
  },
  buildExam(action) {
    let paramsGraphqlArgument = '$blood_group: String, $chagas: String, $donation_id: Int!, $employee_id: Int!, $hematocrit: Float, $hemoglobin: Float, $observations: String, $register_at: Date!, $register_id: Int!, $rpr: String'
    if (action === 'update') {
      paramsGraphqlArgument = '$blood_group: String, $chagas: String, $donation_id: Int, $employee_id: Int, $hematocrit: Float, $hemoglobin: Float, $id: Int!, $observations: String, $register_at: Date, $register_id: Int, $rpr: String'
    }
    const paramsResolve = generics.buildGraphqlParams(paramsGraphqlArgument)

    return `
    mutation ${action}Exam(${paramsGraphqlArgument} ) {
      ${action}_${SINGLE_MODEL}(${paramsResolve}) {
        ${SINGLE_MODEL} {
          id
        }
      }
    }
    `
  }
}

export default exams

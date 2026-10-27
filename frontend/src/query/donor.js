import generics from './generics'

const MODEL = 'donors'
const SINGLE_MODEL = 'donor'

const donors = {
  list(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `    id
           code
           first_name
           last_name
           middle_name
           age
           birth_date
           residence
           department
           civil_status
           gender
           country
           can_donate
           is_volunteer
           zone
           province
           phone
           mobile_phone
           family_phone
           profession
           degree_instruction
           job
           job_address
           email
           is_available_for_new_donation
           last_effective_donation_at
           donations {
             type_donation
             last_donation_at
             register_at
             employee {
               first_name
               middle_name
               last_name
             }
             place {
               name
             }
             clinicalhistoryanswer {
               id
             }
             rejected {
               id
             }
             exam {
               id
             }
             physicalanalysis {
               id
             }
             extraction {
               id
             }
           }
      }
      }
      }`
  },
  showDonor(id) {
    return `{` +
      SINGLE_MODEL + `(id: ` + id + `) {
           id
           ci
           ci_extension
           code
           code_other
           image
           civil_status
           first_name
           middle_name
           last_name
           birth_date
           age
           gender
           country
           can_donate
           is_volunteer
           residence
           zone
           province
           department
           phone
           mobile_phone
           family_phone
           profession
           degree_instruction
           job
           job_address
           email
           quantity_provision
           quantity_va_donation
           is_available_for_new_donation
           last_effective_donation_at
           group_abo
           factor_rh
           donations {
             id
             type_donation
             last_donation_at
             register_at
             age_donor
             employee {
               first_name
               middle_name
               last_name
             }
             place {
               name
             }
             clinicalhistoryanswer {
               id
             }
             rejected {
               id
             }
             exam {
               id
               blood_group
             }
             physicalanalysis {
               id
             }
             immunohematology {
                 id
                 direct_abo
                 factor_rh
             }
             extraction {
               id
             }
           }
        }
      }`
  },
  getDonorProvisionList(id) {
    return `{` +
      SINGLE_MODEL + `(id: ` + id + `) {
           id
           code
           quantity_provision
           quantity_va_donation
        }
      }`
  },
  list_small(listQuery) {
    const query = generics.buildParams(listQuery)
    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `    id
           ci
           ci_extension
           code
           code_other
           first_name
           last_name
           middle_name
           age
           birth_date
           gender
           can_donate
           is_available_for_new_donation
           last_effective_donation_at
           donations {
             last_donation_at
             register_at
             extraction {
              id
             }
           }
         }
        }
      }`
  },
  list_volunteers(listQuery) {
    const query = generics.buildParams(listQuery)
    return `{` +
      MODEL + `(` + query + `, donations__type_donation: "VA") {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `    id
           code
           first_name
           last_name
           middle_name
           age
           birth_date
           gender
           can_donate
           is_available_for_new_donation
           last_effective_donation_at
           donations {
             last_donation_at
             register_at
           }
      }
      }
      }`
  },
  donation_select(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `    id
           code
           first_name
           last_name
           middle_name
      }
      }
      }`
  },
  createDonor() {
    return this.buildDonor('create')
  },
  updateDonor() {
    return this.buildDonor('update')
  },
  joinDonor() {
    return this.buildDonor('join')
  },
  buildDonor(action) {
    let paramsGraphqlArgument = '$ci: String, $ci_extension: String, $birth_date: Date!, $civil_status: String, $code: String!, $code_other: String, $country: String!, $degree_instruction: String!, $department: String!, $email: String, $family_phone: Int, $first_name: String!, $gender: String!, $is_volunteer: Boolean, $job: String, $job_address: String, $last_name: String!, $middle_name: String, $mobile_phone: Int, $phone: Int, $profession: String, $province: String, $residence: String!, $zone: String'
    if (action === 'update') {
      paramsGraphqlArgument = '$ci: String, $ci_extension: String, $birth_date: Date, $civil_status: String, $code: String, $code_other: String, $country: String, $degree_instruction: String, $department: String, $email: String, $family_phone: Int, $first_name: String, $gender: String, $id: Int!, $is_volunteer: Boolean, $job: String, $job_address: String, $last_name: String, $middle_name: String, $mobile_phone: Int, $phone: Int, $profession: String, $province: String, $residence: String, $zone: String'
    } else if (action === 'join') {
      paramsGraphqlArgument = '$id: Int!, $items: GenericScalar!'
    }
    const paramsResolve = generics.buildGraphqlParams(paramsGraphqlArgument)

    return `
    mutation ${action}Donor(${paramsGraphqlArgument} ) {
      ${action}_${SINGLE_MODEL}(${paramsResolve}) {
        ${SINGLE_MODEL} {
          id
        }
      }
    }
    `
  },
  getNextCode() {
    return `{ next_donor_code } `
  }
}

export default donors

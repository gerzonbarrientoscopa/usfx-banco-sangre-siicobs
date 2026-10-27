import generics from './generics'

const MODEL = 'patients'
const SINGLE_MODEL = 'patient'

const patients = {
  list(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `    id
           first_name
           last_name
           middle_name
           phone
           register_at
           ci
           birth_date
           is_real_birthdate
           gender
           institution {
            id
            name
           }
      }
      }
      }`
  },
  donation_select(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{
      patients(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `    id
           first_name
           last_name
           middle_name
      }
      }
      }`
  },
  distribution_select(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{
      patients(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `    id
           first_name
           last_name
           middle_name
      }
      }
      }`
  },
  package_select(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{
      patients(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `    id
           first_name
           last_name
           middle_name
      }
      }
      }`
  },
  createPatient() {
    return this.buildPatient('create')
  },
  updatePatient() {
    return this.buildPatient('update')
  },
  buildPatient(action) {
    let paramsGraphqlArgument = '$first_name: String!, $institution_id: Int, $last_name: String, $middle_name: String!, $phone: Int,' +
        '$ci: String, $birth_date: Date, $gender: String!, $is_real_birthdate: Boolean!'
    if (action === 'update') {
      paramsGraphqlArgument = '$id: Int!, $first_name: String!, $institution_id: Int, $last_name: String, $middle_name: String!, $phone: Int,' +
          '$ci: String, $birth_date: Date, $gender: String!, $is_real_birthdate: Boolean!'
    }
    const paramsResolve = generics.buildGraphqlParams(paramsGraphqlArgument)

    return `
    mutation ${action}Patient(${paramsGraphqlArgument} ) {
      ${action}_${SINGLE_MODEL}(${paramsResolve}) {
        ${SINGLE_MODEL} {
          id
        }
      }
    }
    `
  }
}

export default patients

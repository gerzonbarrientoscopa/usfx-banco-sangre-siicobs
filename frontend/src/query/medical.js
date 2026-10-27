import generics from './generics'

const MODEL = 'medicals'
const SINGLE_MODEL = 'medical'

const medicals = {
  get(id) {
    return `{
      ${SINGLE_MODEL}(id: ${id}) {
            id
            first_name
            middle_name
            last_name
            register_at
            institution {
              id
              name
              address
              phone
            }
      }
      }`
  },
  list(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{
      ${MODEL}(${query}) {
      totalCount
      results(limit: ${listQuery.limit}, offset: ${listQuery.offset}) {
            id
            first_name
            middle_name
            last_name
            register_at
            institution {
              id
              name
              address
              phone
            }
      }
      }
      }`
  },
  phlebotomy_select(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{
      ${MODEL}(${query}) {
      totalCount
      results(limit: ${listQuery.limit}, offset: ${listQuery.offset}) {
            id
            first_name
            middle_name
            last_name
      }
      }
      }`
  },
  distribution_select(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{
      ${MODEL}(${query}) {
      totalCount
      results(limit: ${listQuery.limit}, offset: ${listQuery.offset}) {
            id
            first_name
            middle_name
            last_name
            institution {
              id
              name
              address
              phone
            }
      }
      }
      }`
  },
  createMedical() {
    return this.buildMedical('create')
  },
  updateMedical() {
    return this.buildMedical('update')
  },
  buildMedical(action) {
    let paramsGraphqlArgument = '$institution_id: Int!, $first_name: String!, $last_name: String, $middle_name: String'

    if (action === 'update') {
      paramsGraphqlArgument = '$id: Int!, $institution_id: Int, $first_name: String, $last_name: String, $middle_name: String'
    }

    const paramsResolve = generics.buildGraphqlParams(paramsGraphqlArgument)

    return `
    mutation ${action}Medical(${paramsGraphqlArgument}) {
      ${action}_${SINGLE_MODEL}(${paramsResolve} ) {
        ${SINGLE_MODEL} {
          id
        }
      }
    }
    `
  }
}

export default medicals

import generics from './generics'

const MODEL = 'institutions'
const SINGLE_MODEL = 'institution'

const institutions = {
  list(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{
      ` + MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `   id
          name
          nit
          logo
          address
          phone
          type
          department
          register_at
      }
      }
      }`
  },
  donor_select(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{
      ` + MODEL + `(` + query + `) {
      totalCount
      results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {
         id
         name
         type
      }
      }
      }`
  },
  medical_select(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{
      ` + MODEL + `(` + query + `) {
      totalCount
      results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {
         id
         name
         type
      }
      }
      }`
  },
  distribution_select(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{
      ` + MODEL + `(` + query + `) {
      totalCount
      results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {
         id
         name
         type
      }
      }
      }`
  },
  institution_billing_select(listQuery) {
    let query = generics.buildParams(listQuery)

    query += ', has_distribution: ' + true
    query += ', distribution_type_payment: ' + 1

    if (listQuery.institution_billing_month) {
      query += ', institution_billing_month: ' + listQuery.institution_billing_month
      // query += ', institution_billing_year: ' + listQuery.institution_billing_year
      query += ', distribution_month: ' + listQuery.institution_billing_month
      query += ', distribution_year: ' + listQuery.institution_billing_year
    }

    return `{
      ` + MODEL + `(` + query + `) {
      totalCount
      results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {
         id
         name
         type
      }
      }
      }`
  },
  createInstitution() {
    return this.buildInstitution('create')
  },
  updateInstitution() {
    return this.buildInstitution('update')
  },
  joinInstitution() {
    return this.buildInstitution('join')
  },
  buildInstitution(action) {
    let paramsGraphqlArgument = '$address: String, $department: String!, $name: String!, $dosage_key: String, $type: String, $nit: String, $nro_authorization: String, $phone: Int'
    if (action === 'update') {
      paramsGraphqlArgument = '$id: Int!, $address: String, $department: String, $name: String, $dosage_key: String, $type: String, $nit: String, $nro_authorization: String, $phone: Int'
    } else if (action === 'join') {
      paramsGraphqlArgument = '$id: Int!, $items: GenericScalar!'
    }
    const paramsResolve = generics.buildGraphqlParams(paramsGraphqlArgument)

    return `
    mutation ${action}Institution(${paramsGraphqlArgument} ) {
      ${action}_${SINGLE_MODEL}(${paramsResolve}) {
        ${SINGLE_MODEL} {
          id
          name
        }
      }
    }
    `
  }
}

export default institutions

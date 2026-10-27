import generics from './generics'

// const MODEL = 'donorhistories'
const SINGLE_MODEL = 'donorhistory'

const donorHistories = {
  createDonorHistory() {
    return this.buildDonorHistory('create')
  },
  buildDonorHistory(action) {
    const paramsGraphqlArgument = '$donor_id: Int!, $employee_id: Int!, $reason: String!, $register_at: Date!'
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
  }
}

export default donorHistories

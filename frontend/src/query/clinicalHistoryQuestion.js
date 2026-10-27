import generics from './generics'

const MODEL = 'clinicalhistoryquestions'
const SINGLE_MODEL = 'clinicalhistoryquestion'

const clinicalHistoryQuestions = {
  list(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `   id
          title
          questions
          is_active
          register_at
      }
      }
      }`
  },
  clinicalHistory_select(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `   id
          title
          questions
          is_active
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
    let paramsGraphqlArgument = '$is_active: Boolean!, $questions: GenericScalar, $register_at: Date, $title: String!'
    if (action === 'update') {
      paramsGraphqlArgument = '$id: Int!, $is_active: Boolean, $questions: GenericScalar, $register_at: Date, $title: String'
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

export default clinicalHistoryQuestions

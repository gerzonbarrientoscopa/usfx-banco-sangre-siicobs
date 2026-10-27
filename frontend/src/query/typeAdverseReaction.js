import generics from './generics'

const MODEL = 'typeadversereactions'
const SINGLE_MODEL = 'typeadversereaction'

const typeAdverseReactions = {
  list(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{
    ${MODEL}(${query}) {
      totalCount
        results(limit: ${listQuery.limit}, offset: ${listQuery.offset}){
          id
          name
          show_in_conventional
          show_in_apheresis
          level
        }
      }
    }`
  },
  adverseReaction_select(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{
    ${MODEL}(${query}) {
      totalCount
        results(limit: ${listQuery.limit}, offset: ${listQuery.offset}) {
          id
          name
          show_in_conventional
          show_in_apheresis
          level
        }
      }
    }`
  },

  createTypeAdverseReaction() {
    return this.buildTypeAdverseReaction('create')
  },
  updateTypeAdverseReaction() {
    return this.buildTypeAdverseReaction('update')
  },
  buildTypeAdverseReaction(action) {
    let paramsGraphqlArgument = '$level: String!, $name: String!, $show_in_apheresis: Boolean!, $show_in_conventional: Boolean!'
    if (action === 'update') {
      paramsGraphqlArgument = '$id: Int!, $level: String, $name: String, $show_in_apheresis: Boolean, $show_in_conventional: Boolean'
    }
    const paramsResolve = generics.buildGraphqlParams(paramsGraphqlArgument)

    return `
    mutation ${action}TypeAdverseReaction(${paramsGraphqlArgument} ) {
      ${action}_${SINGLE_MODEL}(${paramsResolve}) {
        ${SINGLE_MODEL} {
          id
        }
      }
    }
    `
  }
}

export default typeAdverseReactions

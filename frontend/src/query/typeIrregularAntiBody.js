import generics from './generics'

const MODEL = 'type_irregular_antibodies'

const TypeIrregularAntiBodies = {
  list(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{
      ${MODEL} (${query}) {
      totalCount
      results(limit: ${listQuery.limit} , offset: ${listQuery.offset} ) {
            id
            name
            recommendation
      }
      }
      }`
  }
}

export default TypeIrregularAntiBodies

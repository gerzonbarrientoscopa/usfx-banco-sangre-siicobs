import generics from './generics'

const MODEL = 'groups'

const groups = {
  userSelect(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `      id
             name
      }
      }
      }`
  }
}
export default groups

import generics from './generics'

const MODEL = 'groupitems'
const SINGLE_MODEL = 'groupitem'

const groupItems = {
  list(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `     id
            name
            init_code
            is_active
      }
      }
      }`
  },
  next_code() {
    return `{ next_code_group_item }`
  },
  createGroupItem() {
    return this.buildGroupItem('create')
  },
  updateGroupItem() {
    return this.buildGroupItem('update')
  },
  buildGroupItem(action) {
    let paramsGraphqlArgument = '$init_code: Int!, $is_active: Boolean!, $name: String!'
    if (action === 'update') {
      paramsGraphqlArgument = '$id: Int!, $init_code: Int, $is_active: Boolean, $name: String'
    }
    const paramsResolve = generics.buildGraphqlParams(paramsGraphqlArgument)

    return `
    mutation ${action}GroupItem(${paramsGraphqlArgument} ) {
      ${action}_${SINGLE_MODEL}(${paramsResolve}) {
        ${SINGLE_MODEL} {
          id
        }
      }
    }
    `
  }
}

export default groupItems

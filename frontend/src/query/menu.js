import generics from './generics'

const MODEL = 'menus'
const SINGLE_MODEL = 'menu'

const menus = {
  list(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `   id
          name
          only_volunteer
          register_at
      }
      }
      }`
  },
  createMenu() {
    return this.buildMenu('create')
  },
  updateMenu() {
    return this.buildMenu('update')
  },
  buildMenu(action) {
    let paramsGraphqlArgument = '$name: String!, $only_volunteer: Boolean!'
    if (action === 'update') {
      paramsGraphqlArgument = '$id: Int!, $name: String, $only_volunteer: Boolean'
    }
    const paramsResolve = generics.buildGraphqlParams(paramsGraphqlArgument)

    return `
    mutation ${action}Menu(${paramsGraphqlArgument} ) {
      ${action}_${SINGLE_MODEL}(${paramsResolve}) {
        ${SINGLE_MODEL} {
          id
        }
      }
    }
    `
  }
}

export default menus

import generics from './generics'

const SINGLE_MODEL = 'user'

const users = {
  createUser() {
    return this.buildUser('create')
  },
  updateUser() {
    return this.buildUser('update')
  },
  buildUser(action) {
    let paramsGraphqlArgument = '$group_ids: [Int]!, $password: String!, $profile_id: Int!, $username: String!'
    if (action === 'update') {
      paramsGraphqlArgument = '$id: Int!, $group_ids: [Int], $password: String, $is_active: Boolean'
    }

    const paramsResolve = generics.buildGraphqlParams(paramsGraphqlArgument)

    return `
    mutation ${action}User(${paramsGraphqlArgument}) {
      ${action}_${SINGLE_MODEL}(${paramsResolve} ) {
        ${SINGLE_MODEL} {
          id
        }
      }
    }
    `
  }
}

export default users

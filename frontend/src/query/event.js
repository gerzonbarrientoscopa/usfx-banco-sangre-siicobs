import generics from './generics'

const MODEL = 'events'
const SINGLE_MODEL = 'event'

const events = {
  getEvent(id) {
    return `{
      event (id: ${id}) {
           id
           name
           init_at
           end_at
           is_active
      }
      }`
  },
  list(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{
      events (` + query + `) {
      totalCount
      results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {
           id
           name
           init_at
           end_at
           is_active
      }
      }
      }`
  },
  list_for_calendar() {
    return `
      query getCalendarEvents($date: String, $filter: String) {
        calendar_events(date: $date, filter: $filter)
      }
    `
  },
  donation_select(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `    id
           name
           init_at
           end_at
           is_active
    }
    }
  }`
  },
  createEvent() {
    return this.buildEvent('create')
  },
  updateEvent() {
    return this.buildEvent('update')
  },
  deleteEvent() {
    return this.buildEvent('delete')
  },
  buildEvent(action) {
    let paramsGraphqlArgument = '$end_at: DateTime, $init_at: DateTime!, $is_active: Boolean, $name: String!'
    if (action === 'update') {
      paramsGraphqlArgument = '$end_at: DateTime, $id: Int!, $init_at: DateTime, $is_active: Boolean, $name: String'
    } else if (action === 'delete') {
      paramsGraphqlArgument = '$id: Int!'
    }
    const paramsResolve = generics.buildGraphqlParams(paramsGraphqlArgument)

    return `
    mutation ${action}Event(${paramsGraphqlArgument} ) {
      ${action}_${SINGLE_MODEL}(${paramsResolve}) {
        ${SINGLE_MODEL} {
          id
        }
      }
    }
    `
  }
}

export default events

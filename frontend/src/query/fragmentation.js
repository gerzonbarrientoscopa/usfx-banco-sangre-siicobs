import generics from './generics'

const MODEL = 'fragmentations'
const SINGLE_MODEL = 'fragmentation'

const fragmentations = {
  list(listQuery) {
    const query = generics.buildParams(listQuery)

    return `query queryFragmentations(
    $employee_id: Decimal, $extraction__donation__donor__age: Decimal, $extraction__donation__donor__age__gte: Decimal,
    $extraction__donation__donor__age__lte: Decimal, $extraction__donation__donor__gender: String,
    $extraction__donation__event__id: Decimal, $extraction__donation__event__isnull: Boolean,
    $extraction__donation__rejected__isnull: Boolean, $extraction__donation__rejected__reason__id: Decimal,
    $extraction__donation__rejected__reason__type: String, $extraction__donation__type_donation: String,
    $extraction__donation__id: Int, $id: Int, $ordering: String, $register_at: Date, $register_at__gte: Date,
    $register_at__lt: Date, $register_at__lte: Date, $search: String, $limit: Int, $offset: Int
    ){
      fragmentations(
    employee_id: $employee_id, extraction__donation__donor__age: $extraction__donation__donor__age,
        extraction__donation__donor__age__gte: $extraction__donation__donor__age__gte,
        extraction__donation__donor__age__lte: $extraction__donation__donor__age__lte,
        extraction__donation__donor__gender: $extraction__donation__donor__gender,
        extraction__donation__event__id: $extraction__donation__event__id,
        extraction__donation__event__isnull: $extraction__donation__event__isnull,
        extraction__donation__rejected__isnull: $extraction__donation__rejected__isnull,
        extraction__donation__rejected__reason__id: $extraction__donation__rejected__reason__id,
        extraction__donation__rejected__reason__type: $extraction__donation__rejected__reason__type,
        extraction__donation__type_donation: $extraction__donation__type_donation, extraction__donation__id: $extraction__donation__id,
        id: $id, ordering: $ordering, register_at: $register_at, register_at__gte: $register_at__gte,
        register_at__lt: $register_at__lt, register_at__lte: $register_at__lte, search: $search
      ) {
      totalCount
      results(limit: $limit, offset: $offset) {
            id
            quality_bag
            total_hc
            observations
            register_at
            donor_code
            total_itemfragmentations
            employee {
                id
                first_name
                middle_name
                last_name
            }
            register {
                id
                first_name
                middle_name
                last_name
            }
            extraction {
                id
                tubing
                weight
                bags_quantity
                register_at
                donation {
                  id
                  donor {
                    code
                  }
                }
            }
      }
      }
      }`
  },
  get(id) {
    return `{
         ${SINGLE_MODEL} (id: ${id}) {
            id
            quality_bag
            total_hc
            observations
            register_at
            donor_code
            itemfragmentations {
              id
              is_satellite_bag
              is_max_expiration_days
              lot
              tubing
              typehemocomponent {
                id
                name
                expiration_day
                is_pediatric
                can_add_bags
                max_expiration_days
              }
              typediscard {
                id
                name
              }
              expiration_date
              weight
              status
              observations
            }
            employee
            {
                id
                first_name
                middle_name
                last_name
            }
            register
            {
                id
                first_name
                middle_name
                last_name
            }
            extraction
            {
                id
                tubing
                weight
                bags_quantity
                register_at
                donation
                {
                    id
                    type_donation
                    register_at
                    last_donation_at
                    donor
                    {
                        id
                        code
                        first_name
                        middle_name
                        last_name
                    }
                    rejected
                    {
                        id
                        reason {
                          id
                          name
                          type
                        }
                    }
                }
            }
      }
      }`
  },
  listReportFragmentation(listQuery) {
    let query = generics.buildParams(listQuery)

    let queryParams = ''

    for (const key in listQuery) {
      switch (key) {
        case 'extra':
          if (listQuery[key]['employee_id'] !== '') {
            queryParams += 'employee_id: ' + listQuery[key]['employee_id'] + ', '
          }
          break
      }
    }

    if (query !== '') {
      query += ', ' + queryParams
    } else {
      query = queryParams
    }

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `     id
            quality_bag
            total_hc
            observations
            register_at
            itemfragmentations {
              id
              typehemocomponent {
                id
                name
              }
              typediscard {
                id
                name
              }
              expiration_date
              weight
              status
              observations
            }
            employee
            {
                id
                first_name
                middle_name
                last_name
            }
            extraction
            {
                id
                tubing
                bags_quantity
                weight
                donation
                {
                    id
                    type_donation
                    register_at
                    last_donation_at
                    donor
                    {
                        id
                        code
                        first_name
                        middle_name
                        last_name
                    }
                    rejected
                    {
                        id
                        reason {
                          id
                          name
                          type
                        }
                    }
                }
            }
      }
      }
      }`
  },
  createFragmentation() {
    return this.buildFragmentation('create')
  },
  updateFragmentation() {
    return this.buildFragmentation('update')
  },
  buildFragmentation(action) {
    let paramsGraphqlArgument = '$donor_code: Int!, $employee_id: Int!, $extraction_id: Int, $itemfragmentations: GenericScalar, $observations: String, $quality_bag: String!, $register_at: DateTime!, $register_id: Int!, $total_hc: Float!'
    if (action === 'update') {
      paramsGraphqlArgument = '$donor_code: Int!, $employee_id: Int, $extraction_id: Int, $id: Int!, $itemfragmentations: GenericScalar, $observations: String, $quality_bag: String, $register_at: DateTime, $register_id: Int, $total_hc: Float'
    }
    const paramsResolve = generics.buildGraphqlParams(paramsGraphqlArgument)

    return `
    mutation ${action}Fragmentation(${paramsGraphqlArgument} ) {
      ${action}_${SINGLE_MODEL}(${paramsResolve}) {
        ${SINGLE_MODEL} {
          id
        }
      }
    }
    `
  }
}

export default fragmentations

import generics from './generics'

const MODEL = 'extractions'
const SINGLE_MODEL = 'extraction'

const extractions = {
  listExtraction(listQuery) {
    return `
      query queryExtractions($limit: Int, $offset: Int, $apheresis__isnull: Boolean, $donation__donor__age: Decimal,
        $donation__donor__age__gte: Decimal, $donation__donor__age__lte: Decimal, $donation__donor__gender: String,
        $donation__event__id: Decimal, $donation__event__isnull: Boolean, $donation__rejected__isnull: Boolean,
        $donation__rejected__reason__type: String, $donation__type_donation: String, $donation__id: Int,
        $extractionrefreshment__isnull: Boolean, $fragmentation__isnull: Boolean, $id: Int, $immunohematology__isnull: Boolean,
        $immunoserology__isnull: Boolean, $ordering: String, $register_at: Date, $register_at__gte: Date, $register_at__lte: Date,
        $search: String, $selfexclusion__isnull: Boolean){
      extractions(apheresis__isnull: $apheresis__isnull, donation__donor__age: $donation__donor__age,
        donation__donor__age__gte: $donation__donor__age__gte, donation__donor__age__lte: $donation__donor__age__lte,
        donation__donor__gender: $donation__donor__gender, donation__event__id: $donation__event__id,
        donation__event__isnull: $donation__event__isnull, donation__rejected__isnull: $donation__rejected__isnull,
        donation__rejected__reason__type: $donation__rejected__reason__type, donation__type_donation: $donation__type_donation,
        donation__id: $donation__id, extractionrefreshment__isnull: $extractionrefreshment__isnull, fragmentation__isnull: $fragmentation__isnull,
        id: $id, immunohematology__isnull: $immunohematology__isnull, immunoserology__isnull: $immunoserology__isnull,
        ordering: $ordering, register_at: $register_at, register_at__gte: $register_at__gte, register_at__lte: $register_at__lte,
        search: $search, selfexclusion__isnull: $selfexclusion__isnull) {
      totalCount
      results(limit: $limit, offset: $offset) {
            id
            type_place
            tubing
          	lot
          	weight
            bags_quantity
            type_bag
            arm
            initial_time
            end_time
            total_time
            observations
          	register_at
          	register {
              id
            }
            employee {
              id
              first_name
              middle_name
              last_name
            }
            adversereaction {
              id
            }
            extractionrefreshment {
              id
            }
            fragmentation {
              id
            }
            donation {
                id
                register_at
                donor {
                    id
                    code
                }
            }
      }
      }
      }`
  },
  getExtraction(id) {
    return `query extractionOne($id: ID!){
        extraction(id: $id) {
            id
            type_place
            tubing
            barcode
            weight
            lot
            bags_quantity
            type_bag
            arm
            initial_time
            end_time
            total_time
            observations
            register_at
            register{
                id
                first_name
                middle_name
                last_name
            }
            employee {
                id
                first_name
                middle_name
                last_name
            }
            adversereaction {
                id
            }
            extractionrefreshment {
                id
            }
            fragmentation {
                id
            }
            donation
            {
                id
                register_at
                type_donation
                donor {
                    id
                    code
                    first_name
                    middle_name
                    last_name
                }
            }
            typeanticoagulant {
                id
                name
            }
        }
    }`
  },
  adverseReactionExtractionSelect(listQuery) {
    let query = generics.buildParams(listQuery)
    query += (query !== '' ? ',' : '') + 'adversereaction__isnull: true'

    return `{
      ${MODEL} (${query}) {
      totalCount
      results(limit: ${listQuery.limit}, offset: ${listQuery.offset}) {
            id
            donation
            {
                id
                register_at
                donor
                {
                    id
                    code
                }
            }
      }
      }
      }`
  },
  apheresisDonationSelect(listQuery) {
    let query = generics.buildParams(listQuery)
    query += (query !== '' ? ',' : '') + 'apheresis__isnull: true'

    return `{
      ${MODEL} (${query}) {
      totalCount
      results(limit: ${listQuery.limit}, offset: ${listQuery.offset}) {
            id
            donation
            {
                id
                register_at
                donor
                {
                    id
                    code
                }
            }
      }
      }
      }`
  },
  selfExclusionExtractionSelect(listQuery) {
    let query = generics.buildParams(listQuery)
    query += (query !== '' ? ',' : '') + 'selfexclusion__isnull: true'

    return `{
      ${MODEL} (${query}) {
      totalCount
      results(limit: ${listQuery.limit}, offset: ${listQuery.offset}) {
            id
            donation
            {
                id
                register_at
                donor
                {
                    id
                    code
                }
            }
      }
      }
      }`
  },
  refreshmentExtractionSelect(listQuery) {
    let query = generics.buildParams(listQuery)
    query += (query !== '' ? ',' : '') + ' extractionrefreshment__isnull: true'

    return `{
      ${MODEL} (${query}) {
      totalCount
      results(limit: ${listQuery.limit}, offset: ${listQuery.offset}) {
            id
            donation
            {
                id
                register_at
                donor
                {
                    id
                    code
                }
            }
      }
      }
      }`
  },
  fragmentationExtractionSelect(listQuery) {
    let query = generics.buildParams(listQuery)
    query += (query !== '' ? ',' : '') + 'fragmentation__isnull: true'

    return `{
      ${MODEL} (${query}) {
      totalCount
      results(limit: ${listQuery.limit}, offset: ${listQuery.offset}) {
            id
            created_at
            register_at
            bags_quantity
            type_bag
            tubing
            weight
            donation {
                id
                register_at
                donor {
                    id
                    code
                }
            }
      }
      }
      }`
  },
  show(listQuery) {
    const query = generics.buildShowParams(listQuery)

    return `{` +
      SINGLE_MODEL + `(` + query + `) {
           id
           fragmentation {
             id
           }
           donation {
              id
              donor {
                id
                code
              }
              exam {
                  id
                  blood_group
                  chagas
                  rpr
              }
           }
        }
      }`
  },
  createExtraction() {
    return this.buildExtraction('create')
  },
  updateExtraction() {
    return this.buildExtraction('update')
  },
  buildExtraction(action) {
    let paramsGraphqlArgument = '$type_place: String!, $arm: String, $type_bag: String!, $barcode: String, $donation_id: Int!, $employee_id: Int!, $end_time: Time, $initial_time: Time!, $lot: String!, $observations: String, $register_at: Date!, $register_id: Int!, $total_time: Float, $tubing: String, $weight: Float, $typeanticoagulant_id: Int!'
    if (action === 'update') {
      paramsGraphqlArgument = '$type_place: String, $arm: String, $type_bag: String, $barcode: String, $donation_id: Int, $employee_id: Int, $end_time: Time, $id: Int!, $initial_time: Time, $lot: String, $observations: String, $register_at: Date, $register_id: Int, $total_time: Float, $tubing: String, $weight: Float'
    }
    const paramsResolve = generics.buildGraphqlParams(paramsGraphqlArgument)

    return `
    mutation ${action}Extraction(${paramsGraphqlArgument} ) {
      ${action}_${SINGLE_MODEL}(${paramsResolve}) {
        ${SINGLE_MODEL} {
          id
        }
      }
    }
    `
  }
}

export default extractions

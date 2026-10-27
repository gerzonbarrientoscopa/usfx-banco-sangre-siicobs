import generics from './generics'

const MODEL = 'distribution_itemfragmentations'

const itemDistribution = {
  list(listQuery) {
    let query = generics.buildParams(listQuery)

    if (listQuery.distribution__id) {
      query += ', distribution__id: ' + listQuery.distribution__id
    }

    return `{
      ${MODEL} ( ${query} ) {
      totalCount
      results(limit: ${listQuery.limit}, offset: ${listQuery.offset}) {
              id
              distributionitemfragmentationrefunded {
                id
                reason
              }
              itemfragmentation {
                id
                donor_code
                expiration_date
                weight
                status
                typehemocomponent {
                  id
                  name
                }
                fragmentation {
                  id
                  extraction {
                    id
                    tubing
                  }
                }
              }
          }
      }
      }`
  },
  listReport(listQuery) {
    let query = generics.buildParams(listQuery)
    if (listQuery.type_payment !== '') {
      query += ', type_payment: ' + listQuery.type_payment
    }

    return `{
      ${MODEL} ( ${query} ) {
      totalCount
      results(limit: ${listQuery.limit}, offset: ${listQuery.offset}) {
              id
              distributionitemfragmentationrefunded {
                id
                reason
              }
              distribution {
                id
                uuid
                is_delivered
                type_payment
                register_at
                employee {
                  id
                  first_name
                  last_name
                  middle_name
                }
              }
              itemfragmentation {
                id
                donor_code
                expiration_date
                weight
                status
                fragmentation {
                  extraction {
                    donation {
                      donor{
                        group_abo
                        factor_rh
                      }
                    }
                  }
                }
                typehemocomponent {
                  id
                  name
                }
              }
          }
      }
      }`
  },
  change_item_distribution() {
    return `mutation createDistributionItemFragmentationRefunded($id: Int!, $reason: String!){
              create_distribution_item_fragmentation_refunded(id: $id, reason: $reason)
              {
                  distribution_item_fragmentation_refunded {
                    id
                    reason
                  }
              }
            }`
  }
}
export default itemDistribution

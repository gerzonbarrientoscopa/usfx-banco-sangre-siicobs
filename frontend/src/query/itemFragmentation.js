import generics from './generics'

const MODEL = 'itemfragmentations'

const itemFragmentations = {
  list(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{
      ${MODEL} ( ${query} ) {
      totalCount
      results(limit: ${listQuery.limit}, offset: ${listQuery.offset}) {
            id
            donor_code
            expiration_date
            weight
            status
            observations
            register_at
            fragmentation {
              id
              extraction {
                id
                tubing
                bags_quantity
                type_bag
                donation
                {
                    id
                    register_at
                }
              }
            }
            typehemocomponent {
              id
              name
              acronym
            }
      }
      }
      }`
  },
  listFragmentation(listQuery) {
    let query = generics.buildParams(listQuery)

    if (listQuery.fragmentation__id) {
      query += ', fragmentation__id: ' + listQuery.fragmentation__id
    }

    return `{
      ${MODEL} ( ${query} ) {
      totalCount
      results(limit: ${listQuery.limit}, offset: ${listQuery.offset}) {
            id
            donor_code
            expiration_date
            weight
            status
            observations
            register_at
            is_satellite_bag
            fragmentation {
              id
              extraction {
                id
                tubing
                bags_quantity
                type_bag
                donation {
                    id
                    register_at
                }
              }
            }
            typehemocomponent {
              id
              name
              acronym
            }
            typediscard {
              id
              name
            }
      }
      }
      }`
  },
  listProduction(listQuery) {
    let query = generics.buildParams(listQuery)

    if (query === '') {
      query = 'release__isnull: false'
      query += ', item_register_at__gte: "' + listQuery['extra']['date_init'] + '", item_register_at__lte: "' + listQuery['extra']['date_end'] + '", '
    } else {
      query += ', release__isnull: false'
      query += ', item_register_at__gte: "' + listQuery['extra']['date_init'] + '", item_register_at__lte: "' + listQuery['extra']['date_end'] + '", '
    }

    return `{
      ${MODEL} ( ${query} ) {
      totalCount
      results(limit: ${listQuery.limit}, offset: ${listQuery.offset}) {
            id
            donor_code
            typehemocomponent {
              id
              name
              acronym
            }
            release {
              id
              register_at
            }
            discard {
              id
              register_at
            }
      }
      }
      }`
  },
  listProductionReport(listQuery) {
    let query = ''
    if (query === '') {
      query = 'only_release_or_discard: "true"'
      query += ', item_register_at__gte: "' + listQuery['extra']['date_init'] + '", item_register_at__lte: "' + listQuery['extra']['date_end'] + '" '
    } else {
      query += ', only_release_or_discard: "true"'
      query += ', item_register_at__gte: "' + listQuery['extra']['date_init'] + '", item_register_at__lte: "' + listQuery['extra']['date_end'] + '" '
    }

    return `{
      ${MODEL} ( ${query} ) {
      totalCount
      results(limit: ${listQuery.limit}, offset: ${listQuery.offset}) {
            id
            donor_code
            fragmentation {
              id
            }
            typehemocomponent {
              id
              name
              acronym
            }
            release {
              id
              register_at
            }
            discard {
              id
              register_at
            }
      }
      }
      }`
  },
  listQuarantine(listQuery) {
    return `
        query queryItemfragmentations(
            $fragmentation__extraction__donation__id: Int,
            $fragmentation__id: Decimal,
            $id: Int,
            $is_distributed: String,
            $item_register_at__gte: Date,
            $item_register_at__lte: Date,
            $only_release_or_discard: String,
            $ordering: String,
            $register_at__gte: Date,
            $register_at__lte: Date,
            $search: String,
            $status: String,
            $status__in: [String], $typehemocomponent_id: Decimal, $limit: Int,
            $offset: Int){
            itemfragmentations(
                discard__isnull: true,
                fragmentation__extraction__donation__id: $fragmentation__extraction__donation__id,
                fragmentation__id: $fragmentation__id,
                id: $id,
                is_distributed: $is_distributed,
                item_register_at__gte: $item_register_at__gte,
                item_register_at__lte: $item_register_at__lte,
                only_release_or_discard: $only_release_or_discard,
                ordering: $ordering,
                register_at__gte: $register_at__gte,
                register_at__lte: $register_at__lte,
                release__isnull: true,
                search: $search,
                status: $status,
                status__in: $status__in,
                typehemocomponent_id: $typehemocomponent_id
            ) {
                totalCount
                results(limit: $limit, offset: $offset) {
                    id
                    donor_code
                    expiration_date
                    weight
                    status
                    observations
                    register_at
                    distributionitemfragmentations {
                        id
                    }
                    fragmentation {
                        id
                        extraction {
                            id
                            register_at
                            donation {
                                id
                                immunoserology {
                                    id
                                    chagas_hai
                                    hiv
                                    hbsag
                                    hvc
                                    cheia
                                    rpr
                                    is_reactive
                                }
                                immunohematology {
                                    id
                                    alb
                                    liss
                                    fsi
                                    coombs
                                    antikell
                                    exist_irregular_antibody
                                }
                            }
                        }
                        employee {
                            id
                            first_name
                            middle_name
                            last_name
                        }
                    }
                    typehemocomponent {
                        id
                        name
                        acronym
                    }
                    typediscard {
                        id
                        name
                    }
                    release {
                        id
                    }
                    discard {
                        id
                    }
                    type_irregular_antibody {
                        id
                        name
                    }

                }
            }
        }`
  },
  listHemocomponents(listQuery) {
    let query = generics.buildParams(listQuery)

    if (listQuery.typehemocomponent_id !== '') {
      query += ', typehemocomponent_id: ' + listQuery.typehemocomponent_id
    }

    if (listQuery.typeFilter !== '') {
      if (listQuery.typeFilter === 'release') {
        query += ', release__isnull: false'
      } else {
        query += ', discard__isnull: false'
      }
    }

    return `{
       ${MODEL} ( ${query} ) {
       totalCount
       results(limit: ${listQuery.limit}, offset: ${listQuery.offset}) {
            id
            donor_code
            expiration_date
            weight
            status
            register_at
            distributionitemfragmentations {
              id
            }
            fragmentation {
              id
              extraction {
                id
                register_at
                donation {
                  immunoserology {
                    id
                  }
                  immunohematology {
                    id
                  }
                }
              }
              employee {
              id
              first_name
              middle_name
              last_name
              }
            }
            typehemocomponent {
              id
              name
              acronym
            }
            typediscard {
              id
              name
            }
            release {
              id
            }
            discard {
              id
            }
            type_irregular_antibody {
              id
              name
            }

      }
      }
      }`
  },
  list_distribution(listQuery) {
    let query = generics.buildParams(listQuery)

    if (query === '') {
      query = 'release__isnull: false'
    } else {
      query += ', release__isnull: false'
    }

    return `{
      ${MODEL} ( ${query} ) {
      totalCount
      results(limit: ${listQuery.limit}, offset: ${listQuery.offset}) {
            id
            donor_code
            expiration_date
            weight
            status
            observations
            register_at
            fragmentation {
              id
              extraction {
                id
                donation {
                  immunoserology {
                    id
                    chagas_hai
                    hiv
                    hbsag
                    hvc
                    cheia
                    rpr
                  }
                  immunohematology {
                    id
                  }
                }
              }
            }
            typehemocomponent {
              id
              name
              acronym
            }
            typediscard {
              id
              name
            }
            release {
              id
            }
            discard {
              id
            }

      }
      }
      }`
  },
  listAddingDistributions(listQuery) {
    return `query queryListAddingDistributions(
        $fragmentation__extraction__donation__id: Int,
        $fragmentation__id: Decimal,
        $id: Int,
        $item_register_at__gte: Date,
        $item_register_at__lte: Date,
        $only_release_or_discard: String,
        $ordering: String,
        $register_at__gte: Date,
        $register_at__lte: Date,
        $search: String,
        $status: String,
        $status__in: [String], $typehemocomponent_id: Decimal, $limit: Int,
        $offset: Int
    ){
        itemfragmentations(
            fragmentation__extraction__donation__id: $fragmentation__extraction__donation__id,
            fragmentation__id: $fragmentation__id,
            id: $id,
            is_distributed: "true",
            item_register_at__gte: $item_register_at__gte,
            item_register_at__lte: $item_register_at__lte,
            only_release_or_discard: $only_release_or_discard,
            ordering: $ordering,
            register_at__gte: $register_at__gte,
            register_at__lte: $register_at__lte,
            release__isnull: false,
            search: $search,
            status: $status,
            status__in: $status__in,
            typehemocomponent_id: $typehemocomponent_id
        ) {
            totalCount
            results(limit: $limit, offset: $offset) {
                id
                donor_code
                expiration_date
                weight
                status
                observations
                register_at
                typehemocomponent {
                    id
                    name
                    acronym
                }
                typediscard {
                    id
                    name
                }
                release {
                    id
                }
                discard {
                    id
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
    }`
  }
}

export default itemFragmentations

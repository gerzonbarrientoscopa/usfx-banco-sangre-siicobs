import generics from './generics'

const MODEL = 'donations'
const SINGLE_MODEL = 'donation'

const donations = {
  select(listQuery) {
    const query = generics.buildParams(listQuery)

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `      id
             register_at
             donor {
               id
               first_name
               middle_name
               last_name
               code
             }
      }
      }
      }`
  },
  listForEvent(listQuery) {
    let query = generics.buildParams(listQuery)
    query += (query !== '' ? ',' : '') + `event__id: ${listQuery.event_id}`

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `     id
            type_process
            type_donation
            register_at
            last_donation_at
            donor {
              id
              code
              first_name
              middle_name
              last_name
            }
            event {
              id
              name
            }
            place {
              id
              name
            }
             employee {
              id
              first_name
              middle_name
              last_name
            }
             patient {
              id
              first_name
              middle_name
              last_name
            }
            rejected {
              id
            }
            exam {
              id
            }
            physicalanalysis {
              id
            }
            extraction {
              id
            }
      }
      }
      }`
  },
  listWithoutEvent(listQuery) {
    let query = generics.buildParams(listQuery)
    query += (query !== '' ? ',' : '') + `event__isnull: true`

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `     id
            type_process
            type_donation
            register_at
            last_donation_at
            donor {
              id
              code
              first_name
              middle_name
              last_name
            }
            event {
              id
              name
            }
            place {
              id
              name
            }
             employee {
              id
              first_name
              middle_name
              last_name
            }
             patient {
              id
              first_name
              middle_name
              last_name
            }
            rejected {
              id
            }
            exam {
              id
            }
            physicalanalysis {
              id
            }
            extraction {
              id
            }
      }
      }
      }`
  },
  immunohematologySelect(listQuery) {
    let query = generics.buildParams(listQuery)
    query += (query !== '' ? ',' : '') + 'immunohematology__isnull: true, rejected__isnull: true'

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `      id
             register_at
             donor {
               id
               first_name
               middle_name
               last_name
               code
             }
      }
      }
      }`
  },
  immunoserologySelect(listQuery) {
    let query = generics.buildParams(listQuery)
    query += (query !== '' ? ',' : '') + 'immunoserology__isnull: true, rejected__isnull: true'

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `      id
             register_at
             donor {
               id
               first_name
               middle_name
               last_name
               code
             }
      }
      }
      }`
  },
  preSieveDonationSelect(listQuery) {
    let query = generics.buildParams(listQuery)
    query += (query !== '' ? ',' : '') + 'exam__isnull: true'

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `      id
             donor {
               id
               first_name
               middle_name
               last_name
               code
             }
             place {
               name
               settingphysical {
                  hematocrit_min
                  hematocrit_max
                  hematocrit_min_m
                  hematocrit_max_m
                  systolic_min
                  systolic_max
                  diastolic_min
                  diastolic_max
                  pulse_min
                  pulse_max
                  weight_min
                  hemoglobin_factor
               }
             }
      }
      }
      }`
  },
  physicalAnalysisDonationSelect(listQuery) {
    let query = generics.buildParams(listQuery)
    query += (query !== '' ? ',' : '') + 'physicalanalysis__isnull: true, rejected__isnull: true'

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `      id
             donor {
               id
               first_name
               middle_name
               last_name
               code
             }
             place {
               name
               settingphysical {
                  hematocrit_min
                  hematocrit_max
                  hematocrit_min_m
                  hematocrit_max_m
                  systolic_min
                  systolic_max
                  diastolic_min
                  diastolic_max
                  pulse_min
                  pulse_max
                  weight_min
                  hemoglobin_factor
               }
             }
      }
      }
      }`
  },
  clinicalHistoryDonationSelect(listQuery) {
    let query = generics.buildParams(listQuery)
    query += (query !== '' ? ',' : '') + 'clinicalhistoryanswer__isnull: true, rejected__isnull: true'

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `      id
             register_at
             donor {
               id
               first_name
               middle_name
               last_name
               code
             }
      }
      }
      }`
  },
  extractionDonationSelect(listQuery) {
    let query = generics.buildParams(listQuery)
    query += (query !== '' ? ',' : '') + 'physicalanalysis__isnull: false, clinicalhistoryanswer__isnull: false, rejected__isnull: true, extraction__isnull: true'

    return `{` +
      MODEL + `(` + query + `) {` +
      `totalCount ` +
      `results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `) {` +
      `      id
             register_at
             type_process
             type_donation
             donor {
               id
               first_name
               middle_name
               last_name
               code
             }
      }
      }
      }`
  },
  listDonations(listQuery) {
    let query = generics.buildParams(listQuery)

    if (listQuery['extra']['patient_id'] !== '') {
      query += (query !== '' ? ',' : '') + 'patient__id: ' + listQuery['extra']['patient_id']
    }

    return `
    {
  donations(` + query + `) {
    totalCount
    results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `){
        id
        type_process
        type_donation
        register_at
        last_donation_at
        donor {
          id
          code
          first_name
          middle_name
          last_name
        }
        event {
          id
          name
        }
        place {
          id
          name
        }
         employee {
          id
          first_name
          middle_name
          last_name
        }
         patient {
          id
          first_name
          middle_name
          last_name
        }
        rejected {
          id
          reason {
            id
            type
          }
        }
        exam {
          id
        }
        physicalanalysis {
          id
        }
        immunoserology {
            id
            hiv
            hbsag
            hvc
            cheia
            chagas_hai
            rpr
        }
        extraction {
          id
        }
    }
  }
}
    `
  },
  list_dashboard(listQuery) {
    let query = generics.buildParams(listQuery)

    query += (query !== '' ? ',' : '') + 'rejected__isnull: true'
    query += (query !== '' ? ',' : '') + 'extraction__adversereaction__isnull: true'

    return `
    {
  donations(` + query + `) {
    totalCount
    results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `){
       id
        type_process
        type_donation
        register_at
        last_donation_at
        donor {
          id
          code
          first_name
          middle_name
          last_name
        }
        event {
          id
          name
        }
        place {
          id
          name
        }
         employee {
          id
          first_name
          middle_name
          last_name
        }
         patient {
          id
          first_name
          middle_name
          last_name
        }
        rejected {
          id
        }
        exam {
          id
        }
        physicalanalysis {
          id
        }
        extraction {
          id
          fragmentation{
            id
          }
        }
        immunoserology {
          id
        }
        immunohematology {
          id
        }
    }
  }
}
    `
  },
  report(listQuery) {
    let query = generics.buildParams(listQuery)

    let queryParams = ''

    for (const key in listQuery) {
      switch (key) {
        case 'extra':
          if (listQuery[key]['gender'] !== '') {
            queryParams += 'donor__gender: "' + listQuery[key]['gender'] + '", '
          }
          if (listQuery[key]['event'] !== '') {
            queryParams += 'event__isnull: ' + (listQuery[key]['event'] !== '1') + ', '
          }
          if (listQuery[key]['extraction'] !== '') {
            queryParams += 'extraction__isnull: ' + (listQuery[key]['extraction'] !== '1') + ', '
          }
          if (listQuery[key]['selfexclusion'] !== '' && listQuery[key]['extraction'] === '1') {
            queryParams += 'extraction__selfexclusion__isnull: ' + (listQuery[key]['selfexclusion'] !== '1') + ', '
          }
          if (listQuery[key]['adversereaction'] !== '' && listQuery[key]['extraction'] === '1') {
            queryParams += 'extraction__adversereaction__isnull: ' + (listQuery[key]['adversereaction'] !== '1') + ', '
          }
          if (listQuery[key]['rejected'] !== '') {
            switch (listQuery[key]['rejected']) {
              case '0':
                queryParams += 'rejected__isnull: true, '
                break
              case '1':
                queryParams += 'rejected__isnull: false, '
                break
              case '2': // temporal
                queryParams += 'rejected__reason__type: "TE", '
                break
              case '3': // permanente
                queryParams += 'rejected__reason__type: "PE", '
                break
            }
          }
          // console.log(listQuery[key]['rejected'])
          if (listQuery[key]['reasonRejected'] !== '' && listQuery[key]['rejected'] === '1') {
            queryParams += 'rejected__reason_id: "' + (listQuery[key]['reasonRejected']) + '", '
          }
          if (listQuery[key]['typeDonation'] !== '') {
            queryParams += 'type_donation: "' + (listQuery[key]['typeDonation']) + '", '
          }
          if (listQuery[key]['typeProcess'] !== '') {
            queryParams += 'type_process: "' + (listQuery[key]['typeProcess']) + '", '
          }
          if (listQuery[key]['etary'] !== '') {
            var etaryOption = listQuery[key]['etary'].split('-')
            queryParams += 'donor__age__gte: ' + etaryOption[0] + ', donor__age__lte: ' + etaryOption[1] + ', '
          }
          break
      }
    }

    if (query !== '') {
      query += ', ' + queryParams
    } else {
      query = queryParams
    }

    return `
    {
  donations(` + query + `) {
    totalCount
    results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `){
       id
        type_process
        type_donation
        register_at
        last_donation_at
        donor {
          id
          code
          first_name
          middle_name
          last_name
          gender
          age
        }
        event {
          id
          name
        }
        place {
          id
          name
        }
         employee {
          id
          first_name
          middle_name
          last_name
        }
         patient {
          id
          first_name
          middle_name
          last_name
        }
        rejected {
          id
        }
        exam {
          id
        }
        physicalanalysis {
          id
        }
        extraction {
          id
          selfexclusion{
            id
          }
      }
    }
  }
}
    `
  },
  reportDailyDonation(listQuery) {
    let query = generics.buildParams(listQuery)

    let queryParams = ''

    for (const key in listQuery) {
      switch (key) {
        case 'extra':
          if (listQuery[key]['event'] !== '') {
            queryParams += 'event__isnull: ' + (listQuery[key]['event'] !== '1') + ', '
          }
          break
      }
    }

    if (query !== '') {
      query += ', ' + queryParams
    } else {
      query = queryParams
    }

    return `
    {
  donations(` + query + `) {
    totalCount
    results(limit: ` + listQuery.limit + `, offset: ` + listQuery.offset + `){
       id
        type_process
        type_donation
        register_at
        last_donation_at
        donor {
          id
          code
          first_name
          middle_name
          last_name
          gender
          age
        }
        event {
          id
          name
        }
        place {
          id
          name
        }
         employee {
          id
          first_name
          middle_name
          last_name
        }
         patient {
          id
          first_name
          middle_name
          last_name
        }
        clinicalhistoryanswer {
          id
        }
        rejected {
          id,
          resource
        }
        exam {
          id
          blood_group
          chagas
          rpr
          hematocrit
        }
        physicalanalysis {
          id
        }
        extraction {
          id
        }
    }
  }
}
    `
  },
  getDonationEdit(id) {
    return `
      {
        donation(id: ${id}){
          id
          type_process
          type_donation
          register_at
          last_donation_at
          donor {
            id
            code
            image
            civil_status
            first_name
            middle_name
            last_name
            birth_date
            age
            gender
            country
            can_donate
            is_volunteer
            residence
            zone
            province
            department
            phone
            mobile_phone
            family_phone
            profession
            degree_instruction
            job
            job_address
            email
          }
          event {
            id
            name
          }
          place {
            id
            name
            settingphysical {
              hematocrit_min
              hematocrit_max
              hematocrit_min_m
              hematocrit_max_m
              systolic_min
              systolic_max
              diastolic_min
              diastolic_max
              pulse_min
              pulse_max
              weight_min
              hemoglobin_factor
            }
          }
          employee {
            id
            first_name
            middle_name
            last_name
          }
          patient {
            id
            first_name
            middle_name
            last_name
          }
          rejected {
            id
            donation {
              id
            }
            resource
            observations
            resource_id
            resource
            register_at
            reason {
              id
              type
              name
            }
            employee {
              id
            }
          }
          exam {
            id
            donation {
              id
            }
            hematocrit
            hemoglobin
            blood_group
            chagas
            rpr
            register_at
            observations
            history
            employee {
              id
            }
          }
          physicalanalysis {
            id
            donation {
              id
            }
            systolic
            diastolic
            pulse
            tall
            weight
            temperature
            observations
            register_at
            employee {
              id
            }
          }
          immunoserology {
            id
          }
          immunohematology {
            id
          }
          extraction {
            id
            register_at
            employee {
              id
            }
            fragmentation {
              id
            }
          }
        }
      }
    `
  },
  createDonation() {
    return this.buildDonation('create')
  },
  updateDonation() {
    return this.buildDonation('update')
  },
  buildDonation(action) {
    let paramsGraphqlArgument = '$donor_id: Int!, $employee_id: Int!, $event_id: Int, $last_donation_at: Date, $patient_id: Int, $place_id: Int!, $register_at: Date!, $register_id: Int!, $type_donation: String!, $type_process: String!'
    if (action === 'update') {
      paramsGraphqlArgument = '$donor_id: Int, $employee_id: Int, $event_id: Int, $id: Int!, $last_donation_at: Date, $patient_id: Int, $place_id: Int, $register_at: Date, $register_id: Int, $type_donation: String, $type_process: String'
    }
    const paramsResolve = generics.buildGraphqlParams(paramsGraphqlArgument)

    return `
    mutation ${action}Donation(${paramsGraphqlArgument} ) {
      ${action}_${SINGLE_MODEL}(${paramsResolve}) {
        ${SINGLE_MODEL} {
          id
        }
      }
    }
    `
  }
}
export default donations

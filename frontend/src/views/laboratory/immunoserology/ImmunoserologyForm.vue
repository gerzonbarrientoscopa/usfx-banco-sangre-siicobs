<template>
  <div class="app-container">
    <el-form
      ref="dataForm"
      :model="temp"
      :rules="rules"
      label-position="left"
      label-width="150px"
      style="width: 100%;"
    >

      <div class="grid-content">
        <el-row :gutter="20">
          <el-col :md="24" :sm="24">
            <el-form-item :label="$t('models.immunoserology.donation')" prop="donation_id">
              <el-select
                v-if="dialogStatus === 'create' && !rowExtraction"
                v-model="temp.donation_id"
                :loading="loading"
                :placeholder="$t('please_select')"
                :remote-method="remoteMethod"
                automatic-dropdown
                class="filter-item"
                clearable
                filterable
                remote
                @change="getDonation()"
              >
                <el-option
                  v-for="item in donations"
                  :key="item.id"
                  :label="item.donor.code"
                  :value="item.id"
                >
                  <span style="float: left"><strong>{{ item.donor.code }}</strong></span>
                  <span style="float: right; color: #8492a6; font-size: 13px">{{ item.register_at| toHumanDateMonthLetter }}</span>
                </el-option>
              </el-select>
              <strong v-if="dialogStatus === 'update'" class="text-text-green-sea">
                {{ temp.donation.donor.code }}
              </strong>
              <strong v-if="dialogStatus === 'create' && rowExtraction" class="text-text-green-sea">
                {{ rowExtraction.donation.donor.code }}
              </strong>
              <br>
              <div>
                Resultados Pre-Tamizaje:
                <span v-if="donation && donation.exam.chagas">CHAGAS: {{ donation.exam.rpr | typeReactFilter }}</span>,
                <span v-if="donation && donation.exam.rpr">RPR: {{ donation.exam.chagas | typeReactFilter }}</span>
              </div>
            </el-form-item>
            <el-form-item :label="$t('models.donation.register_at')" prop="register_at">
              <el-date-picker
                v-model="temp.register_at"
                :placeholder="$t('models.donation.register_at')"
                format="dd-MM-yyyy"
                type="date"
                value-format="yyyy-MM-dd"
              />
            </el-form-item>
          </el-col>
          <el-col :md="24" :sm="24">
            <el-button size="mini" type="default" @click="setImmunoserology()">PONER TODO EN NO REACTIVO</el-button>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item :label="$t('models.immunoserology.chagas_hai')" prop="chagas_hai">
              <el-radio-group v-model="temp.chagas_hai" class="el-row--flex" size="small">
                <el-radio-button v-for="item in typeReactOptions" :key="item.key" :label="item.key">
                  {{ item.display_name }}
                </el-radio-button>
              </el-radio-group>
            </el-form-item>
            <el-form-item :label="$t('models.immunoserology.cheia')" prop="cheia">
              <el-radio-group v-model="temp.cheia" class="el-row--flex" size="small">
                <el-radio-button v-for="item in typeReactOptions" :key="item.key" :label="item.key">
                  {{ item.display_name }}
                </el-radio-button>
              </el-radio-group>
            </el-form-item>
            <el-form-item :label="$t('models.immunoserology.rpr')" prop="rpr">
              <el-radio-group v-model="temp.rpr" class="el-row--flex" size="small">
                <el-radio-button v-for="item in typeReactOptions" :key="item.key" :label="item.key">
                  {{ item.display_name }}
                </el-radio-button>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item :label="$t('models.immunoserology.hvc')" prop="hvc">
              <el-radio-group v-model="temp.hvc" class="el-row--flex" size="small">
                <el-radio-button v-for="item in typeReactOptions" :key="item.key" :label="item.key">
                  {{ item.display_name }}
                </el-radio-button>
              </el-radio-group>
            </el-form-item>
            <el-form-item :label="$t('models.immunoserology.hbsag')" prop="hbsag">
              <el-radio-group v-model="temp.hbsag" class="el-row--flex" size="small">
                <el-radio-button v-for="item in typeReactOptions" :key="item.key" :label="item.key">
                  {{ item.display_name }}
                </el-radio-button>
              </el-radio-group>
            </el-form-item>
            <el-form-item :label="$t('models.immunoserology.hiv')" prop="hiv">
              <el-radio-group v-model="temp.hiv" class="el-row--flex" size="small">
                <el-radio-button v-for="item in typeReactOptions" :key="item.key" :label="item.key">
                  {{ item.display_name }}
                </el-radio-button>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item :label="$t('models.fragmentation.observations')" prop="observations">
          <el-input v-model="temp.observations" :rows="3" type="textarea"
                    @input.native="setUpperCase(temp, 'observations', $event)"/>
        </el-form-item>
        <el-form-item :label="$t('models.exam.employee')" prop="employee_id">
          <el-select
            v-model="temp.employee_id"
            :placeholder="$t('please_select')"
            automatic-dropdown
            class="filter-item"
            filterable
          >
            <el-option
              v-for="item in employees"
              :key="item.id"
              :label="item.first_name +' '+ item.middle_name +' '+ item.last_name "
              :value="item.id"
            />
          </el-select>
        </el-form-item>
      </div>
    </el-form>
    <br>
    <el-button @click="dialogStatus==='create'?createData():updateData()">{{ $t('confirm') }}</el-button>

  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { graphqlRequest } from '@/api/graphql'
import donations from '@/query/donation'
import moment from 'moment'
import immunoserologies from '@/query/immunoserology'

const typeReactOptions = [
  { key: 'R', display_name: 'REACTIVO' },
  { key: 'NR', display_name: 'NO REACTIVO' },
  { key: 'IN', display_name: 'INDETERMINADO' }
]

const typeReactKeyValue = typeReactOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'ImmunoserologyForm',
  components: {},
  directives: {},
  filters: {
    typeReactFilter(type) {
      return typeReactKeyValue[type]
    }
  },
  props: {
    row: {
      type: Object,
      default: null
    },
    rowExtraction: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      tableKey: 0,
      donations: null,
      listH: null,
      loading: false,
      typeReactOptions,
      donation: null,
      listDonationQuery: { page: 1, limit: 20, search: '', offset: 0, ordering: '-id', from: 'SER' },
      listQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-created_at', immunoserology__id: '' },
      temp: {
        id: undefined,
        donation_id: '',
        hiv: null,
        hbsag: null,
        hvc: null,
        cheia: null,
        chagas_hai: null,
        rpr: null,
        observations: '',
        register_at: moment().format('YYYY-MM-DD')
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Editando Serología',
        create: 'Creando Serología'
      },
      rules: {
        donation_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        hiv: [{ required: false, message: this.$t('is_required'), trigger: 'change' }],
        hbsag: [{ required: false, message: this.$t('is_required'), trigger: 'change' }],
        hvc: [{ required: false, message: this.$t('is_required'), trigger: 'change' }],
        cheia: [{ required: false, message: this.$t('is_required'), trigger: 'change' }],
        chagas_hai: [{ required: false, message: this.$t('is_required'), trigger: 'change' }],
        rpr: [{ required: false, message: this.$t('is_required'), trigger: 'change' }],
        observations: [{ trigger: 'blur' }],
        register_at: [{ required: true, message: this.$t('is_required') }],
        employee_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }]
      },
      downloadLoading: false
    }
  },
  computed: {
    ...mapGetters([
      'employees',
      'employee_id'
    ])
  },
  watch: {
    row: function() {
      this.determineAction()
    },
    rowExtraction: function() {
      this.determineAction()
    }
  },
  mounted() {
    this.determineAction()
  },
  methods: {
    determineAction() {
      if (this.row) {
        this.handleUpdate(this.row)
      } else {
        this.handleCreate()
      }
    },
    getListDonation() {
      this.loading = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'donations',
          query: donations.immunoserologySelect(this.listDonationQuery)
        }
      ).then(response => {
        const data = response.data
        this.donations = data.donations.results
        this.total = data.donations.totalCount
        this.loading = false
      })
    },
    remoteMethod(query) {
      if (query !== '') {
        this.listDonationQuery.search = query
      } else {
        this.listDonationQuery.search = ''
      }
      this.getListDonation()
    },
    setImmunoserology() {
      const tempData = Object.assign({}, this.temp)
      tempData.hiv = 'NR'
      tempData.hbsag = 'NR'
      tempData.hvc = 'NR'
      tempData.cheia = 'NR'
      tempData.chagas_hai = 'NR'
      tempData.rpr = 'NR'
      this.temp = tempData
    },
    resetTemp() {
      this.listH = null
      this.temp = {
        id: undefined,
        donation_id: '',
        hiv: null,
        hbsag: null,
        hvc: null,
        cheia: null,
        chagas_hai: null,
        rpr: null,
        observations: '',
        register_at: moment().format('YYYY-MM-DD')
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      if (this.rowExtraction) {
        this.temp.donation_id = this.rowExtraction.donation.id
        this.getDonation()
      } else {
        this.getListDonation()
      }
      const tempData = Object.assign({}, this.temp)
      tempData.employee_id = this.employee_id
      this.temp = tempData
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      const tempData = Object.assign({}, this.temp)

      if (!this.isSelectedAllNoReactive(tempData) && !this.isSelectedReactive(tempData)) {
        this.$notify({
          title: 'Falta Resultado',
          message: 'Debe seleccionar al menos un resultado "Reactivo" o seleccione todo en "No Reactivo"',
          type: 'success',
          duration: 2000
        })
        return
      }

      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'createImmunoserology',
              query: immunoserologies.createImmunoserology(),
              variables: tempData
            }
          ).then(response => {
            if (response.errors) {
              this.$notify({
                title: 'Estado',
                message: response.errors[0].message,
                type: 'error',
                duration: 2000
              })
            } else {
              this.$emit('dialogStatus', false)
              this.resetTemp()
              this.$notify({
                title: 'Estado',
                message: 'Registro creado',
                type: 'success',
                duration: 2000
              })
            }
          })
        }
      })
    },
    getDonation() {
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'donation',
          query: donations.getDonationEdit(this.temp.donation_id)
        }
      ).then(response => {
        const data = response.data
        this.donation = data.donation
      })
    },
    handleUpdate(row) {
      this.dialogStatus = 'update'
      const tempData = Object.assign({}, row) // copy obj
      tempData.donation_id = tempData.donation.id
      tempData.employee_id = tempData.employee.id
      this.temp = tempData
      this.getDonation()
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'updateImmunoserology',
              query: immunoserologies.updateImmunoserology(),
              variables: tempData
            }
          ).then(response => {
            if (response.errors) {
              this.$notify({
                title: 'Estado',
                message: response.errors[0].message,
                type: 'error',
                duration: 2000
              })
            } else {
              this.$emit('dialogStatus', false)
              this.$notify({
                title: 'Estado',
                message: 'Se ha actualizado',
                type: 'success',
                duration: 2000
              })
            }
          })
        }
      })
    },
    isSelectedReactive(data) {
      return (data.hiv === 'R' || data.hbsag === 'R' || data.hvc === 'R' || data.cheia === 'R' || data.chagas_hai === 'R' || data.rpr === 'R' || data.hiv === 'IN' || data.hbsag === 'IN' || data.hvc === 'IN' || data.cheia === 'IN' || data.chagas_hai === 'IN' || data.rpr === 'IN')
    },
    isSelectedAllNoReactive(data) {
      return (data.hiv === 'NR' && data.hbsag === 'NR' && data.hvc === 'NR' && data.cheia === 'NR' && data.chagas_hai === 'NR' && data.rpr === 'NR')
    }
  }
}
</script>

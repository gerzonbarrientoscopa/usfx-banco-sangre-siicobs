<template>
  <div class="app-container">
    <el-row :gutter="20">
      <el-col :md="6">
        <el-card :body-style="{ padding: '0px' }">
          <img src="@/assets/global_images/user.png" class="image" alt="user-image">
        </el-card>
        <h3 v-if="dialogStatus==='update'" class="text-text-turquoise-600"><strong>{{ temp.donor | fullName }} <small>{{ temp.donor.is_volunteer ? 'Voluntario' : '' }}</small></strong></h3>
      </el-col>
      <el-col :md="18">
        <div class="grid-content">
          <el-form
            ref="dataForm"
            :rules="rules"
            :model="temp"
            style="width: 100%;"
          >
            <el-form-item :label="$t('models.donation.register_at')" prop="register_at">
              <el-date-picker
                v-model="temp.register_at"
                :placeholder="$t('models.donation.register_at')"
                :picker-options="pickerOptions"
                type="date"
                format="dd-MM-yyyy"
                value-format="yyyy-MM-dd"
              />
            </el-form-item>
            <el-form-item :label="$t('models.donation.donor')" prop="donor_id">
              <el-select
                v-model="temp.donor_id"
                :placeholder="$t('please_select')"
                :remote-method="remoteMethod"
                :loading="loading"
                filterable
                remote
                automatic-dropdown
                class="filter-item"
                @change="canDonate(temp.donor_id)"
              >
                <el-option
                  v-for="item in donors"
                  :key="item.id"
                  :label="item | donorCodeFullName"
                  :value="item.id"
                >
                  <span style="float: left"><strong>{{ item.code }}</strong> {{ item | fullName }}</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">{{ item.is_volunteer ? 'Voluntario' : '' }}</span>
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item :label="$t('models.donation.place') + ' (Será usado para las formulas de Analisis Físico)'" prop="place_id">
              <el-radio-group v-model="temp.place_id">
                <el-radio-button v-for="item in places" :key="item.id" :label="item.id">
                  {{ item.name }}
                </el-radio-button>
              </el-radio-group>
            </el-form-item>
            <el-form-item :label="$t('models.donation.type_donation')" prop="type_donation">
              <el-radio-group v-model="temp.type_donation">
                <el-radio-button v-for="item in typeDonationOptions" :key="item.key" :label="item.key">
                  {{ item.display_name }}
                </el-radio-button>
              </el-radio-group>
            </el-form-item>

            <el-form-item :label="$t('models.extraction.receptor_fullname') + ' (Para quién está donando)'" prop="patient_id">
              <el-select
                v-model="temp.patient_id"
                :placeholder="$t('please_select')"
                :loading="patientLoading"
                :remote-method="remoteMethodPatient"
                remote
                filterable
                automatic-dropdown
                clearable
                class="filter-item"
              >
                <el-option
                  v-for="item in patients"
                  :key="item.id"
                  :label="item | fullName "
                  :value="item.id"
                />
              </el-select>
            </el-form-item>

            <el-form-item :label="$t('models.donation.last_donation_at')" prop="last_donation_at">
              <el-date-picker
                v-model="temp.last_donation_at"
                :placeholder="$t('models.donation.last_donation_at')"
                :picker-options="lastDonationOptions"
                type="date"
                format="dd-MM-yyyy"
                value-format="yyyy-MM-dd"
              />
              <el-alert
                v-if="dialogStatus === 'create' && donationEligibility"
                :title="donationEligibility.message"
                :type="donationEligibility.type"
                :closable="false"
                show-icon
                effect="dark"
                class="donation-eligibility-alert"
              />
            </el-form-item>
            <el-form-item :label="$t('models.donation.event') + ' (seleccionar si es de colectas)'" prop="event_id">
              <el-select
                v-model="temp.event_id"
                :placeholder="$t('please_select')"
                :remote-method="remoteMethodEvent"
                :loading="eventLoading"
                filterable
                remote
                automatic-dropdown
                class="filter-item"
              >
                <el-option v-for="item in events" :key="item.id" :label="item.name" :value="item.id" />
              </el-select>
            </el-form-item>
            <el-form-item :label="$t('models.clinical-history.employee')" prop="employee_id">
              <el-select
                v-model="temp.employee_id"
                :placeholder="$t('please_select')"
                filterable
                automatic-dropdown
                class="filter-item"
              >
                <el-option
                  v-for="item in employees"
                  :key="item.id"
                  :label="item.first_name +' '+ item.middle_name +' '+ item.last_name "
                  :value="item.id"
                />
              </el-select>
            </el-form-item>
          </el-form>
        </div>
      </el-col>
      <el-col v-if="!donor.can_donate" :sm="24" :md="10">
        <div class="grid-content">
          <el-alert
            :closable="false"
            title="El Donante seleccionado en la anterior donacion fue RECHAZADO DE FORMA PERMANENTE"
            type="error"
          />
        </div>
      </el-col>
    </el-row>
    <div slot="footer" class="dialog-footer" style="text-align: right">
      <el-button :disabled="!(donor.can_donate)" @click="dialogStatus==='create'?createData():updateData()">{{ $t('confirm') }}
      </el-button>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import moment from 'moment'
import Cookies from 'js-cookie'
import { graphqlRequest } from '@/api/graphql'
import patients from '@/query/patient'
import events from '@/query/event'
import donors from '@/query/donor'
import donations from '@/query/donation'
import places from '@/query/place'
import { TYPE_PROCESS } from '@/utils/const'
import { getDonationEligibility, getLastDonationDate } from '@/utils/donationEligibility'

const typeDonationOptions = [
  { key: 'VA', display_name: 'VOLUNTARIA ALTRUISTA' },
  { key: 'RS', display_name: 'REPOSICION SOLIDARIA' },
  { key: 'RE', display_name: 'REPOSICION EXIGIDA' },
  { key: 'DA', display_name: 'DONACION AUTOLOGA' }
]

export default {
  name: 'DonationForm',
  data() {
    return {
      pickerOptions: {
        disabledDate(time) {
          return time.getTime() > Date.now()
        }
      },
      tableKey: 0,
      donor: {
        can_donate: true
      },
      donors: null,
      patients: null,
      places: null,
      exams: null,
      physicalAnalisiss: null,
      events: null,
      list: null,
      total: null,
      loading: false,
      patientLoading: false,
      placeLoading: false,
      eventLoading: false,
      loadingSelectEvents: false,
      listLoading: true,
      listQuery: { page: 1, limit: 20, search: undefined, ordering: '-id', only_event: false },
      listDonorQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-id', id: undefined },
      listEventQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-init_at', is_active: true, id: undefined },
      listPatientQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: 'first_name', id: undefined },
      listPlaceQuery: { page: 1, limit: 50, offset: 0, search: '', ordering: 'name', id: undefined },
      typeDonationOptions,
      donationEligibility: null,
      selectedDonorLastDonationAt: null,
      temp: {
        id: undefined,
        donor_id: undefined,
        place_id: undefined,
        event_id: undefined,
        employee_id: undefined,
        last_donation_at: null,
        register_at: '',
        type_donation: 'RE',
        type_process: TYPE_PROCESS.NORMAL
      },
      exam: {
        register_at: undefined,
        blood_group: ''
      },
      donation: {
        id: undefined,
        donor: {
          code: undefined,
          first_name: '',
          last_name: '',
          age: undefined,
          birth_date: undefined,
          ci: undefined,
          civil_status: '',
          residence: ''
        },
        status: '',
        register_at: '',
        employee_id: undefined
      },
      dialogShowVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Editando Donación',
        create: 'Creando Donación'
      },
      rules: {
        donor_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        place_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        type_donation: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        register_at: [{ required: true, message: this.$t('is_required') }],
        last_donation_at: [{ required: false, message: this.$t('is_required'), trigger: 'change' }],
        patient_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        employee_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        event_id: []
      },
      downloadLoading: false,
      isAreaPromotion: false,
      lastDonationOptions: {
        disabledDate(time) {
          return time.getTime() > Date.now()
        },
        shortcuts: [{
          text: 'Hace 4 meses',
          onClick(picker) {
            const date = new Date()
            date.setTime(date.getTime() - 3600 * 1000 * 24 * (30 * 4))
            picker.$emit('pick', date)
          }
        }, {
          text: 'Hace 5 meses',
          onClick(picker) {
            const date = new Date()
            date.setTime(date.getTime() - 3600 * 1000 * 24 * (30 * 5))
            picker.$emit('pick', date)
          }
        }, {
          text: 'Hace 6 meses',
          onClick(picker) {
            const date = new Date()
            date.setTime(date.getTime() - 3600 * 1000 * 24 * (30 * 6))
            picker.$emit('pick', date)
          }
        }, {
          text: 'Hace 7 meses',
          onClick(picker) {
            const date = new Date()
            date.setTime(date.getTime() - 3600 * 1000 * 24 * (30 * 7))
            picker.$emit('pick', date)
          }
        }, {
          text: 'Hace 8 meses',
          onClick(picker) {
            const date = new Date()
            date.setTime(date.getTime() - 3600 * 1000 * 24 * (30 * 8))
            picker.$emit('pick', date)
          }
        }, {
          text: 'Hace 9 meses',
          onClick(picker) {
            const date = new Date()
            date.setTime(date.getTime() - 3600 * 1000 * 24 * (30 * 9))
            picker.$emit('pick', date)
          }
        }, {
          text: 'Hace 1 año',
          onClick(picker) {
            const date = new Date()
            date.setTime(date.getTime() - 3600 * 1000 * 24 * (30 * 12))
            picker.$emit('pick', date)
          }
        }, {
          text: 'Hace 2 años',
          onClick(picker) {
            const date = new Date()
            date.setTime(date.getTime() - 3600 * 1000 * 24 * (30 * (12 * 2)))
            picker.$emit('pick', date)
          }
        }, {
          text: 'Hace 3 años',
          onClick(picker) {
            const date = new Date()
            date.setTime(date.getTime() - 3600 * 1000 * 24 * (30 * (12 * 3)))
            picker.$emit('pick', date)
          }
        }]
      }
    }
  },
  computed: {
    ...mapGetters([
      'employees',
      'employee_id'
    ])
  },
  watch: {
    'temp.type_donation': function(value) {
      this.setRules(value)
    },
    'temp.last_donation_at': function(value) {
      this.updateDonationEligibility()
    },
    'temp.register_at': function() {
      this.updateDonationEligibility()
    }
  },
  created() {
    if (this.$route.name === 'promotions-donation') {
      this.isAreaPromotion = true
      this.listQuery.only_event = true
      this.rules.event_id = [{ required: true, message: this.$t('is_required'), trigger: 'change' }]
    }
    this.handleCreate()
  },
  methods: {
    setRules(value) {
      console.log(value)
      if (value === 'VA') {
        this.rules.patient_id = [{ required: false, message: this.$t('is_required'), trigger: 'change' }]
        // this.rules.event_id = [{ required: true, message: this.$t('is_required'), trigger: 'change' }]
      } else {
        this.rules.event_id = []
        this.rules.patient_id = [{ required: true, message: this.$t('is_required'), trigger: 'change' }]
      }
    },
    getStatus(row) {
      var type = 'info'
      if (row.exam) {
        type = ''
      }
      if (row.rejected) {
        type = 'danger'
      }
      return type
    },
    getListPatients() {
      this.patientLoading = true
      if (Cookies.get('donationReceptor') !== 'undefined' && Cookies.get('donationReceptor') !== undefined) {
        const receptor = JSON.parse(Cookies.get('donationReceptor'))
        const tempData = Object.assign({}, this.temp)
        tempData.patient_id = receptor.id
        this.temp = tempData
      }
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'patients',
          query: patients.donation_select(this.listPatientQuery)
        }
      ).then(response => {
        const data = response.data
        this.patients = data.patients.results
        this.patientLoading = false
      })
    },
    remoteMethodPatient(query) {
      if (query !== '') {
        this.listPatientQuery.search = query
      } else {
        this.listPatientQuery.search = ''
      }
      this.getListPatients()
    },
    getListDonors() {
      this.loading = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'donors',
          query: donors.list(this.listDonorQuery)
        }
      ).then(response => {
        const data = response.data
        this.donors = data.donors.results
        this.loading = false

        if (Cookies.get('donationDonor') !== 'undefined' && Cookies.get('donationDonor') !== undefined) {
          const storedDonor = JSON.parse(Cookies.get('donationDonor'))
          const donor = this.donors.find(item => String(item.id) === String(storedDonor.id))
          if (donor && getLastDonationDate(donor)) {
            this.selectDonor(donor)
          } else {
            this.loadStoredDonor(storedDonor.id)
          }
        }
      })
    },
    canDonate(id) {
      const donor = (this.donors || []).find(item => String(item.id) === String(id))
      if (donor && getLastDonationDate(donor)) {
        this.selectDonor(donor)
      } else if (donor) {
        this.loadStoredDonor(donor.id)
      } else {
        this.selectDonor(null)
      }
    },
    loadStoredDonor(id) {
      const listDonor = (this.donors || []).find(item => String(item.id) === String(id))
      if (listDonor) {
        this.donor = listDonor
      }
      this.selectedDonorLastDonationAt = null
      this.temp = Object.assign({}, this.temp, { donor_id: id, last_donation_at: null })
      this.donationEligibility = null
      this.loading = true
      graphqlRequest({
        from: this.$route.name,
        service: 'donors',
        query: donors.showDonor(id)
      }).then(response => {
        if (response.errors && response.errors.length) {
          throw new Error('No se pudo cargar el historial de donaciones.')
        }
        const donor = response.data && response.data.donor
        if (!donor) {
          throw new Error('No se pudo cargar el historial de donaciones.')
        }
        if (String(this.temp.donor_id) !== String(id)) {
          return
        }
        const index = this.donors.findIndex(item => String(item.id) === String(donor.id))
        if (index === -1) {
          this.donors.unshift(donor)
        } else {
          this.$set(this.donors, index, donor)
        }
        this.selectDonor(donor)
      }).catch(() => {
        if (String(this.temp.donor_id) === String(id)) {
          this.donationEligibility = null
          this.$notify({
            title: 'Estado',
            message: 'No se pudo cargar el historial de donaciones del donante.',
            type: 'error'
          })
        }
      }).finally(() => {
        this.loading = false
      })
    },
    selectDonor(donor) {
      if (!donor) {
        this.donor = { can_donate: true }
        this.selectedDonorLastDonationAt = null
        this.temp = Object.assign({}, this.temp, { donor_id: undefined, last_donation_at: null })
        this.donationEligibility = null
        return
      }
      this.donor = donor
      this.selectedDonorLastDonationAt = getLastDonationDate(donor)
      this.temp = Object.assign({}, this.temp, {
        donor_id: donor.id,
        last_donation_at: this.selectedDonorLastDonationAt
      })
      this.updateDonationEligibility()
    },
    updateDonationEligibility() {
      if (!this.temp.donor_id || !this.donor || !this.donor.can_donate) {
        this.donationEligibility = null
        return
      }
      this.donationEligibility = getDonationEligibility(this.selectedDonorLastDonationAt, this.temp.register_at)
    },
    remoteMethod(query) {
      if (query !== '') {
        this.listDonorQuery.search = query
      } else {
        this.listDonorQuery.search = ''
      }
      this.getListDonors()
    },
    getListPlaces() {
      this.placeLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'places',
          query: places.donation_select(this.listPlaceQuery)
        }
      ).then(response => {
        const data = response.data
        this.places = data.places.results
        this.placeLoading = false
      })
    },
    getListEvents() {
      this.eventLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'events',
          query: events.donation_select(this.listEventQuery)
        }
      ).then(response => {
        const data = response.data
        this.events = data.events.results
        this.eventLoading = false
      })
    },
    remoteMethodEvent(query) {
      if (query !== '') {
        this.listEventQuery.search = query
      } else {
        this.listEventQuery.search = ''
      }
      this.getListEvents()
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        place_id: 1,
        donor_id: undefined,
        type_donation: 'RE',
        register_at: moment().format('YYYY-MM-DD'),
        last_donation_at: null,
        employee_id: this.employee_id
      }
      this.donor = {
        can_donate: true
      }
      this.selectedDonorLastDonationAt = null
      this.donationEligibility = null
    },
    handleCreate() {
      this.resetTemp()
      if (Cookies.get('donationDonor') !== 'undefined' && Cookies.get('donationDonor') !== undefined) {
        const donor = JSON.parse(Cookies.get('donationDonor'))
        this.listDonorQuery['id'] = donor.id
      }
      if (Cookies.get('donationReceptor') !== 'undefined' && Cookies.get('donationReceptor') !== undefined) {
        const receptor = JSON.parse(Cookies.get('donationReceptor'))
        this.listPatientQuery['id'] = receptor.id
      }
      this.dialogStatus = 'create'
      this.getListDonors()
      this.getListPatients()
      this.getListEvents()
      this.getListPlaces()
      this.listPatientQuery['id'] = undefined
      this.listDonorQuery['id'] = undefined
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          if (tempData.patient_id === '') tempData.patient_id = undefined
          if (tempData.event_id === '') tempData.event_id = undefined
          tempData.register_id = this.employee_id
          tempData.type_process = Cookies.get('type_process')
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'createDonation',
              query: donations.createDonation(),
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
              Cookies.set('type_process', TYPE_PROCESS.NORMAL)
              this.$router.replace({ path: '/registry/donations/' + response.data.create_donation.donation.id })
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
    handleUpdate(row) {
      this.listPatientQuery['id'] = row.patient.id
      this.getListPatients()
      this.listPatientQuery['id'] = undefined

      this.donationEligibility = null

      if (this.isAreaPromotion) {
        this.listEventQuery['id'] = row.event.id
        this.getListEvents()
        this.listEventQuery['id'] = undefined
      }

      this.temp = Object.assign({}, row)
      this.temp.donor_id = this.temp.donor.id
      this.temp.place_id = this.temp.place.id
      this.temp.employee_id = this.temp.employee.id

      if (this.temp.event) {
        this.temp.event_id = this.temp.event.id
        this.events = [this.temp.event]
      }

      if (this.temp.patient) {
        this.temp.patient_id = this.temp.patient.id
      }

      this.dialogStatus = 'update'
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      const tempData = Object.assign({}, this.temp)

      if (tempData == null) {
        this.temp.last_donation_at = null
      }

      this.temp = tempData

      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          if (tempData.patient_id === '') tempData.patient_id = undefined
          if (tempData.event_id === '') tempData.event_id = undefined
          tempData.register_id = this.employee_id
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'updateDonation',
              query: donations.updateDonation(),
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
              this.$notify({
                title: 'Estado',
                message: 'Registro actualizado',
                type: 'success',
                duration: 2000
              })
            }
          })
        }
      })
    },
    handleShowDetail(row) {
      this.temp = row
      this.dialogShowVisible = true
    },
    handleCloseDetail() {
      this.dialogShowVisible = false
      this.temp = null
    }
  }
}
</script>
<style type="text/scss" >
  .title {
    padding-top: 20px;
    font-size: 15px;
    vertical-align: middle;
    text-transform: uppercase;
    font-weight: bold;
  }
  .bold {
    font-weight: bold;
  }
  .step {
    height: 300px;
    margin-top: 20px;
  }
  .text {
    padding-top: 5px;
    font-size: 12px;
  }
  .code {
    float: left;
    font-size: 15px;
    margin-right: 20px;
  }
  .font-120 {
    font-size: 120px;
  }
  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
  .clearfix:after {
    clear: both
  }
  .mt-40 {
    margin-top: 40px;
  }
  .box-card {
    width: 100%;
    span {
      vertical-align: middle;
    }
    img {
      height:140px;
    }
  }
  .box-card {
    width: 100%;
    height: auto;
  }
  .donation-eligibility-alert {
    margin-top: 12px;
  }
  .donation-eligibility-alert .el-alert__title {
    font-size: 16px;
    font-weight: 700;
    line-height: 1.4;
  }
</style>

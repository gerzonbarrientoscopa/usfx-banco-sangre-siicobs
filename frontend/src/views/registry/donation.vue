<template>
  <div class="app-container">
    <div class="filter-container">
      <el-row :gutter="20">
        <el-col :md="12">
          <div class="block">
            <div class="demonstration">Fecha Inicial / Fecha Final</div>
            <el-date-picker
              v-model="listQuery.date_range"
              type="daterange"
              align="right"
              unlink-panels
              range-separator="A"
              start-placeholder="Fecha Inicial"
              end-placeholder="Fecha Final"
              format="dd-MM-yyyy"
              value-format="yyyy-MM-dd"
              :picker-options="pickerOptions2"
              @change="handleFilter"
            />
          </div>
        </el-col>
        <el-col :md="2">
          <span class="demonstration">Total</span>
          <br>
          <strong style="font-size: 2em">
            {{ total }}
          </strong>
        </el-col>
      </el-row>
    </div>
    <div class="filter-container">
      <el-input
        v-model.lazy="listQuery.search"
        :placeholder="$t('models.donation.search')"
        :autofocus="'autofocus'"
        prefix-icon="el-icon-search"
        clearable
        class="filter-item"
        @input="handleFilter"
      />
      <el-button
        v-if="checkPermission(['add_donation'])"
        class="filter-item"
        style="margin-left: 10px;"
        type="primary"

        @click="handleCreate()"
      >{{ $t('add') }}
      </el-button>
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      :default-sort="{prop: 'register_at', order: 'descending'}"
      border
      fit
      stripe
      highlight-current-row
      style="width: 100%;"
      @sort-change="handleOrderChange"
    >
      <el-table-column
        :label="$t('models.donation.register_at')"
        fixed
        width="190px"
        align="center"
        prop="register_at"
        sortable="custom"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.register_at | toHumanDate }}</span>
        </template>
      </el-table-column>
      <el-table-column
        :label="$t('models.donor.code')"
        width="120px"
        align="center"
        prop="donor__code"
        sortable="custom"
      >
        <template slot-scope="scope">
          <el-tooltip
            v-if="textReactiveFilter(scope.row) !== ''"
            class="item"
            effect="dark"
            :content="textReactiveFilter(scope.row)"
            placement="top-start"
          >
            <div :class="scope.row | colorReactiveFilter" class="circle" />
          </el-tooltip>
          <strong>{{ scope.row.donor.code }}</strong>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.donor.names')" width="220px" align="left">
        <template slot-scope="scope">
          <span>{{ scope.row.donor | fullName }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.donation.status')" width="155px" align="center">
        <template slot-scope="scope">
          <el-tag :type="getStatus(scope.row)">{{ scope.row | statusFilter }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.donation.type_donation')" width="200px" align="left">
        <template slot-scope="scope">
          <span>{{ scope.row.type_donation | typeDonationFilter }}</span>
          <br>
          <small>{{ scope.row.patient | fullName }}</small>
        </template>
      </el-table-column>
      <el-table-column v-if="isAreaPromotion" :label="$t('models.donation.event')" width="200px" align="left">
        <template slot-scope="scope">
          <span v-if="scope.row.event">{{ scope.row.event.name }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.donation.place')" width="155px" align="center">
        <template slot-scope="scope">
          <span v-if="scope.row.place">{{ scope.row.place.name }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.donation.last_donation_at')" width="200px" align="center">
        <template slot-scope="scope">
          <span>{{ formatDonationDate(scope.row.last_donation_at) }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.donation.employee')" width="300" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.employee | fullName }}</span>
        </template>
      </el-table-column>
      <el-table-column
        :label="$t('actions')"
        fixed="right"
        align="center"
        width="230"
        class-name="small-padding"
      >
        <template slot-scope="scope">
          <el-tooltip :enterable="false" :content="$t('details')" class="item" effect="dark">
            <el-button v-if="checkPermission(['view_donor'])"  @click="handleEdit(scope.row)" size="mini">
              <font-awesome-icon icon="align-justify"/>
            </el-button>
          </el-tooltip>

          <el-tooltip :enterable="false" :content="$t('edit')" class="item" effect="dark">
            <el-button
              v-if="checkPermission(['change_donation'])"
              size="mini"
              @click.stop.prevent="handleUpdate(scope.row)"
            >
              <font-awesome-icon icon="edit" />
            </el-button>
          </el-tooltip>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination-container">
      <el-pagination
        v-show="total>0"
        :current-page="listQuery.page"
        :page-sizes="[10,20,30, 50]"
        :page-size="listQuery.limit"
        :total="total"
        background
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible" width="90%" destroy-on-close>
      <el-row :gutter="20">
        <el-col :md="24">
          <div class="grid-content">
            <el-form
              ref="dataForm"
              :rules="rules"
              :model="temp"
              style="width: 100%;"
            >
              <span v-if="dialogStatus!=='update'">
                <el-form-item :label="$t('models.donation.donor')" prop="donor_id">
                  <el-select
                    v-model="temp.donor_id"
                    :placeholder="$t('please_select')"
                    :remote-method="remoteMethod"
                    :loading="loadingDonor"
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
              </span>
              <el-form-item :label="$t('models.donation.type_process')" prop="type_process">
                <el-radio-group v-model="temp.type_process">
                  <el-radio-button v-for="item in typeProcessOptions" :key="item.key" :label="item.key">
                    {{ item.display_name }}
                  </el-radio-button>
                </el-radio-group>
              </el-form-item>
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
              <el-form-item
                :label="$t('models.donation.place')"
                prop="place_id"
              >
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

              <el-form-item
                :label="$t('models.extraction.receptor_fullname') + ' (Para quién está donando)'"
                prop="patient_id"
              >
                <el-select
                  v-model="temp.patient_id"
                  :placeholder="$t('please_select')"
                  :loading="patientLoading"
                  :remote-method="remotePatient"
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
              <el-form-item :label="$t('models.donation.event')" prop="event_id">
                <el-select
                  v-model="temp.event_id"
                  :placeholder="$t('please_select')"
                  :remote-method="getListEvents"
                  :loading="loadingSelectEvents"
                  filterable
                  remote
                  clearable
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
        <el-col :md="6"><p>&nbsp;</p></el-col>
        <el-col v-if="donor && !donor.can_donate" :md="18">
          <div class="grid-content">
            <el-alert
              :closable="false"
              title="El Donante seleccionado en la anterior donación fue RECHAZADO DE FORMA PERMANENTE"
              type="error"
            />
          </div>
        </el-col>
      </el-row>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">{{ $t('cancel') }}</el-button>
        <el-button
          v-if="checkPermission(['change_donation'])"
          :disabled="!(donor && donor.can_donate)"
          type="primary"
          @click="dialogStatus !== 'update' ? createData(): updateData()"
        >
          {{ $t('confirm') }}
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import { mapGetters } from 'vuex'
import patients from '@/query/patient'
import moment from 'moment'
import { graphqlRequest } from '@/api/graphql'
import { debounce } from 'debounce'
import donors from '@/query/donor'
import places from '@/query/place'
import donations from '@/query/donation'
import events from '@/query/event'
import { getDonationEligibility, getLastDonationDate } from '@/utils/donationEligibility'

const typeDonationOptions = [
  { key: 'VA', display_name: 'VOLUNTARIA ALTRUISTA' },
  { key: 'RS', display_name: 'REPOSICION SOLIDARIA' },
  { key: 'RE', display_name: 'REPOSICION EXIGIDA' },
  { key: 'DA', display_name: 'DONACION AUTOLOGA' }
]
const typeProcessOptions = [
  { key: 'NO', display_name: 'DONACION CONVENCIONAL' },
  { key: 'NA', display_name: 'DONACION AFERESIS' }
]

const statusOptions = [
  { key: 'NU', display_name: 'NUEVO' },
  { key: 'EP', display_name: 'EN PROCESO' },
  { key: 'CO', display_name: 'COMPLETADO' },
  { key: 'RE', display_name: 'DIFERIDO' }
]

const typeDonationKeyValue = typeDonationOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

const typeProcessKeyValue = typeProcessOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'DonationList',
  components: { },
  directives: {},
  filters: {
    typeDonationFilter(type) {
      return typeDonationKeyValue[type]
    },
    typeProcessFilter(type) {
      return typeProcessKeyValue[type]
    },
    statusFilter(row) {
      var step = ''
      if (row.extraction) {
        step = 'EXTRACCION'
      } else if (row.clinicalhistoryanswer) {
        step = 'HISTORIA CLINICA'
      } else if (row.physicalanalysis) {
        step = 'ANALISIS FISICO'
      } else if (row.exam) {
        step = 'PRE-TAMIZAJE'
      } else {
        step = 'NUEVO'
      }

      return step
    },
    colorReactiveFilter(row) {
      let variable = 'white'
      if (row.rejected) {
        if (row.rejected.reason.type === 'PE') {
          variable = 'orange'
        } else {
          variable = 'yellow'
        }
      } else if (row.immunoserology) {
        const imm = row.immunoserology
        if (imm.hiv === 'R' || imm.hbsag === 'R' || imm.hvc === 'R' || imm.cheia === 'R' || imm.chagas_hai === 'R' || imm.rpr === 'R') {
          variable = 'red'
        }
      }
      return variable
    }
  },
  data() {
    return {
      pickerOptions: {
        disabledDate(time) {
          return time.getTime() > Date.now()
        }
      },
      pickerOptions2: {
        disabledDate(time) {
          return time.getTime() > Date.now()
        },
        shortcuts: [{
          text: 'Mes Actual',
          onClick(picker) {
            const start = moment().startOf('month').format('YYYY-MM-DD')
            const end = moment().format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
          }
        }, {
          text: 'Mes Anterior',
          onClick(picker) {
            const start = moment().subtract(1, 'months').startOf('month').format('YYYY-MM-DD')
            const end = moment().subtract(1, 'months').endOf('month').format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
          }
        }, {
          text: 'Año Actual',
          onClick(picker) {
            var thisYear = (new Date()).getFullYear()
            var startDate = new Date('1/1/' + thisYear)
            const start = moment(startDate.valueOf()).format('YYYY-MM-DD')
            const end = moment().format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
          }
        }]
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
      listLoading: true,
      loadingDonor: true,
      patientLoading: false,
      loadingSelectEvents: false,
      placeLoading: false,
      eventLoading: false,
      listQuery: {
        page: 1,
        limit: 20,
        offset: 0,
        search: '',
        ordering: '-id',
        from: 'main',
        extra: {
          date_init: '',
          date_end: '',
          patient_id: ''
        },
        date_range: [moment().startOf('month').format('YYYY-MM-DD'), moment().format('YYYY-MM-DD')]
      },
      listQueryEvent: {
        page: 1,
        limit: 20,
        search: '',
        ordering: '-init_at',
        is_active: true
      },
      listDonorQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-id' },
      listEventQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-init_at', is_active: true, id: undefined },
      listPatientQuery: {
        page: 1,
        limit: 20,
        offset: 0,
        search: '',
        ordering: 'first_name, middle_name, last_name',
        id: undefined
      },
      listPlaceQuery: { page: 1, limit: 50, offset: 0, search: '', ordering: 'name' },
      typeDonationOptions,
      typeProcessOptions,
      statusOptions,
      temp: {
        id: undefined,
        donor_id: undefined,
        place_id: undefined,
        event_id: undefined,
        employee_id: undefined,
        last_donation_at: null,
        register_at: '',
        type_donation: 'VA',
        type_process: 'NO'
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
          residence: '',
          patient_id: ''
        },
        status: '',
        register_at: ''
      },
      dialogFormVisible: false,
      dialogShowVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Editando Donación',
        create: 'Creando Donación',
        create_with_covid: 'Creando Donación con COVID-19',
        create_with_apheresis: 'Creando Donación con Aféresis',
        create_with_covid_apheresis: 'Creando Donación con COVID-19 y Aféresis'
      },
      rules: {
        donor_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        place_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        type_process: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        type_donation: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        register_at: [{ required: true, message: this.$t('is_required') }],
        last_donation_at: [{ required: false, message: this.$t('is_required'), trigger: 'change' }],
        patient_id: [{ required: false, message: this.$t('is_required'), trigger: 'change' }],
        employee_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        event_id: []
      },
      downloadLoading: false,
      isAreaPromotion: false,
      donationEligibility: null,
      selectedDonorLastDonationAt: null,
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
      },
      canSaveDonation: false,
      typeProcessDialogVisible: false
    }
  },
  computed: {
    ...mapGetters([
      'employees',
      'employee_id',
      'min_date_edit'
    ])
  },
  watch: {
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
    this.getList()
  },
  mounted() {
    this.getListPatients()
  },
  methods: {
    checkPermission,
    formatDonationDate(value) {
      const date = moment(value)
      return date.isValid() ? date.format('DD-MM-YYYY') : ''
    },
    textReactiveFilter(row) {
      let variable = ''
      if (row.rejected) {
        if (row.rejected.reason.type === 'PE') {
          variable = 'Diferido Permanente'
        } else {
          variable = 'Diferido Temporal'
        }
      } else if (row.immunoserology) {
        const imm = row.immunoserology
        if (imm.hiv === 'R' || imm.hbsag === 'R' || imm.hvc === 'R' || imm.cheia === 'R' || imm.chagas_hai === 'R' || imm.rpr === 'R') {
          variable = 'Serologia Reactiva'
        }
      }
      return variable
    },
    remotePatient(query) {
      if (query !== '') {
        this.listPatientQuery.search = query
      } else {
        this.listPatientQuery.search = ''
      }
      this.getListPatients()
    },
    getListPatients() {
      this.patientLoading = true
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
    getLastDonation(donor) {
      const lastDonationAt = getLastDonationDate(donor)
      this.selectedDonorLastDonationAt = lastDonationAt
      this.temp = Object.assign({}, this.temp, { last_donation_at: lastDonationAt })
      if (!lastDonationAt) {
        this.donationEligibility = null
        this.loadDonorHistory(donor.id)
        return
      }
      this.updateDonationEligibility()
    },
    loadDonorHistory(id) {
      this.loadingDonor = true
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
        this.donor = donor
        const donorIndex = (this.donors || []).findIndex(item => String(item.id) === String(id))
        if (donorIndex !== -1) {
          this.$set(this.donors, donorIndex, donor)
        }
        this.selectedDonorLastDonationAt = getLastDonationDate(donor)
        this.temp = Object.assign({}, this.temp, {
          last_donation_at: this.selectedDonorLastDonationAt
        })
        this.updateDonationEligibility()
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
        this.loadingDonor = false
      })
    },
    updateDonationEligibility() {
      if (!this.temp.donor_id || !this.donor || !this.donor.can_donate) {
        this.donationEligibility = null
        return
      }
      this.donationEligibility = getDonationEligibility(this.selectedDonorLastDonationAt, this.temp.register_at)
    },
    canDonate(id) {
      const donor = (this.donors || []).find(item => String(item.id) === String(id))
      if (!donor) {
        this.donor = { can_donate: true }
        this.selectedDonorLastDonationAt = null
        this.temp = Object.assign({}, this.temp, { donor_id: undefined, last_donation_at: null })
        this.donationEligibility = null
        return
      }
      this.donor = donor
      this.getLastDonation(donor)
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
    getListDonors() {
      this.loadingDonor = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'donors',
          query: donors.list(this.listDonorQuery)
        }
      ).then(response => {
        const data = response.data
        this.donors = data.donors.results
        this.loadingDonor = false
      })
    },
    getListPlaces() {
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
    getListEvents(query) {
      this.loadingSelectEvents = true
      graphqlRequest(
        {
          from: this.$route.name,
          query: events.donation_select(this.listEventQuery)
        }
      ).then(response => {
        const data = response.data
        this.events = data.events.results
        this.loadingSelectEvents = false
      })
    },
    remoteMethod(query) {
      if (query !== '') {
        this.listDonorQuery.search = query
      } else {
        this.listDonorQuery.search = ''
      }
      this.getListDonors()
    },
    filterWithRangePicker(event) {
      if (event !== null) {
        this.listQuery.date_init = moment(event[0]).format('YYYY-MM-DD')
        this.listQuery.date_end = moment(event[1]).format('YYYY-MM-DD')
        this.listQuery.search = ''
        this.getList()
      }
    },
    getList() {
      this.listLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'donations',
          query: donations.listDonations(this.listQuery)
        }
      ).then(response => {
        const data = response.data

        this.list = data.donations.results
        this.total = data.donations.totalCount
        this.listLoading = false
      })
    },
    handleFilter: debounce(function(e) {
      this.listQuery.page = 1
      this.listQuery.offset = 0
      this.getList()
    }, 500),
    handleSizeChange(val) {
      this.listQuery.limit = val
      this.getList()
    },
    handleCurrentChange(val) {
      this.listQuery.page = val
      this.listQuery.offset = this.listQuery.limit * (val - 1)
      this.getList()
    },
    handleOrderChange(val) {
      if (val['prop'] !== 'register_at') {
        this.listQuery.ordering = (val['order'] === 'descending' ? '-' : '') + val['prop']
      } else {
        // default sorting
        this.listQuery.ordering = '-register_at,-donor__code'
      }
      this.getList()
    },
    handleModifyStatus(row, status) {
      this.$message({
        message: '操作成功',
        type: 'success'
      })
      row.status = status
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        place: { id: undefined },
        donor: { id: undefined },
        type_donation: 'VA',
        type_process: 'NO',
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
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.canSaveDonation = true
      this.getListDonors()
      this.getListPatients()
      this.getListEvents()
      this.getListPlaces()
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.register_id = this.employee_id
          if (tempData.patient_id === '') tempData.patient_id = undefined
          if (tempData.event_id === '') tempData.event_id = undefined
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
              this.getList()
              this.dialogFormVisible = false
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
    handleEdit(row, event) {
      this.$router.push({ name: 'donationDetail', params: { id: row.id }})
    },
    checkEditDonation(register_at) {
      if (checkPermission(['edit_every_time_institution'])) {
        this.canSaveDonation = true
      } else {
        this.canSaveDonation = moment(register_at, 'YYYY-MM-DD') >= moment(this.min_date_edit, 'YYYY-MM-DD')
      }
    },
    handleUpdate(row) {
      this.donationEligibility = null
      this.getListPlaces()
      this.checkEditDonation(row.register_at)

      const tempData = Object.assign({}, row)
      tempData.donor_id = tempData.donor.id
      tempData.place_id = tempData.place.id
      tempData.employee_id = tempData.employee.id

      if (tempData.event) {
        tempData.event_id = tempData.event.id
        this.listEventQuery.id = tempData.event_id
        this.getListEvents()
        this.listEventQuery.id = undefined
      }

      if (tempData.patient) {
        tempData.patient_id = tempData.patient.id
        this.listPatientQuery.id = tempData.patient_id
        this.getListPatients()
        this.listPatientQuery.id = undefined
      }

      this.temp = tempData

      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      const tempData = Object.assign({}, this.temp)
      if (tempData == null) this.temp.last_donation_at = null
      this.temp = tempData

      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          if (tempData.patient_id === '') tempData.patient_id = undefined
          if (tempData.event_id === '') tempData.event_id = undefined
          tempData.register_id = this.employee_id
          tempData.is_will_back = false
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
              this.getList()
              this.dialogFormVisible = false
              this.$notify({
                title: 'Estado',
                message: 'Registro actualizado',
                type: 'success',
                duration: 2000
              })
            }
          })
        } else {
          this.getList()
          this.dialogFormVisible = false
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

<style>
.el-table .warning-row {
  background: rgba(249, 0, 4, 0.22);
}

.el-table .success-row {
  background: #f0f9eb;
}

.donation-eligibility-alert {
  margin-top: 12px;
}

.donation-eligibility-alert .el-alert__title {
  font-size: 16px;
  font-weight: 700;
  line-height: 1.4;
}

.red {
  background-color: red;
}

.orange {
  background-color: orange;
}

.yellow {
  background-color: yellow;
}

.white {
  background-color: transparent;
}

.circle {
  width: 13px;
  height: 13px;
  border-radius: 50%;
  -moz-border-radius: 50px;
  -webkit-border-radius: 50px;
  display: inline-block;
}
</style>

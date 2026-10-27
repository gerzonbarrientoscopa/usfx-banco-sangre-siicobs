<template>
  <div class="app-container">
    <div class="filter-container">
      <el-row :gutter="20">
        <el-col :md="20">
          <div class="block">
            <div class="demonstration">Fecha Inicial / Fecha Final</div>
            <el-date-picker
              v-model="listQuery.date_range"
              :picker-options="pickerOptions"
              align="right"
              end-placeholder="Fecha Final"
              format="dd-MM-yyyy"
              range-separator="A"
              start-placeholder="Fecha Inicial"
              type="daterange"
              unlink-panels
              value-format="yyyy-MM-dd"
              @change="handleFilter"
            />
          </div>
        </el-col>

      </el-row>
    </div>

    <div class="filter-container">
      <el-input
        v-model.lazy="listQuery.search"
        :autofocus="'autofocus'"
        :placeholder="$t('donors.search')"
        class="filter-item"
        clearable
        prefix-icon="el-icon-search"
        @input="handleFilter"
      />
      <el-button
        v-if="checkPermission(['add_exam'])"
        class="filter-item"

        style="margin-left: 10px;"
        type="primary"
        @click="handleCreate"
      >{{ $t('add') }}
      </el-button>
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      stripe
      style="width: 100%;"
    >
      <el-table-column :label="$t('models.exam.register_at')" align="center" fixed width="150px">
        <template slot-scope="scope">
          <el-tooltip
            class="item"
            effect="dark"
            placement="top"
          >
            <div slot="content">Fecha de Tamizaje: {{ scope.row.donation.register_at | toHumanDate }}</div>
            <small :class="scope.row.register_at === scope.row.donation.register_at ? '': 'fg-orange'">
              <i class="el-icon-time" style="font-size: 15px" />
            </small>
          </el-tooltip>
          <span> {{ scope.row.register_at | toHumanDate }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.donor.code')" align="center" width="90px">
        <template slot-scope="scope">
          <strong>{{ scope.row.donation.donor.code }}</strong>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.exam.donation')" align="left" width="300px">
        <template slot-scope="scope">
          <span>{{ scope.row.donation.donor | fullName }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.exam.hematocrit')" align="center" width="110px">
        <template slot-scope="scope">
          <span v-if="scope.row.hematocrit">{{ scope.row.hematocrit }} %</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.exam.hemoglobin')" align="center" width="140px">
        <template slot-scope="scope">
          <span v-if="scope.row.hemoglobin">{{ scope.row.hemoglobin }} gr/dl</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.exam.blood_group')" align="center" width="140px">
        <template slot-scope="scope">
          <span>{{ scope.row.blood_group | bloodGroupFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.exam.chagas')" align="center" width="140px">
        <template slot-scope="scope">
          <span>{{ scope.row.chagas | typeChagasFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.exam.rpr')" align="center" width="140px">
        <template slot-scope="scope">
          <span>{{ scope.row.rpr | typeRprFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.exam.employee')" align="center" width="155px">
        <template slot-scope="scope">
          <span>{{ scope.row.employee | fullName }}</span>
        </template>
      </el-table-column>
      <el-table-column
        :label="$t('actions')"
        align="center"
        class-name="small-padding"
        fixed="right"
        width="230"
      >
        <template slot-scope="scope">
          <el-tooltip :content="$t('edit')" :enterable="false" class="item" effect="dark">
            <el-button v-if="checkPermission(['change_exam'])" size="mini" @click="handleUpdate(scope.row)"><font-awesome-icon icon="pencil-alt" /></el-button>
          </el-tooltip>
          <el-tooltip :enterable="false" class="item" content="Diferir" effect="dark">
            <el-button v-if="checkPermission(['add_rejected'])" :disabled="scope.row.donation.rejected !== null" size="mini" @click="handleRejected(scope.row)"><font-awesome-icon icon="allergies" /></el-button>
          </el-tooltip>
          <el-tooltip :enterable="false" class="item" content="Código de Barras" effect="dark">
            <el-button size="mini" type="default" @click="handlePrintQR(scope.row)">
              <font-awesome-icon icon="barcode" />
            </el-button>
          </el-tooltip>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination-container">
      <el-pagination
        v-show="total>0"
        :current-page="listQuery.page"
        :page-size="listQuery.limit"
        :page-sizes="[10,20,30, 50]"
        :total="total"
        background
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible" destroy-on-close width="80%">
      <el-row :gutter="20">
        <el-col :md="12">
          <el-form
            ref="dataForm"
            :model="temp"
            :rules="rules"
            label-position="right"
            label-width="170px"
            style="width: 100%;"
          >
            <div class="grid-content">
              <el-form-item :label="$t('models.exam.donation')" prop="donation_id">
                <el-select
                  v-if="action === 'create'"
                  v-model="temp.donation_id"
                  :loading="loadingDonation"
                  :placeholder="$t('please_select')"
                  :remote-method="remoteMethodDonation"
                  automatic-dropdown
                  class="filter-item"
                  filterable
                  remote
                  @change="getConfigValidation"
                >
                  <el-option
                    v-for="item in donations"
                    :key="item.id"
                    :label="item.donor | donorCodeFullName"
                    :value="item.id"
                  >
                    <span style="float: left"><strong>{{ item.donor.code }}</strong> {{ item.donor | fullName }}</span>
                    <span style="float: right; color: #8492a6; font-size: 13px">{{ item.register_at| toHumanDateMonthLetter }}</span>
                  </el-option>
                </el-select>
                <span v-if="action === 'update'" class="text-text-turquoise" style="font-weight: bolder">
                  {{ temp.donation.donor | donorCodeFullName }}
                </span>
              </el-form-item>

              <el-form-item :label="$t('models.extraction.register_at')" prop="register_at">
                <el-date-picker
                  v-model="temp.register_at"
                  :placeholder="$t('models.extraction.register_at')"
                  format="dd-MM-yyyy"
                  type="date"
                  value-format="yyyy-MM-dd"
                />
              </el-form-item>

              <el-form-item :label="$t('models.exam.hematocrit')" prop="hematocrit">
                <el-input v-model.number="temp.hematocrit" type="number" @change="setHemoglobin()">
                  <template slot="append">%</template>
                </el-input>
                <el-alert
                  v-if="validationDinamic && isNotValidHematocrit"
                  :closable="false"
                  show-icon
                  title=""
                >
                  <slot>
                    Rango permitido  Min:{{ validationDinamic.current_hematocrit_min }} Max:{{ validationDinamic.current_hematocrit_max }}
                  </slot>
                </el-alert>
              </el-form-item>

              <el-form-item :label="$t('models.exam.hemoglobin')" prop="hemoglobin">
                <el-input v-model.number="temp.hemoglobin" type="number" @change="setHematocrit()">
                  <template slot="append">gr/dl</template>
                </el-input>
              </el-form-item>

              <el-form-item :label="$t('models.exam.blood_group')" prop="blood_group">
                <el-select v-model="temp.blood_group" :placeholder="$t('please_select')" class="filter-item">
                  <el-option
                    v-for="item in bloodGroupOptions"
                    :key="item.key"
                    :label="item.display_name"
                    :value="item.key"
                  />
                </el-select>
              </el-form-item>

              <el-form-item :label="$t('models.exam.chagas')" prop="chagas">
                <el-select v-model="temp.chagas" :placeholder="$t('please_select')" class="filter-item">
                  <el-option
                    v-for="item in typeChagasOptions"
                    :key="item.key"
                    :label="item.display_name"
                    :value="item.key"
                  />
                </el-select>
              </el-form-item>

              <el-form-item :label="$t('models.exam.rpr')" prop="rpr">
                <el-select v-model="temp.rpr" :placeholder="$t('please_select')" class="filter-item">
                  <el-option
                    v-for="item in typeRprOptions"
                    :key="item.key"
                    :label="item.display_name"
                    :value="item.key"
                  />
                </el-select>
              </el-form-item>

              <el-form-item :label="$t('models.exam.observations')" prop="observations">
                <el-input v-model="temp.observations" :rows="2" type="textarea" @input.native="setUpperCase(temp, 'observations', $event)" />
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
        </el-col>
        <el-col v-show="isRejected || openRejected" :md="12">
          <el-form
            ref="dataFormRejected"
            :model="rejected"
            :rules="rulesRejected"
            label-position="right"
            label-width="170px"
            style="width: 100%;"
          >
            <div class="grid-content">
              <el-alert
                :closable="false"
                title="Detalle de Diferimiento"
                type="error"
              >
                <el-row :gutter="20">
                  <el-col :md="24" :sm="24">
                    <el-form-item :label="$t('models.rejected.type')" prop="type">
                      <el-select
                        v-model="rejected.type"
                        :placeholder="$t('please_select')"
                        class="filter-item"
                        @change="getReason(rejected.type)"
                      >
                        <el-option
                          v-for="item in typeReasonOptions"
                          :key="item.key"
                          :label=" item.display_name"
                          :value="item.key"
                        />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  <el-col :md="24" :sm="24">
                    <el-form-item :label="$t('models.rejected.reason')" prop="reason_id">
                      <el-select
                        v-model="rejected.reason_id"
                        :loading="loadingReasons"
                        :placeholder="$t('please_select')"
                        automatic-dropdown
                        class="filter-item"
                      >
                        <el-option
                          v-for="item in filteredReasons"
                          :key="item.id"
                          :label="item.name "
                          :value="item.id"
                        />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  <el-col :md="24" :sm="24">
                    <el-form-item :label="$t('models.rejected.observations')" prop="observations">
                      <el-input v-model="rejected.observations" :rows="4" type="textarea" @input.native="setUpperCase(rejected, 'observations', $event)" />
                    </el-form-item>
                  </el-col>
                </el-row>
              </el-alert>
            </div>
          </el-form>
        </el-col>
      </el-row>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">{{ $t('cancel') }}</el-button>
        <el-button v-show="isConfirm" @click="dialogStatus==='create'?createData():updateData()">{{ $t('accept') }}</el-button>
        <el-button v-show="isRejected" @click="dialogStatus==='create'?createData():updateData()">{{ $t('rejected') }}</el-button>
      </div>
    </el-dialog>

    <el-dialog
      :visible.sync="reportDialogVisible"
      center
      title="Reporte"
      top="10px"
      width="100%"
    >
      <report-dialog v-if="!reportDialogLoading" :row="pdf" />
      <div v-if="reportDialogLoading" class="loading-report">
        <i class="el-icon-loading" style="font-size: 80px" />
      </div>
    </el-dialog>
    <el-dialog
      :before-close="handleCloseRejectedForm"
      :visible.sync="rejectedDialogVisible"
      destroy-on-close
      title="DETALLE DE DIFERIMIENTO"
      width="70%"
    >
      <rejected-dialog :row="{temp: temp.donation ? temp.donation.rejected : null, donation: temp.donation, resource_id: temp.id, resource: 'Exam'}" @dialogState="handleCloseRejectedForm" />
    </el-dialog>
    <el-dialog :before-close="handleCloseQR" :title="textMap[dialogStatus]" :visible.sync="dialogQRVisible" destroy-on-close>
      <tubing-qr :id="donor_id" @dialogStatus="handleCloseQR" />
    </el-dialog>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import { mapGetters } from 'vuex'
import { printPreSieveAll } from '@/api/exam'
import rejecteds from '@/query/rejected'
import ReportDialog from '../report-dialog/ReportDialog'
import RejectedDialog from '../rejected/rejected'
import { graphqlRequest } from '@/api/graphql'
import exams from '@/query/exam'
import reasons from '@/query/reason'
import donations from '@/query/donation'
import { debounce } from 'debounce'
import tubingQr from './../extractions/tubingQR'
import moment from 'moment'
import { buildRegisterAtFilter } from "@/utils/general"

const typeChagasOptions = [
  { key: 'R', display_name: 'REACTIVO' },
  { key: 'NR', display_name: 'NO REACTIVO' }
]

const typeRprOptions = [
  { key: 'R', display_name: 'REACTIVO' },
  { key: 'NR', display_name: 'NO REACTIVO' }
]

const typeReasonOptions = [
  { key: 'TE', display_name: 'TEMPORAL' },
  { key: 'PE', display_name: 'PERMANENTE' }
]
const bloodGroupOptions = [
  { key: 'O+', display_name: 'O RH+' },
  { key: 'A+', display_name: 'A RH+' },
  { key: 'B+', display_name: 'B RH+' },
  { key: 'AB+', display_name: 'AB RH+' },
  { key: 'O-', display_name: 'O RH-' },
  { key: 'A-', display_name: 'A RH-' },
  { key: 'B-', display_name: 'B RH-' },
  { key: 'AB-', display_name: 'AB RH-' }
]

const typeChagasKeyValue = typeChagasOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

const typeReasonKeyValue = typeReasonOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

const typeRprKeyValue = typeRprOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

const bloodGroupKeyValue = bloodGroupOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'Exam',
  components: { ReportDialog, RejectedDialog, tubingQr },
  directives: {},
  filters: {
    typeChagasFilter(type) {
      return typeChagasKeyValue[type]
    },
    typeRprFilter(type) {
      return typeRprKeyValue[type]
    },
    bloodGroupFilter(type) {
      return bloodGroupKeyValue[type]
    },
    typeReasonFilter(type) {
      return typeReasonKeyValue[type]
    }
  },
  data() {
    return {
      pickerOptions: {
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
      pdf: null,
      reportDialogVisible: false,
      reportDialogLoading: false,
      dialogQRVisible: false,
      rejectedDialogVisible: false,
      openRejected: false,
      tableKey: 0,
      donations: null,
      settingPhysicals: null,
      current_place: null,
      list: null,
      donation: null,
      total: null,
      loadingDonation: false,
      listLoading: true,
      listDonationQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-id', from: 'PT' },
      listReasonQuery: { page: 1, limit: 50, offset: 0, search: '', ordering: 'name' },
      bloodGroupOptions,
      typeChagasOptions,
      typeRprOptions,
      listQuery: {
        page: 1,
        limit: 20,
        offset: 0,
        search: '',
        ordering: '-id',
        date_range: [moment().startOf('month').format('YYYY-MM-DD'), moment().format('YYYY-MM-DD')]
      },
      temp: {
        id: undefined,
        donation_id: undefined,
        hematocrit: undefined,
        hemoglobin: undefined,
        remark: '',
        register_at: undefined,
        title: '',
        type: '',
        status: 'published',
        age: '',
        degree_instruction: '',
        observations: ''
      },

      // datos de rechazo
      typeReasonOptions,
      reasons: null,
      filteredReasons: null,
      loadingReasons: null,
      rejected_status: false,
      rejected: {
        id: undefined,
        reason_id: undefined,
        donation: undefined,
        type: '',
        observations: '',
        employee: undefined,
        resource_id: undefined,
        resource: '',
        register_at: ''
      },
      validationDinamic: {
        current_hematocrit_min: undefined,
        current_hematocrit_max: undefined,
        hemoglobin_factor: undefined
      },
      dialogFormVisible: false,
      dialogStatus: '',
      action: '',
      textMap: {
        update: 'Modificando Examen Pre-Tamizaje',
        create: 'Creando Examen Pre-Tamizaje'
      },
      rules: {
        donation_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        hematocrit: [{ required: false, message: this.$t('is_required'), trigger: 'blur' }, { type: 'number', message: 'Debe ser número' }],
        hemoglobin: [{ required: false, message: this.$t('is_required'), trigger: 'blur' }, { type: 'number', message: 'Debe ser número' }],
        rpr: [{ required: false, message: this.$t('is_required'), trigger: 'change' }],
        chagas: [{ required: false, message: this.$t('is_required'), trigger: 'change' }],
        blood_group: [{ required: false, message: this.$t('is_required'), trigger: 'change' }],
        employee_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        observations: [{ required: false, trigger: 'blur' }]
      },
      rulesRejected: {
        type: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        reason_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        observations: []
      },
      downloadLoading: false,
      donor_id: null,
      currentGender: ''
    }
  },
  computed: {
    ...mapGetters([
      'employees',
      'employee_id'
    ]),
    isHaveChagasOrRpr: function() {
      return (this.temp.chagas === 'R' || this.temp.rpr === 'R')
    },
    isNotValidHematocrit: function() {
      if (this.temp.hematocrit) {
          return (this.temp.hematocrit < this.validationDinamic.current_hematocrit_min || this.temp.hematocrit > this.validationDinamic.current_hematocrit_max)
      } else {
        return false
      }
    },
    isRejected: function() {
      return this.isHaveChagasOrRpr || this.isNotValidHematocrit
    },
    isConfirm: function() {
      return !this.isHaveChagasOrRpr && !this.isNotValidHematocrit
    }
  },
  watch: {
    'rejected.type': function(value) {
      if (value !== undefined || value !== null) {
        this.getReason(value)
      }
    }
  },
  created() {
    this.getList()
    this.getListReasons()
  },
  methods: {
    checkPermission,
    getReason(id) {
      this.filteredReasons = this.reasons.filter(function(item) {
        return item.type === id
      })
    },
    getListReasons() {
      this.loadingReasons = true
      graphqlRequest(
        {
          from: this.$route.name,
          query: reasons.exam_select(this.listReasonQuery)
        }
      ).then(response => {
        const data = response.data
        this.reasons = data.reasons.results
        this.loadingReasons = false
      })
    },
    getConfigValidation(donation_id) {
      this.getDonation(donation_id)
    },
    getDonation(id) {
      var donation = this.donations.filter(function(item) {
        return item.id === id
      })
      this.donation = donation[0]

      this.validationDinamic = this.donation.place.settingphysical
      this.currentGender = this.donation.donor.gender
    },
    getListDonations() {
      this.loadingDonation = true
      graphqlRequest(
        {
          from: this.$route.name,
          query: donations.preSieveDonationSelect(this.listDonationQuery)
        }
      ).then(response => {
        const data = response.data
        this.donations = data.donations.results
        this.loadingDonation = false
      })
    },
    remoteMethodDonation(query) {
      if (query !== '') {
        this.listDonationQuery.search = query
      } else {
        this.listDonationQuery.search = ''
      }
      this.getListDonations()
    },
    getList() {
      this.listLoading = true
      let tempListQuery = Object.assign({}, this.listQuery)
      tempListQuery = buildRegisterAtFilter(tempListQuery)
      graphqlRequest(
        {
          from: this.$route.name,
          query: exams.list(tempListQuery),
          variables: tempListQuery
        }
      ).then(response => {
        const data = response.data
        this.list = data.exams.results
        this.total = data.exams.totalCount
        this.listLoading = false
      })
    },
    handleFilter: debounce(function() {
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
        employee: { id: undefined },
        donation: { id: undefined },
        observations: '',
        register_at: moment().format('YYYY-MM-DD')
      }
      this.listDonorQuery = {
        page: 1,
        limit: 20,
        search: undefined,
        ordering: '-id'
      }
    },
    resetRejected() {
      this.rejected = {
        type: '',
        reason_id: undefined,
        observations: ''
      }
    },
    handleCreate() {
      this.getListDonations()
      this.action = 'create'
      this.resetTemp()

      const tempData = Object.assign({}, this.temp)
      tempData.employee_id = this.employee_id
      this.temp = tempData

      this.resetRejected()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true

      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
        this.$refs['dataFormRejected'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.register_id = this.employee_id

          if (this.isRejected) {
            this.$refs['dataFormRejected'].validate((valid) => {
              if (valid) {
                graphqlRequest(
                  {
                    from: this.$route.name,
                    service: 'createExam',
                    query: exams.createExam(),
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
                    this.createRejectedData(response.data.create_exam.exam.id)
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
          } else {
            graphqlRequest(
              {
                from: this.$route.name,
                service: 'createExam',
                query: exams.createExam(),
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
        }
      })
    },
    createRejectedData(resource_id) {
      this.$refs['dataFormRejected'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.rejected)
          tempData.donation_id = this.temp.donation_id
          tempData.employee_id = this.temp.employee_id
          tempData.resource = 'Exam'
          tempData.register_at = this.temp.register_at
          tempData.resource_id = resource_id
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'createRejected',
              query: rejecteds.createRejected(),
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
              this.$notify({
                title: 'Estado',
                message: 'Registro de Diferimiento se ha creado',
                type: 'success',
                duration: 2000
              })
            }
          })
        }
      })
    },
    updateRejectedData() {
      this.$refs['dataFormRejected'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.rejected)
          tempData.donation_id = this.temp.donation_id
          tempData.employee_id = this.temp.employee_id
          tempData.register_at = this.temp.register_at
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'updateRejected',
              query: rejecteds.updateRejected(),
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
              this.$notify({
                title: 'Estado',
                message: 'Registro de Diferimiento se ha actualizado',
                type: 'success',
                duration: 2000
              })
            }
          })
        }
      })
    },
    handleUpdateRejected() {
      if (this.temp.donation.rejected && this.temp.donation.rejected.resource === 'Exam') {
        this.openRejected = true
        const tempData = Object.assign({}, this.temp.donation.rejected)
        tempData.type = tempData.reason.type
        tempData.reason_id = tempData.reason.id
        this.rejected = tempData
      } else {
        this.resetRejected()
        this.openRejected = false
      }
    },
    handleUpdate(row) {
      this.action = 'update'

      const tempData = Object.assign({}, row)
      tempData.donation_id = tempData.donation.id
      tempData.employee_id = tempData.employee.id
      this.temp = tempData

      this.handleUpdateRejected()
      this.dialogStatus = 'update'
      this.dialogFormVisible = true

      this.currentGender = this.temp.donation.donor.gender

      let settingPhysical = this.temp.donation.place.settingphysical

      this.validationDinamic = {
        current_hematocrit_min: settingPhysical.hematocrit_min,
        current_hematocrit_max: settingPhysical.hematocrit_max,
        hemoglobin_factor: settingPhysical.hemoglobin_factor
      }

      if (this.currentGender === 'M') {
        this.validationDinamic.current_hematocrit_min = settingPhysical.hematocrit_min_m
        this.validationDinamic.current_hematocrit_max = settingPhysical.hematocrit_max_m
      }

      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
        this.$refs['dataFormRejected'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.register_id = this.employee_id

          if (this.isRejected || this.openRejected) {
            this.$refs['dataFormRejected'].validate((valid) => {
              if (valid) {
                graphqlRequest(
                  {
                    from: this.$route.name,
                    service: 'updateExam',
                    query: exams.updateExam(),
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
                    if (this.temp.donation.rejected && this.temp.donation.rejected.resource === 'Exam') {
                      this.updateRejectedData()
                    } else {
                      this.createRejectedData(this.temp.id)
                    }
                    this.dialogFormVisible = false
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
          } else {
            graphqlRequest(
              {
                from: this.$route.name,
                service: 'updateExam',
                query: exams.updateExam(),
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
          }
        }
      })
    },
    handlePrintPreSieve() {
      this.reportDialogVisible = true
      this.reportDialogLoading = true
      printPreSieveAll().then(
        response => {
          this.pdf = response
          this.reportDialogLoading = false
        }
      )
    },
    setHemoglobin() {
      const temp = Object.assign({}, this.temp)
      temp.hemoglobin = +Number(temp.hematocrit * (this.validationDinamic.hemoglobin_factor * 0.1)).toFixed(2)
      this.temp = temp
    },
    setHematocrit() {
      const temp = Object.assign({}, this.temp)
      temp.hematocrit = +Number(temp.hemoglobin / (this.validationDinamic.hemoglobin_factor * 0.1)).toFixed(2)
      this.temp = temp
    },
    handleRejected(row) {
      this.rejectedDialogVisible = true
      this.temp = row
    },
    handleCloseRejectedForm() {
      this.rejectedDialogVisible = false
      this.getList()
    },
    handlePrintQR(examTemp) {
      this.dialogStatus = 'printQR'
      this.dialogQRVisible = true
      this.donor_id = examTemp.donation.id
    },
    handleCloseQR() {
      this.dialogQRVisible = false
    }
  }
}
</script>

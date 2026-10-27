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
        v-if="checkPermission(['add_physicalanalysis'])"
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
      <el-table-column :label="$t('models.physical-analysis.register_at')" align="center" fixed width="150px">
        <template slot-scope="scope">
          <el-tooltip
            class="item"
            effect="dark"
            placement="top"
          >
            <div slot="content">Fecha de Donación: {{ scope.row.donation.register_at | toHumanDate }}</div>
            <small :class="scope.row.register_at === scope.row.donation.register_at ? '': 'fg-orange'">
              <i class="el-icon-time" style="font-size: 15px" />
            </small>
          </el-tooltip>
          <span> {{ scope.row.register_at | toHumanDate }}</span>
          <br>
          <small>

          </small>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.physical-analysis.donation')" align="left" fixed width="320px">
        <template slot-scope="scope">
          <span><strong>{{ scope.row.donation.donor.code }}</strong> {{ scope.row.donation.donor | fullName }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.physical-analysis.systolic')" align="center" width="110">
        <template slot-scope="scope">
          <span v-if="scope.row.systolic">{{ scope.row.systolic }} mmHg.</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.physical-analysis.diastolic')" align="center" width="110">
        <template slot-scope="scope">
          <span v-if="scope.row.diastolic">{{ scope.row.diastolic }} mmHg.</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.physical-analysis.pulse')" align="center" width="110">
        <template slot-scope="scope">
          <span v-if="scope.row.pulse">{{ scope.row.pulse }} /min</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.physical-analysis.tall')" align="center" width="110">
        <template slot-scope="scope">
          <span v-if="scope.row.tall">{{ scope.row.tall }} cm.</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.physical-analysis.weight')" align="center" width="110">
        <template slot-scope="scope">
          <span v-if="scope.row.weight">{{ scope.row.weight }} Kg.</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.physical-analysis.temperature')" align="center" width="110">
        <template slot-scope="scope">
          <span v-if="scope.row.temperature">{{ scope.row.temperature }} °C</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.physical-analysis.hematocrit')" align="center" width="110">
        <template slot-scope="scope">
          <span v-if="scope.row.donation.exam.hematocrit">{{ scope.row.donation.exam.hematocrit }} %</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.physical-analysis.hemoglobin')" align="center" width="110">
        <template slot-scope="scope">
          <span v-if="scope.row.donation.exam.hemoglobin">{{ scope.row.donation.exam.hemoglobin }} gr/dl</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.physical-analysis.employee')" align="left" width="320px">
        <template slot-scope="scope">
          <span>{{ scope.row.employee | fullName }}</span>
        </template>
      </el-table-column>
      <el-table-column
        :label="$t('actions')"
        align="center"
        class-name="small-padding"
        fixed="right"
        width="170"
      >
        <template slot-scope="scope">
          <el-tooltip :content="$t('edit')" :enterable="false" class="item" effect="dark">
            <el-button v-if="checkPermission(['change_physicalanalysis'])" size="mini" @click="handleUpdate(scope.row)"><font-awesome-icon icon="edit" /></el-button>
          </el-tooltip>
          <el-tooltip :enterable="false" class="item" content="Diferir" effect="dark">
            <el-button v-if="checkPermission(['add_rejected'])" :disabled="scope.row.donation.rejected !== null" size="mini"  @click="handleRejected(scope.row)"><font-awesome-icon icon="allergies" /></el-button>
          </el-tooltip>
          <el-tooltip :enterable="false" class="item" content="Imprimir Analisis Físico" effect="dark">
            <el-button size="mini" @click="handlePrint(scope.row)"><font-awesome-icon icon="print" /></el-button>
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
            label-position="left"
            label-width="120px"
            style="width: 100%;"
          >
            <div class="grid-content">
              <el-form-item :label="$t('models.physical-analysis.donation')" prop="donation_id">
                <el-select
                  v-if="dialogStatus === 'create'"
                  v-model="temp.donation_id"
                  :loading="loadingDonation"
                  :placeholder="$t('please_select')"
                  :remote-method="remoteMethodDonation"
                  automatic-dropdown
                  class="filter-item"
                  filterable
                  remote
                  @change="getSetting(temp.donation_id)"
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
                <span v-if="dialogStatus === 'update'" class="text-text-turquoise" style="font-weight: bolder">
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

              <el-form-item :label="$t('models.physical-analysis.systolic')" prop="systolic">
                <el-input v-model.number="temp.systolic" type="number">
                  <template slot="append">mmHg.</template>
                </el-input>
                <el-alert
                  v-if="c_set && isValidSystolic"
                  :closable="false"
                  :title="'Rango permitido  Min: ' + c_set.systolic_min + ' Max: '+ c_set.systolic_max "
                  show-icon
                />
              </el-form-item>

              <el-form-item :label="$t('models.physical-analysis.diastolic')" prop="diastolic">
                <el-input v-model.number="temp.diastolic" type="number">
                  <template slot="append">mmHg.</template>
                </el-input>
                <el-alert
                  v-if="c_set && isValidDiastolic"
                  :closable="false"
                  :title="'Rango permitido  Min: ' + c_set.diastolic_min + ' Max: '+ c_set.diastolic_max "
                  show-icon
                />
              </el-form-item>

              <el-form-item :label="$t('models.physical-analysis.pulse')" prop="pulse">
                <el-input v-model.number="temp.pulse" type="number">
                  <template slot="append">/min.</template>
                </el-input>
                <el-alert
                  v-if="c_set && isValidPulse"
                  :closable="false"
                  :title="'Rango permitido  Min: ' + c_set.pulse_min + ' Max: '+ c_set.pulse_max "
                  show-icon
                />
              </el-form-item>

              <el-form-item :label="$t('models.physical-analysis.tall')" prop="tall">
                <el-input v-model.number="temp.tall" type="number">
                  <template slot="append">cm.</template>
                </el-input>
              </el-form-item>

              <el-form-item :label="$t('models.physical-analysis.weight')" prop="weight">
                <el-input v-model.number="temp.weight" type="number">
                  <template slot="append">Kg.</template>
                </el-input>
                <el-alert
                  v-if="c_set && isValidWeight"
                  :closable="false"
                  :title="'Peso Min: ' + c_set.weight_min "
                  show-icon
                />
              </el-form-item>

              <el-form-item :label="$t('models.physical-analysis.temperature')" prop="temperature">
                <el-input v-model.number="temp.temperature" type="number">
                  <template slot="append">°C</template>
                </el-input>
              </el-form-item>

              <el-form-item :label="$t('models.physical-analysis.hematocrit')" prop="hematocrit">
                <el-input v-model.number="temp.hematocrit" disabled type="number">
                  <template slot="append">%</template>
                </el-input>
              </el-form-item>

              <el-form-item :label="$t('models.physical-analysis.hemoglobin')" prop="hemoglobin">
                <el-input v-model.number="temp.hemoglobin" disabled type="number">
                  <template slot="append">gr/dl</template>
                </el-input>
              </el-form-item>

              <el-form-item :label="$t('models.physical-analysis.observations')" prop="observations">
                <el-input v-model="temp.observations" :rows="2" type="textarea" @input.native="setUpperCase(temp, 'observations', $event)" />
              </el-form-item>
              <el-form-item :label="$t('models.physical-analysis.employee')" prop="employee_id">
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
            label-position="left"
            label-width="120px"
            style="width: 100%;"
          >
            <div class="grid-content">
              <el-alert
                :closable="false"
                title="Detalle de Diferimiento"
                type="error"
              >
                <div class="grid-content">
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
                </div>
              </el-alert>
            </div>
          </el-form>
        </el-col>
      </el-row>

      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">{{ $t('cancel') }}</el-button>
        <el-button v-show="isConfirm" @click="dialogStatus==='create'?createData():updateData()">{{ $t('confirm') }}</el-button>
        <el-button v-show="isRejected"  @click="dialogStatus==='create'?createData():updateData()">{{ $t('rejected') }}</el-button>
      </div>
    </el-dialog>

    <el-dialog
      :visible.sync="reportDialogVisible"
      center
      title="HISTORIA CLINICA DEL DONANTE"
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
      <rejected-dialog :row="{temp: temp.donation ? temp.donation.rejected : null, donation: temp.donation, resource_id: temp.id, resource: 'PhysicalAnalysis'}" @dialogState="handleCloseRejectedForm" />
    </el-dialog>

  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import { mapGetters } from 'vuex'
import { printClinicalhistory } from '@/api/donation'
import ReportDialog from '../report-dialog/ReportDialog'
import RejectedDialog from '../rejected/rejected'
import moment from 'moment'
import { graphqlRequest } from '@/api/graphql'
import physicalAnalysis from '@/query/physicalAnalysis'
import reasons from '@/query/reason'
import donations from '@/query/donation'
import rejecteds from '@/query/rejected'
import { debounce } from 'debounce'

const typeReasonOptions = [
  { key: 'TE', display_name: 'TEMPORAL' },
  { key: 'PE', display_name: 'PERMANENTE' }
]

export default {
  name: 'PhysicalAnalysis',
  components: { ReportDialog, RejectedDialog },
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
      pdf: ArrayBuffer,
      tableKey: 0,
      donations: null,
      donation: null,
      settingPhysicals: null,
      exam: null,
      exams: null,
      list: null,
      total: null,
      loadingDonation: false,
      loadingSetting: false,
      listLoading: true,
      listDonationQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-id', from: 'AF' },
      listQuery: {
        page: 1,
        limit: 20,
        offset: 0,
        search: '',
        ordering: '-id',
        date_range: [moment().startOf('month').format('YYYY-MM-DD'), moment().format('YYYY-MM-DD')]
      },
      listReasonQuery: { page: 1, limit: 50, offset: 0, search: '', ordering: 'name' },
      temp: {
        id: undefined,
        donation_id: undefined,
        systolic: undefined,
        diastolic: undefined,
        pulse: undefined,
        weight: undefined,
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
      c_set: {
        systolic_min: undefined,
        systolic_max: undefined,
        diastolic_min: undefined,
        diastolic_max: undefined,
        pulse_min: undefined,
        pulse_max: undefined,
        weight_min: undefined
      },
      dialogFormVisible: false,
      reportDialogVisible: false,
      reportDialogLoading: false,
      dialogStatus: '',
      textMap: {
        update: 'Editando',
        create: 'Creando'
      },
      // datos de rechazo
      typeReasonOptions,
      reasons: null,
      filteredReasons: null,
      loadingReasons: null,
      rejected_status: false,
      openRejected: false,
      rejected: {
        id: undefined,
        reason_id: undefined,
        donation: undefined,
        type: '',
        observations: '',
        employee: undefined,
        resource_id: undefined,
        resource: '',
        register_at: moment().format('YYYY-MM-DD')
      },
      rules: {
        donation_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        register_at: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        systolic: [{ required: false, message: this.$t('is_required') }, { type: 'number', message: 'Debe ser número', trigger: 'blur' }],
        diastolic: [{ required: false, message: this.$t('is_required') }, { type: 'number', message: 'Debe ser número', trigger: 'blur' }],
        pulse: [{ required: false, message: this.$t('is_required') }, { type: 'number', message: 'Debe ser número', trigger: 'blur' }],
        tall: [{ required: false, message: this.$t('is_required') }, { type: 'number', message: 'Debe ser número', trigger: 'blur' }],
        weight: [{ required: false, message: this.$t('is_required') }, { type: 'number', message: 'Debe ser número', trigger: 'blur' }],
        temperature: [{ required: false, message: this.$t('is_required') }, { type: 'number', message: 'Debe ser número', trigger: 'blur' }],
        observations: [{ required: false, message: this.$t('is_required') }],
        employee_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }]
      },
      rulesRejected: {
        type: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        reason_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        observations: []
      },
      rejectedDialogVisible: false
    }
  },
  computed: {
    ...mapGetters([
      'employees',
      'employee_id'
    ]),
    isValidSystolic: function() {
      if (this.temp.systolic) {
        return this.temp.systolic < this.c_set.systolic_min || this.temp.systolic > this.c_set.systolic_max
      } else {
        return true
      }
    },
    isValidDiastolic: function() {
      if (this.temp.diastolic) {
        return this.temp.diastolic < this.c_set.diastolic_min || this.temp.diastolic > this.c_set.diastolic_max
      } else {
        return true
      }
    },
    isValidPulse: function() {
      if (this.temp.pulse) {
        return this.temp.pulse < this.c_set.pulse_min || this.temp.pulse > this.c_set.pulse_max
      } else {
        return true
      }
    },
    isValidWeight: function() {
      if (this.temp.weight) {
        return this.temp.weight < this.c_set.weight_min
      } else {
        return true
      }
    },
    isRejected: function() {
      return (this.c_set && (this.isValidSystolic || this.isValidDiastolic || this.isValidPulse || this.isValidWeight))
    },
    isConfirm: function() {
      return !this.isValidSystolic && !this.isValidDiastolic && !this.isValidPulse && !this.isValidWeight
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
    updateHematocritHemoglobinFromExam() {
      if (this.temp.donation.exam) {
        this.temp.hematocrit = this.temp.donation.exam.hematocrit
        this.temp.hemoglobin = this.temp.donation.exam.hemoglobin
      }
    },
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
          service: 'reasons',
          query: reasons.physicalAnalysis_select(this.listReasonQuery)
        }
      ).then(response => {
        const data = response.data
        this.reasons = data.reasons.results
        this.loadingReasons = false
      })
    },
    getSetting(id) {
      const donation = this.donations.filter(function(item) {
        return item.id === id
      })

      this.donation = donation[0]
      this.c_set = this.donation.place.settingphysical

      if (this.donation.exam) {
        if (this.donation.exam.hematocrit) {
          this.temp.hematocrit = donation.exam.hematocrit
        }

        if (this.donation.exam.hemoglobin) {
          this.temp.hemoglobin = donation.exam.hemoglobin
        }
      }
    },
    getListDonations() {
      this.loadingDonation = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'donations',
          query: donations.physicalAnalysisDonationSelect(this.listDonationQuery)
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
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'physical_analysis',
          query: physicalAnalysis.list(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.physicalanalyses.results
        this.total = data.physicalanalyses.totalCount
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
    },
    resetRejected() {
      this.rejected = {
        type: '',
        reason_id: undefined,
        observations: '',
        register_at: moment().format('YYYY-MM-DD')
      }
    },
    handleCreate() {
      this.resetTemp()
      this.resetRejected()
      const tempData = Object.assign({}, this.temp)
      tempData.employee_id = this.employee_id
      this.temp = tempData

      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.getListDonations()

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
                    service: 'createPhysicalAnalysis',
                    query: physicalAnalysis.createPhysicalAnalysis(),
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
                    this.createRejectedData(response.data.create_physicalanalysis.physicalanalysis.id)
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
                service: 'createPhysicalAnalysis',
                query: physicalAnalysis.createPhysicalAnalysis(),
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
          tempData.resource = 'PhysicalAnalysis'
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
    getSettingUpdateData() {
      this.c_set = this.temp.donation.place.settingphysical
    },
    handleUpdateRejected() {
      if (this.temp.donation.rejected && this.temp.donation.rejected.resource === 'PhysicalAnalysis') {
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
      const tempData = Object.assign({}, row)
      tempData.donation_id = tempData.donation.id
      tempData.employee_id = tempData.employee.id
      this.temp = tempData

      this.getSettingUpdateData()
      this.handleUpdateRejected()
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.updateHematocritHemoglobinFromExam()
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
                    service: 'updatePhysicalAnalysis',
                    query: physicalAnalysis.updatePhysicalAnalysis(),
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
                    if (this.temp.donation.rejected && this.temp.donation.rejected.resource === 'PhysicalAnalysis') {
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
                service: 'updatePhysicalAnalysis',
                query: physicalAnalysis.updatePhysicalAnalysis(),
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
    handlePrint(row) {
      this.reportDialogVisible = true
      this.reportDialogLoading = true
      this.temp = Object.assign({}, row)
      printClinicalhistory(this.temp.donation.id).then(
        response => {
          this.pdf = response
          this.reportDialogLoading = false
        }
      )
    },
    handleRejected(row) {
      this.rejectedDialogVisible = true
      this.temp = row
    },
    handleCloseRejectedForm() {
      this.rejectedDialogVisible = false
      this.getList()
    }
  }
}
</script>
<style>
  .button-form {
    padding-top: 5px;
    float: right;
    margin-bottom: 5px;
    width: 85%;
  }
</style>

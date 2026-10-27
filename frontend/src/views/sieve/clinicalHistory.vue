<template>
  <div class="app-container">
    <div class="filter-container">
      <el-row :gutter="20">
        <el-col :md="20">
          <div class="block">
            <div class="demonstration">Fecha Inicial / Fecha Final</div>
            <el-date-picker
              v-model="listQuery.date_range"
              :picker-options="pickerRangeOptions"
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
        :placeholder="$t('search')"
        class="filter-item"
        clearable
        prefix-icon="el-icon-search"
        @input="handleFilter"
      />
      <el-button
        v-if="checkPermission(['add_clinicalhistoryanswer'])"
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
      <el-table-column :label="$t('models.clinical-history.register_at')" align="center" width="150px">
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
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.clinical-history.donation')" width="320px">
        <template slot-scope="scope">
          <span><strong>{{ scope.row.donation.donor.code }}</strong> {{ scope.row.donation.donor | fullName }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.clinical-history.questionnaire_id')" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.questionnaire.title }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.clinical-history.employee')" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.employee|fullName }}</span>
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
            <el-button v-if="checkPermission(['change_clinicalhistoryanswer'])" size="mini" @click="handleUpdate(scope.row)">
              <font-awesome-icon icon="edit" />
            </el-button>
          </el-tooltip>
          <el-tooltip :enterable="false" class="item" content="Diferir" effect="dark">
            <el-button v-if="checkPermission(['add_rejected'])" :disabled="scope.row.donation.rejected !== null" size="mini" @click="handleRejected(scope.row)">
              <font-awesome-icon icon="allergies" />
            </el-button>
          </el-tooltip>
          <el-tooltip :enterable="false" class="item" content="Imprimir Historia Clínica" effect="dark">
            <el-button size="mini" @click="handlePrint(scope.row)">
              <font-awesome-icon icon="print" />
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

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible" destroy-on-close width="60%">
      <el-form
        ref="dataForm"
        :model="temp"
        :rules="rules"
        label-position="top"
        label-width="100%"
        style="width: 100%;"
      >
        <el-row :gutter="20">
          <el-col :md="24" :sm="24">
            <div class="grid-content">
              <el-form-item :label="$t('models.clinical-history.donation')" prop="donation_id">
                <el-select
                  v-if="dialogStatus === 'create'"
                  v-model="temp.donation_id"
                  :loading="loadingDonation"
                  :placeholder="$t('please_select')"
                  :remote-method="remoteGetDonation"
                  automatic-dropdown
                  class="filter-item"
                  filterable
                  remote
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
              <el-form-item :label="$t('models.clinical-history.register_at')" prop="register_at">
                <el-date-picker
                  v-model="temp.register_at"
                  :placeholder="$t('models.clinical-history.register_at')"
                  format="dd-MM-yyyy"
                  type="date"
                  value-format="yyyy-MM-dd"
                />
              </el-form-item>
              <el-form-item :label="$t('models.clinical-history.questionnaire')" prop="questionnaire_id">

                <el-row :gutter="10">
                  <el-col :md="18">
                    <el-select v-model="temp.questionnaire_id" :placeholder="$t('please_select')" class="filter-item" @change="getForm(temp.questionnaire_id)">
                      <el-option
                        v-for="item in questionnaires"
                        :key="item.id"
                        :label="item.title"
                        :value="item.id"
                      />
                    </el-select>
                  </el-col>
                  <el-col :md="6">
                    <el-button v-if="dialogStatus === 'create'" @click="setFormNo()">
                      Poner todo en NO
                    </el-button>
                  </el-col>
                </el-row>
              </el-form-item>
              <div v-for="(q, index) in form" :key="q.id">
                <el-form-item :label="(index + 1) +' ' +q.title" prop="name">
                  <el-input v-if="q.type === 'TEXT'" v-model="q.value" />

                  <el-radio-group v-if="q.type === 'RADIO'" v-model="q.value">
                    <el-radio label="SI" />
                    <el-radio label="NO" />
                  </el-radio-group>
                  <el-form-item :label="q.sub_title" prop="name">
                    <el-input v-if="q.sub_type === 'TEXT'" v-model="q.sub_value" />

                    <el-radio-group v-if="q.sub_type === 'RADIO'" v-model="q.sub_value">
                      <el-radio label="SI" />
                      <el-radio label="NO" />
                    </el-radio-group>
                  </el-form-item>
                </el-form-item>
              </div>
              <el-form-item :label="$t('models.clinical-history.observations')" prop="temperature">
                <el-input v-model="temp.observations" type="textarea" @input.native="setUpperCase(temp, 'observations', $event)" />
              </el-form-item>
            </div>
          </el-col>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          {{ $t('cancelButtonText') }}
        </el-button>
        <el-button @click="dialogStatus==='create'?createData():updateData()">
          {{ $t('confirmButtonText') }}
        </el-button>
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
      <rejected-dialog :row="{temp: temp.donation ? temp.donation.rejected : null, donation: temp.donation, resource_id: temp.id, resource: 'ClinicalHistory'}" @dialogState="handleCloseRejectedForm" />
    </el-dialog>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import { mapGetters } from 'vuex'
import { printClinicalHistoryAnswers } from '@/api/clinicalHistory'
import donations from '@/query/donation'
import ReportDialog from '../report-dialog/ReportDialog'
import RejectedDialog from '../rejected/rejected'
import moment from 'moment'
import { graphqlRequest } from '@/api/graphql'
import clinicalHistoryAnswers from '@/query/clinicalHistoryAnswer'
import clinicalHistoryQuestions from '@/query/clinicalHistoryQuestion'
import { debounce } from 'debounce'
import { defaultshorcouts } from '@/utils/date-utils'

export default {
  name: 'ClinicalHistory',
  components: { ReportDialog, RejectedDialog },
  data() {
    return {
      pickerRangeOptions: {
        disabledDate(time) {
          return time.getTime() > Date.now()
        },
        shortcuts: defaultshorcouts()
      },
      pdf: null,
      reportDialogVisible: false,
      reportDialogLoading: false,
      rejectedDialogVisible: false,
      n: 0,
      tableKey: 0,
      list: null,
      questionnaires: null,
      donations: null,
      donation: null,
      form: [],
      total: null,
      loadingDonation: true,
      listDonationQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-id' },
      listQueryQuestions: { page: 1, limit: 20, offset: 0, search: '', ordering: '-id' },
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        offset: 0,
        search: '',
        ordering: '-register_at, -donation__donor__code',
        date_range: [moment().startOf('month').format('YYYY-MM-DD'), moment().format('YYYY-MM-DD')]
      },
      showReviewer: false,
      for_loop: 0,
      temp: {
        id: undefined,
        questionnaire_id: undefined,
        donation_id: undefined,
        responses: [],
        register_at: moment().format('YYYY-MM-DD')
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Editando Historia Clinica ',
        create: 'Creando Historia Clinica'
      },
      rules: {
        register_at: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        donation_id: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        questionnaire_id: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        responses: [{ required: true, message: this.$t('is_required') }],
        observations: [{ required: false, message: this.$t('is_required') }]
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
  created() {
    this.getList()
  },
  methods: {
    checkPermission,
    setFormNo() {
      if (this.temp.questionnaire_id) {
        var formNew = []
        this.form.forEach(function(obj) {
          var tempData = Object.assign({}, obj)
          if (tempData.type === 'RADIO') tempData.value = 'NO'
          if (tempData.sub_type === 'RADIO') tempData.sub_value = 'NO'
          formNew.push(tempData)
        })
        this.form = formNew
      } else {
        this.$message({
          message: 'Seleccione un formulario',
          type: 'error'
        })
      }
    },
    getListQuestionnaires() {
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'clinicalHistoryQuestions',
          query: clinicalHistoryQuestions.list(this.listQueryQuestions)
        }
      ).then(response => {
        const data = response.data
        this.questionnaires = data.clinicalhistoryquestions.results
        const newQuestionnaireList = []
        for (const q of this.questionnaires) {
          if (q.id !== 2) {
            newQuestionnaireList.push(q)
          }
        }
        this.questionnaires = newQuestionnaireList
      })
    },
    getList() {
      this.listLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'clinicalHistoryAnswers',
          query: clinicalHistoryAnswers.listClinicalHistory(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.clinicalhistoryanswers.results
        this.total = data.clinicalhistoryanswers.totalCount
        this.listLoading = false
      })
    },
    remoteGetDonation(query) {
      if (query !== '') {
        this.listDonationQuery.search = query
      } else {
        this.listDonationQuery.search = ''
      }
      this.getListDonations()
    },
    getListDonations() {
      this.loadingDonation = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'donations',
          query: donations.clinicalHistoryDonationSelect(this.listDonationQuery)
        }
      ).then(response => {
        const data = response.data
        this.donations = data.donations.results
        this.loadingDonation = false
      })
    },
    getForm(form_id) {
      var form_selected = this.questionnaires.filter(function(item) {
        return item.id === form_id
      })
      this.form = form_selected[0].questions
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
    handleModifyStatus(row, status) {
      this.$message({
        message: 'Se modifico el estado de una fila',
        type: 'success'
      })
      row.status = status
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        questionnaire_id: undefined,
        donation_id: undefined,
        register_at: moment().format('YYYY-MM-DD')
      }
      this.form = null
    },
    handleCreate() {
      this.resetTemp()
      this.getListQuestionnaires()
      this.getListDonations()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.responses = this.form
          tempData.employee_id = this.employee_id
          tempData.register_id = this.employee_id
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'createClinicalHistory',
              query: clinicalHistoryAnswers.createClinicalHistory(),
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
    handleUpdate(row) {
      this.getListQuestionnaires()

      const tempData = Object.assign({}, row)
      tempData.donation_id = tempData.donation.id
      tempData.questionnaire_id = tempData.questionnaire.id
      this.form = tempData.responses
      this.temp = tempData

      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.employee_id = this.employee_id
          tempData.register_id = this.employee_id
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'updateClinicalHistory',
              query: clinicalHistoryAnswers.updateClinicalHistory(),
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
      })
    },
    handlePrint(row) {
      this.reportDialogVisible = true
      this.reportDialogLoading = true
      this.temp = Object.assign({}, row)
      printClinicalHistoryAnswers(this.temp.id).then(
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

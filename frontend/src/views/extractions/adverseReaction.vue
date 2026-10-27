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
        <el-col :md="4">
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
        :autofocus="'autofocus'"
        :placeholder="$t('donors.search')"
        class="filter-item"
        clearable
        prefix-icon="el-icon-search"
        @input="handleFilter"
      />
      <el-button
        v-if="checkPermission(['add_adversereaction'])"
        class="filter-item"
        icon="el-icon-plus"
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
      style="width: 100%;"
    >
      <el-table-column :label="$t('models.adverseReaction.register_at')" align="center" fixed width="140px">
        <template slot-scope="scope">
          <span>{{ scope.row.register_at | toHumanDatetime }}</span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.donor.code')" align="center" width="120px">
        <template slot-scope="scope">
          <span><strong>{{ scope.row.extraction.donation.donor.code }}</strong></span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.adverseReaction.extraction_place')" align="center" width="180px">
        <template slot-scope="scope">
          <span>{{ scope.row.extraction_place | extractionPlaceFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.adverseReaction.evolution')" align="center" width="155px">
        <template slot-scope="scope">
          <span>{{ scope.row.evolution | evolutionFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.adverseReaction.detection')" align="center" width="155px">
        <template slot-scope="scope">
          <span>{{ scope.row.detection | detectionFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.adverseReaction.type')" align="center" width="300px">
        <template slot-scope="scope">
          <span v-for="item in scope.row.type" :key="item.id">{{ item.name }}, </span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.adverseReaction.behavior_taken')" align="center" width="385px">
        <template slot-scope="scope">
          <span>{{ scope.row.behavior_taken }}</span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.adverseReaction.employee')" align="center" width="320px">
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
          <el-button
            v-if="checkPermission(['change_adversereaction'])"
            size="mini"
            type="primary"
            @click="handleUpdate(scope.row)"
          >{{ $t('edit') }}
          </el-button>
          <el-button size="mini" type="primary" @click="handlePrint(scope.row)">{{ $t('print') }}</el-button>
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
        <el-col :md="24">
          <el-form
            ref="dataForm"
            :model="temp"
            :rules="rules"
            label-position="right"
            label-width="180px"
            style="width: 100%;"
          >
            <div class="grid-content">
              <el-form-item :label="$t('models.adverseReaction.donation')" prop="extraction_id">
                <el-select
                  v-if="dialogStatus === 'create'"
                  v-model="temp.extraction_id"
                  :loading="loadingExtraction"
                  :placeholder="$t('please_select')"
                  :remote-method="remoteMethodExtraction"
                  automatic-dropdown
                  class="filter-item"
                  filterable
                  remote
                  @change="getExtraction(temp.extraction_id)"
                >
                  <el-option
                    v-for="item in extractions"
                    :key="item.id"
                    :label="item.donation.donor.code"
                    :value="item.id"
                  >
                    <span style="float: left"><strong>{{ item.donation.donor.code }}</strong></span>
                    <span style="float: right; color: #8492a6; font-size: 13px">
                      {{ item.donation.register_at| toHumanDateMonthLetter }}
                    </span>
                  </el-option>
                </el-select>
                <span v-if="dialogStatus === 'update'" class="text-text-turquoise" style="font-weight: bolder">
                  {{ temp.extraction.donation.donor | donorCodeFullName }}
                </span>
              </el-form-item>
              <el-form-item :label="$t('models.fragmentation.register_at')" prop="register_at">
                <el-date-picker
                  v-model="temp.register_at"
                  placeholder="Seleccione fecha y hora"
                  type="datetime"
                />
              </el-form-item>

              <el-form-item :label="$t('models.adverseReaction.extraction_place')" prop="extraction_place">
                <el-radio-group v-model="temp.extraction_place">
                  <el-radio-button v-for="item in extractionPlaceOptions" :key="item.key" :label="item.key">
                    {{ item.display_name }}
                  </el-radio-button>
                </el-radio-group>
              </el-form-item>

              <el-form-item :label="$t('models.adverseReaction.detection')" prop="detection">
                <el-select v-model="temp.detection" :placeholder="$t('please_select')" class="filter-item">
                  <el-option
                    v-for="item in detectionOptions"
                    :key="item.key"
                    :label="item.display_name"
                    :value="item.key"
                  />
                </el-select>
              </el-form-item>

              <el-form-item :label="$t('models.adverseReaction.behavior_taken')" prop="behavior_taken">
                <el-input v-model="temp.behavior_taken" :rows="4" type="textarea" @input.native="setUpperCase(temp, 'behavior_taken', $event)" />
              </el-form-item>
              <el-form-item :label="$t('models.adverseReaction.evolution')" prop="evolution">
                <el-select v-model="temp.evolution" :placeholder="$t('please_select')" class="filter-item">
                  <el-option
                    v-for="item in evolutionOptions"
                    :key="item.key"
                    :label="item.display_name"
                    :value="item.key"
                  />
                </el-select>
              </el-form-item>
              <el-form-item :label="$t('models.adverseReaction.type')" prop="type_id">
                <el-select v-model="temp.type_id" automatic-dropdown class="filter-item" filterable multiple>
                  <el-option-group v-for="group in typeAdverseReactionList" :key="group.label" :label="group.label">
                    <el-option v-for="item in group.options" :key="item.value" :label="item.label" :value="item.value">
                      <span style="float: left">{{ item.label }}</span>
                      <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
                    </el-option>
                  </el-option-group>
                </el-select>
              </el-form-item>

              <el-form-item :label="$t('models.adverseReaction.observations')" prop="observations">
                <el-input v-model="temp.observations" :rows="2" type="textarea" @input.native="setUpperCase(temp, 'observations', $event)" />
              </el-form-item>
              <el-form-item :label="$t('models.extraction.employee')" prop="employee_id">
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
      </el-row>

      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">{{ $t('cancel') }}</el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">
          {{ $t('confirm') }}
        </el-button>
      </div>
    </el-dialog>

    <el-dialog
      :visible.sync="reportDialogVisible"
      center
      title="FICHA DE NOTIFICACIÓN DE REACCIÓN ADVERSA A LA DONACION"
      top="10px"
      width="100%"
    >
      <report-dialog v-if="!reportDialogLoading" :row="pdf" />
      <div v-if="reportDialogLoading" class="loading-report">
        <i class="el-icon-loading" style="font-size: 80px" />
      </div>
    </el-dialog>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import { mapGetters } from 'vuex'
import { printAdverseReaction } from '@/api/adverseReaction'
import ReportDialog from '../report-dialog/ReportDialog'
import { graphqlRequest } from '@/api/graphql'
import adverseReactions from '@/query/adverseReaction'
import typeAdverseReactions from '@/query/typeAdverseReaction'
import extractions from '@/query/extraction'
import { debounce } from 'debounce'
import moment from 'moment'

const typeReasonOptions = [
  { key: 'TE', display_name: 'TEMPORAL' },
  { key: 'PE', display_name: 'PERMANENTE' }
]
const evolutionOptions = [
  { key: 'RR', display_name: 'RECUPERACION RAPIDA' },
  { key: 'RL', display_name: 'RECUPERACION LENTA' },
  { key: 'HO', display_name: 'HOSPITALIZACION' }
]
const detectionOptions = [
  { key: 'TD', display_name: 'DURANTE LA DONACION' },
  { key: 'AD', display_name: 'DESPUES DE LA DONACION' }
]
const extractionPlaceOptions = [
  { key: 'PF', display_name: 'PUESTO FIJO' },
  { key: 'UM', display_name: 'UNIDAD MOVIL' }
]

const evolutionKeyValue = evolutionOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

const detectionKeyValue = detectionOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

const extrationPlaceKeyValue = extractionPlaceOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'Donation',
  components: { ReportDialog },
  directives: {},
  filters: {
    evolutionFilter(type) {
      return evolutionKeyValue[type]
    },
    detectionFilter(type) {
      return detectionKeyValue[type]
    },
    extractionPlaceFilter(type) {
      return extrationPlaceKeyValue[type]
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
      tableKey: 0,
      extractions: null,
      donation: {
        donor: null,
        place: null
      },
      typeAdverseReactionList: null,
      conventionalTypeAdverseReactionList: null,
      apheresisTypeAdverseReactionList: null,
      list: null,
      total: null,
      loading: false,
      listLoading: true,
      listTypeAdverseReactionLoading: true,
      listExtractionQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-id' },
      listQuery: {
        page: 1,
        limit: 20,
        offset: 0,
        search: '',
        ordering: '-register_at,-extraction__donation__donor__code',
        date_range: [moment().startOf('month').format('YYYY-MM-DD'), moment().format('YYYY-MM-DD')]
      },
      listTypeAdverseReactionQuery: { page: 1, limit: 50, offset: 0, search: '', ordering: 'name' },
      temp: {
        id: undefined,
        extraction_id: undefined,
        type_id: [],
        observations: '',
        employee_id: undefined,
        register_at: moment()
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Modificando Reaccion Adversa / Extracción Fallida',
        create: 'Añadiendo Reaccion Adversa / Extracción Fallida'
      },
      // datos de rechazo
      typeReasonOptions,
      detectionOptions,
      evolutionOptions,
      extractionPlaceOptions,
      rules: {
        register_at: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        extraction_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        type_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        evolution: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        detection: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        extraction_place: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        behavior_taken: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        observations: [],
        employee_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }]
      },
      downloadLoading: false,
      loadingExtraction: false
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
    getListTypeAdverseReaction() {
      this.listTypeAdverseReactionLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          query: typeAdverseReactions.adverseReaction_select(this.listTypeAdverseReactionQuery)
        }
      ).then(response => {
        const data = response.data
        this.groupedTypeAdverseReactionListMethod(data.typeadversereactions.results)
        this.listTypeAdverseReactionLoading = false
      })
    },
    groupedTypeAdverseReactionListMethod(typeAdverseReactions) {
      var apheresisList = [{ label: 'LEVE', options: [] }, { label: 'MODERADO', options: [] }, { label: 'SEVERA', options: [] }]
      var conventionalList = [{ label: 'LEVE', options: [] }, { label: 'MODERADO', options: [] }, { label: 'SEVERA', options: [] }]

      for (const tar of typeAdverseReactions) {
        if (tar.show_in_apheresis) {
          switch (tar.level) {
            case 'LOW':
              apheresisList[0].options.push({ label: tar.name, value: tar.id })
              break
            case 'MEDIUM':
              apheresisList[1].options.push({ label: tar.name, value: tar.id })
              break
            case 'HIGH':
              apheresisList[2].options.push({ label: tar.name, value: tar.id })
              break
          }
        }
        if (tar.show_in_conventional) {
          switch (tar.level) {
            case 'LOW':
              conventionalList[0].options.push({ label: tar.name, value: tar.id })
              break
            case 'MEDIUM':
              conventionalList[1].options.push({ label: tar.name, value: tar.id })
              break
            case 'HIGH':
              conventionalList[2].options.push({ label: tar.name, value: tar.id })
              break
          }
        }
      }

      this.apheresisTypeAdverseReactionList = apheresisList
      this.conventionalTypeAdverseReactionList = conventionalList
    },
    setTypeAdverseReactionList(extraction) {
      if (extraction && (extraction.donation.type_process === 'NA' || extraction.donation.type_process === 'CA')) {
        this.typeAdverseReactionList = this.apheresisTypeAdverseReactionList
      } else {
        this.typeAdverseReactionList = this.conventionalTypeAdverseReactionList
      }
    },
    getExtraction(id) {
      const extraction = this.extractions.filter(function(item) {
        return item.id === id
      })
      this.setTypeAdverseReactionList(extraction[0])
    },
    getListExtractions() {
      this.loadingExtraction = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'extractions',
          query: extractions.adverseReactionExtractionSelect(this.listExtractionQuery)
        }
      ).then(response => {
        const data = response.data
        this.extractions = data.extractions.results
        this.loadingExtraction = false
      })
    },
    remoteMethodExtraction(query) {
      if (query !== '') {
        this.listExtractionQuery.search = query
      } else {
        this.listExtractionQuery.search = ''
      }
      this.getListExtractions()
    },
    getList() {
      this.listLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          query: adverseReactions.list(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.adversereactions.results
        this.total = data.adversereactions.totalCount
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
    handleModifyStatus(row, status) {
      this.$message({
        message: '操作成功',
        type: 'success'
      })
      row.status = status
    },
    resetTemp() {
      this.temp = {
        employee_id: { id: undefined },
        donation: { id: undefined },
        type_id: [],
        observations: '',
        register_at: moment()
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.getListExtractions()
      this.getListTypeAdverseReaction()
      const tempData = Object.assign({}, this.temp)
      tempData.employee_id = this.employee_id
      this.temp = tempData
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'createAdverseReaction',
              query: adverseReactions.createAdverseReaction(),
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
      this.getListTypeAdverseReaction()
      const tempData = Object.assign({}, row)
      tempData.extraction_id = tempData.extraction.id
      tempData.employee_id = tempData.employee.id
      tempData.type_id = []
      for (const type of tempData.type) {
        tempData.type_id.push(type.id)
      }
      this.temp = tempData
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.setTypeAdverseReactionList(row.extraction)
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
              service: 'updateAdverseReaction',
              query: adverseReactions.updateAdverseReaction(),
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
      printAdverseReaction(this.temp.id).then(
        response => {
          this.pdf = response
          this.reportDialogLoading = false
        }
      )
    }
  }
}
</script>

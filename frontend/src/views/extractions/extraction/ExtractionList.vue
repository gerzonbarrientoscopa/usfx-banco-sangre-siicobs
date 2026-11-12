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
        :placeholder="$t('models.extraction.search')"
        class="filter-item"
        clearable
        prefix-icon="el-icon-search"
        @input="handleFilter"
      />
      <el-input
        v-model.number="listQuery.extraction_code"
        :placeholder="$t('models.extraction.extraction_code')"
        class="filter-item"
        clearable
        min="1"
        prefix-icon="el-icon-search"
        style="width: 230px;"
        type="number"
        @input="handleFilter"
      />
      <el-button
        v-if="checkPermission(['add_extraction'])"
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
      @row-click="handleEdit"
    >
      <el-table-column label="Fecha Extracción" align="center" fixed width="140px">
        <template slot-scope="scope">
          <span class="date-nowrap">
            {{ scope.row.register_at | toHumanDate }}
          </span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.donor.code')" align="center" width="100px">
        <template slot-scope="scope">
          <strong>{{ scope.row.donation.donor.code }}</strong>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.extraction.extraction_code')" align="center" width="145px">
        <template slot-scope="scope">
          <strong>{{ scope.row.id }}</strong>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.extraction.type_bag')" align="center" width="120px">
        <template slot-scope="scope">
          <span>{{ scope.row.type_bag | typeBagFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.extraction.lot')" align="center" width="110px">
        <template slot-scope="scope">
          <span>{{ scope.row.lot }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.extraction.tubing')" align="center" width="110px">
        <template slot-scope="scope">
          <span>{{ scope.row.tubing }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.extraction.type_place')" align="center" width="160px">
        <template slot-scope="scope">
          <span>{{ scope.row.type_place === 'PF' ? 'Puesto Fijo' : 'Puesto Móvil' }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.extraction.arm')" align="center" width="110px">
        <template slot-scope="scope">
          <span>{{ scope.row.arm | armFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.extraction.initial_time')" align="center" width="155px">
        <template slot-scope="scope">
          <span>{{ scope.row.initial_time }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.extraction.end_time')" align="center" width="110px">
        <template slot-scope="scope">
          <span>{{ scope.row.end_time }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.extraction.total_time')" align="center" width="110px">
        <template slot-scope="scope">
          <span>{{ scope.row.total_time }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.extraction.adverse_reactions')" align="center" width="155px">
        <template slot-scope="scope">
          <span>{{ scope.row.adversereaction !== null ? 'SI' : 'NO' }}</span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.extraction.observations')" align="center" width="155px">
        <template slot-scope="scope">
          <span>{{ scope.row.observations }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.extraction.employee')" align="center" width="155px">
        <template slot-scope="scope">
          <span>{{ scope.row.employee | fullName }}</span>
        </template>
      </el-table-column>
      <el-table-column
        :label="$t('actions')"
        align="center"
        class-name="small-padding"
        fixed="right"
        width="130"
      >
        <template slot-scope="scope">
          <el-tooltip :enterable="false" class="item" content="Código de Barras" effect="dark">
            <el-button size="mini" type="default" @click.stop.prevent="handlePrintBR(scope.row)">
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

    <el-dialog
      :title="reportTitle"
      :visible.sync="reportDialogVisible"
      center
      top="10px"
      width="100%"
    >
      <report-dialog v-if="!reportDialogLoading" :row="pdf" />
      <div v-if="reportDialogLoading" class="loading-report">
        <i class="el-icon-loading" style="font-size: 80px" />
      </div>
    </el-dialog>

    <el-dialog
      :before-close="handleCloseDialog"
      :destroy-on-close="!(dialogStatus==='printQR')"
      :title="textMap[dialogStatus]"
      :visible.sync="dialogFormVisible"
      :width="width_dialog"
    >
      <extraction-form
        v-if="dialogStatus==='create'"
        :is-editing="true"
        :row="temp"
        @dialogStatus="handleCloseDialog"
      />
      <tubing-qr v-if="dialogStatus==='printQR'" :id="id" @dialogStatus="handleCloseDialog" />
      <extraction-refreshment-form
        v-if="dialogStatus==='createExtractionRefreshment'"
        :row-extraction="temp"
        @dialogStatus="handleCloseDialog"
      />
      <immunoserology-form
        v-if="dialogStatus==='createSerology'"
        :row-extraction="temp"
        @dialogStatus="handleCloseDialog"
      />
      <immunohematology-form
        v-if="dialogStatus==='createHematology'"
        :row-extraction="temp"
        @dialogStatus="handleCloseDialog"
      />
    </el-dialog>

  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import { mapGetters } from 'vuex'
import { printAutoexclude } from '@/api/extraction'
import moment from 'moment'
import ReportDialog from '@/views/report-dialog/ReportDialog'
import tubingQr from '@/views/extractions/tubingQR'
import { graphqlRequest } from '@/api/graphql'
import extractions from '@/query/extraction'
import { debounce } from 'debounce'
import ExtractionRefreshmentForm from '@/views/extractions/refreshment/ExtractionRefreshmentForm'
import ExtractionForm from '@/views/extractions/extraction/tab/ExtractionForm'
import { defaultshorcouts } from '@/utils/date-utils'
import { buildBarcodeFilter, buildRegisterAtFilter } from '@/utils/general'
import { TYPE_BAG_LABELS } from '@/constants/type-bag'

const armOptions = [
  { key: 'I', display_name: 'IZQUIERDO' },
  { key: 'D', display_name: 'DERECHA' }
]

const armKeyValue = armOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'Extraction',
  components: {
    ReportDialog,
    tubingQr,
    ExtractionForm,
    ExtractionRefreshmentForm
  },
  directives: {},
  filters: {
    typeBagFilter(type) {
      return TYPE_BAG_LABELS[type]
    },
    armFilter(type) {
      return armKeyValue[type]
    }
  },
  data() {
    return {
      pickerOptions: {
        disabledDate(time) {
          return time.getTime() > Date.now()
        },
        shortcuts: defaultshorcouts()
      },
      tableKey: 0,
      pdf: null,
      reportDialogVisible: false,
      reportDialogLoading: false,
      reportTitle: '',
      list: null,
      total: null,
      listLoading: true,
      armOptions,
      listQuery: {
        page: 1,
        limit: 20,
        search: '',
        extraction_code: null,
        offset: 0,
        ordering: '-register_at',
        date_range: [moment().startOf('month').format('YYYY-MM-DD'), moment().format('YYYY-MM-DD')]
      },
      temp: { id: undefined },
      width_dialog: '90%',
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        create: 'Creando Extracción',
        createSerology: 'Creando Serología',
        createHematology: 'Creando Hematología',
        createExtractionRefreshment: 'Creando Asignación de  Refrigerio',
        printQR: 'Código de Barras'
      }
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
    handleEdit(row, event) {
      if (this.checkPermission(['change_extraction'])) {
        this.$router.push({ name: 'extractionDetail', params: { id: row.id }})
      }
    },
    handleCreate() {
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.temp = null
    },
    getList() {
      this.listLoading = true
      let tempListQuery = Object.assign({}, this.listQuery)

      const extractionCode = tempListQuery.extraction_code
      if (extractionCode !== null && extractionCode !== '' && Number.isInteger(Number(extractionCode))) {
        tempListQuery.id = Number(extractionCode)
      } else {
        delete tempListQuery.id
      }
      delete tempListQuery.extraction_code
      tempListQuery = buildBarcodeFilter(tempListQuery, 'donation__id')
      tempListQuery = buildRegisterAtFilter(tempListQuery)

      graphqlRequest(
        {
          from: this.$route.name,
          service: 'extractions',
          query: extractions.listExtraction(tempListQuery),
          variables: tempListQuery
        }
      ).then(response => {
        const data = response.data
        this.list = data.extractions.results
        this.total = data.extractions.totalCount
        this.listLoading = false
      })
    },
    existsNextStep(row) {
      return (row.donation.immunoserology || row.donation.immunohematology || row.fragmentation || row.extractionrefreshment)
    },
    getStatus(row) {
      var type = 'default'
      if (row.adversereaction) {
        type = 'danger'
      }
      return type
    },
    handleCommand(element) {
      const row = Object.assign({}, element.row)

      if (element.option === 'createSerology') {
        this.handleCreateSerology(row)
      } else if (element.option === 'createHematology') {
        this.handleCreateHematology(row)
      } else if (element.option === 'createExtractionRefreshment') {
        this.handleCreateExtractionRefreshment(row)
      }
    },
    handleCreateExtractionRefreshment(row) {
      this.dialogStatus = 'createExtractionRefreshment'
      this.width_dialog = '60%'
      this.dialogFormVisible = true
      this.temp = row
    },
    handleCreateSerology(row) {
      this.dialogStatus = 'createSerology'
      this.width_dialog = '90%'
      this.dialogFormVisible = true
      this.temp = row
    },
    handleCreateHematology(row) {
      this.dialogStatus = 'createHematology'
      this.width_dialog = '90%'
      this.dialogFormVisible = true
      this.temp = row
    },
    handlePrintBR(row) {
      this.dialogStatus = 'printQR'
      this.width_dialog = '40%'
      this.dialogFormVisible = true
      this.id = row.donation.id
    },
    handleCloseDialog() {
      this.dialogFormVisible = false
      this.getList()
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
    handlePrintExclude(row) {
      this.reportDialogVisible = true
      this.reportDialogLoading = true
      this.reportTitle = 'VOTO DE AUTOEXCLUSION'
      this.temp = Object.assign({}, row)
      printAutoexclude(this.temp.donation.id).then(
        response => {
          this.pdf = response
          this.reportDialogLoading = false
        }
      )
    }
  }
}
</script>
<style>
.fg-orange {
  color: #bd3739;
}

.date-nowrap {
  white-space: nowrap;
}
</style>

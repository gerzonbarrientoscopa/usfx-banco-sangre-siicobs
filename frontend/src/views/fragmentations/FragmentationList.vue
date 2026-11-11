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
        :placeholder="$t('models.fragmentation.search')"
        class="filter-item"
        clearable
        prefix-icon="el-icon-search"
        @input="handleFilter"
      />
      <el-button
        v-if="checkPermission(['add_fragmentation'])"
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
      style="width: 100%;"
    >
      <el-table-column :label="$t('models.fragmentation.register_at')" align="center" width="150px">
        <template slot-scope="scope">
          <span>{{ scope.row.register_at | toHumanDatetime }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.donor.code')" align="center" width="100px">
        <template slot-scope="scope">
          <span><strong>{{ scope.row.donor_code }}</strong></span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.fragmentation.tubing')" align="center" width="150px">
        <template slot-scope="scope">
          <span v-if="scope.row.extraction">
            {{ scope.row.extraction.tubing }}
          </span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.fragmentation.type_bag')" align="center" width="100px">
        <template slot-scope="scope">
          <span v-if="scope.row.extraction">{{ scope.row.extraction.type_bag | typeBagFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.fragmentation.weight')" align="right" width="80px">
        <template slot-scope="scope">
          <span>{{ scope.row.extraction.weight }} gr.</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.fragmentation.quality_bag')" align="center" width="100px">
        <template slot-scope="scope">
          <span>{{ scope.row.quality_bag | qualityBagFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.fragmentation.total_hc')" align="center" width="100px">
        <template slot-scope="scope">
          <span>{{ scope.row.total_hc }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.fragmentation.employee')" align="center" width="320px">
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
          <el-button size="mini" type="default" @click="handleShowItems(scope.row)">Hemocomponentes</el-button>
          <el-button v-if="checkPermission(['change_fragmentation'])" size="mini" @click="handleUpdate(scope.row)">{{ $t('edit') }}</el-button>
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

    <el-dialog :before-close="handleCloseForm" :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible" destroy-on-close width="90%">
      <fragmentation-form v-if="dialogStatus!=='view_items'" :row="temp" @dialogStatus="handleCloseForm" />
      <fragmentation-item-list v-if="dialogStatus==='view_items'" :fragmentation="temp" />
    </el-dialog>

    <el-dialog
      :title="titleReport"
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
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import { mapGetters } from 'vuex'
import { printRoadMap } from '@/api/fragmentation'
import FragmentationForm from './FragmentationForm'
import FragmentationItemList from './FragmentationItemList'
import ReportDialog from '../report-dialog/ReportDialog'
import moment from 'moment'
import { graphqlRequest } from '@/api/graphql'
import fragmentations from '@/query/fragmentation'
import { debounce } from 'debounce'
import { defaultshorcouts } from '@/utils/date-utils'
import { buildBarcodeFilter, buildRegisterAtFilter } from '@/utils/general'
import { TYPE_BAG_LABELS } from '@/constants/type-bag'

const qualityBagOptions = [
  { key: 'AP', display_name: 'APTO' },
  { key: 'NA', display_name: 'NO APTO' }
]

const qualityBagKeyValue = qualityBagOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'FragmentationList',
  components: { FragmentationForm, ReportDialog, FragmentationItemList },
  directives: {},
  filters: {
    typeBagFilter(type) {
      return TYPE_BAG_LABELS[type]
    },
    qualityBagFilter(type) {
      return qualityBagKeyValue[type]
    }
  },
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
      titleReport: '',
      tableKey: 0,
      list: null,
      total: null,
      loading: false,
      listLoading: true,
      listExtractionQuery: {
        page: 1,
        limit: 20,
        search: '',
        ordering: '-id'
      },
      qualityBagOptions,
      listQuery: {
        page: 1,
        limit: 20,
        offset: 0,
        search: '',
        ordering: '-id',
        from: 'main',
        date_range: [moment().startOf('month').format('YYYY-MM-DD'), moment().format('YYYY-MM-DD')]
      },
      temp: {
        id: undefined,
        employee: undefined,
        extraction: undefined,
        total_hc: 0,
        weight: 0
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Editando Fraccionamiento',
        create: 'Creando Fraccionamiento',
        view_items: 'Hemocomponentes de Fraccionamiento'
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
  watch: {},
  created() {
    this.getList()
  },
  methods: {
    checkPermission,
    remoteMethod(query) {
      this.listExtractionQuery.search = query
      this.getListExtraction()
    },
    getList() {
      this.listLoading = true
      let tempListQuery = Object.assign({}, this.listQuery)

      tempListQuery = buildBarcodeFilter(tempListQuery, 'extraction__donation__id')

      // important add more one day for filters date with time
      if (tempListQuery.date_range && tempListQuery.date_range.length === 2) {
        tempListQuery.date_range[1] = moment(tempListQuery.date_range[1], 'YYYY-MM-DD').add(1, 'days').format('YYYY-MM-DD')
      }
      tempListQuery = buildRegisterAtFilter(tempListQuery)

      graphqlRequest(
        {
          from: this.$route.name,
          query: fragmentations.list(tempListQuery),
          variables: tempListQuery
        }
      ).then(response => {
        const data = response.data
        this.list = data.fragmentations.results
        this.total = data.fragmentations.totalCount
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
    handleCreate() {
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.temp = null
    },
    handleUpdate(row) {
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.temp = row
    },
    handleShowItems(row) {
      this.dialogStatus = 'view_items'
      this.dialogFormVisible = true
      this.temp = row
    },
    handleCloseForm() {
      this.dialogFormVisible = false
      this.getList()
    },
    handlePrintRoadMap() {
      this.reportDialogVisible = true
      this.reportDialogLoading = true
      this.titleReport = 'HOJA DE RUTA DEL DONANTE'
      printRoadMap().then(
        response => {
          this.pdf = response
          this.reportDialogLoading = false
        }
      )
    }
  }
}
</script>

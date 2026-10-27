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
      <router-link :to="'/distributions/distribution-fast/'">
        <el-button
          v-if="checkPermission(['add_distribution'])"
          class="filter-item"

          style="margin-left: 10px;"
          type="primary"
        >{{ $t('add') }}
        </el-button>
      </router-link>
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
      <el-table-column :label="$t('models.distribution.register_at')" align="center" fixed width="150px">
        <template slot-scope="scope">
          <span>{{ scope.row.register_at | toHumanDatetime }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.distribution.uuid')" align="center" width="100px">
        <template slot-scope="scope">
          {{ scope.row.id }}
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.distribution.is_delivered')" align="center" width="150px">
        <template slot-scope="scope">
          <el-tag :type="getTypeColor(scope.row.status)">{{ scope.row.status | distributionOptionsFilter }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.distribution.medical')" width="220px">
        <template slot-scope="scope">
          <span>{{ scope.row.medical | fullName }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.distribution.institution')" width="220px">
        <template slot-scope="scope">
          <span>{{  scope.row.institution.name }}</span><br>
          <small>{{ scope.row.institution.type | institutionTypeValue }}</small>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.distribution.patient')" width="320px">
        <template slot-scope="scope">
          <span> {{ scope.row.patient | fullName }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="'Cantidad'" align="center" width="90px">
        <template slot-scope="scope">
          <span> {{ scope.row.total_itemfragmentations }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.distribution.type_payment')" align="center" width="130px">
        <template slot-scope="scope">
          <span>{{ scope.row.type_payment | receiptOptionsFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.distribution.employee')" align="center" width="320px">
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
          <el-tooltip v-show="scope.row.total_itemfragmentations>0" :enterable="false" class="item" content="Hemocomponentes" effect="dark">
            <el-button size="mini" type="default" @click="handleUpdateItems(scope.row)">Items</el-button>
          </el-tooltip>
          <el-tooltip v-show="scope.row.status==='DELIVERED'" :content="$t('print')" :enterable="false" class="item" effect="dark">
            <el-button size="mini" type="default" @click="handlePrint(scope.row)"><font-awesome-icon icon="book" /></el-button>
          </el-tooltip>
          <el-tooltip v-show="scope.row.status==='IN_PROGRESS'" :enterable="false" class="item" content="Marcar como entregado" effect="dark">
            <el-button v-if="checkPermission(['change_distribution'])" size="mini" type="success" @click="handleDelivered(scope.row)">
              <font-awesome-icon icon="check" />
            </el-button>
          </el-tooltip>

          <el-button
            v-if="checkPermission(['change_distribution']) && (scope.row.status==='NEW' || scope.row.status==='IN_PROGRESS')"
            @click="handleCommandButtons('modify', scope.row)"
            size="mini"
          >{{ $t('edit') }}
          </el-button>
          <el-button v-if="scope.row.status!=='CANCELED'" @click="handleCommandButtons('cancel', scope.row)"
                     size="mini">
            {{ $t('cancel') }}
          </el-button>

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
      <distribution-form v-if="dialogStatus!=='update_items'" :row="temp" @dialogStatus="handleCloseForm" />
      <distribution-item-list v-if="dialogStatus==='update_items'" :distribution="temp" />
    </el-dialog>

    <el-dialog
      :visible.sync="reportDialogVisible"
      center
      title="Reporte"
      top="10px"
      width="100%"
    >
      <report-dialog v-if="!reportDialogLoading" :row="pdf" @dialogStatus="handleCloseForm" />
      <div v-if="reportDialogLoading" class="loading-report">
        <i class="el-icon-loading" style="font-size: 80px" />
      </div>
    </el-dialog>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import { printDistribution, printDistributionRequestGlobal, printDistributionRequestParticular } from '@/api/distribution'
import ReportDialog from '../report-dialog/ReportDialog'
import DistributionForm from './DistributionForm'
import DistributionItemList from './DistributionItemList'
import { graphqlRequest } from '@/api/graphql'
import distributions from '@/query/distribution'
import { debounce } from 'debounce'
import { defaultshorcouts } from '@/utils/date-utils'
import moment from 'moment'
import { mapGetters } from 'vuex'
import { TYPE_PAYMENT_OPTIONS } from "@/utils/const"

const DistributionOptions = [
  { key: 'NEW', display_name: 'NUEVO', tag_type: 'default' },
  { key: 'IN_PROGRESS', display_name: 'EN PROCESO', tag_type: 'default' },
  { key: 'DELIVERED', display_name: 'ENTREGADO', tag_type: 'success' },
  { key: 'CANCELED', display_name: 'CANCELADO', tag_type: 'info' },
  { key: 'REFUNDED', display_name: 'DEVUELTO', tag_type: 'danger' },
  { key: 'PARTIAL_REFUNDED', display_name: 'PARCIALMENTE DEVUELTO', tag_type: 'warning' }
]

const allOptions = {
  receipts: TYPE_PAYMENT_OPTIONS,
  distributions: DistributionOptions
}

function getValueOptions(list, key) {
  var option = allOptions[list].reduce((acc, cur) => {
    acc[cur.key] = cur.display_name
    return acc
  }, {})
  return option[key]
}

export default {
  name: 'DistributionList',
  components: { ReportDialog, DistributionForm, DistributionItemList },
  directives: {},
  filters: {
    receiptOptionsFilter(type) {
      return getValueOptions('receipts', type)
    },
    distributionOptionsFilter(type) {
      return getValueOptions('distributions', type)
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
      tableKey: 0,
      storages: null,
      storage: null,
      patients: null,
      medicals: null,
      list: null,
      total: null,
      loading: false,
      listLoading: true,
      patientLoading: false,
      medicalLoading: false,
      TYPE_PAYMENT_OPTIONS,
      listQuery: {
        page: 1,
        limit: 20,
        offset: 0,
        search: '',
        ordering: '-id',
        date_range: [moment().startOf('month').format('YYYY-MM-DD'), moment().format('YYYY-MM-DD')] },
      temp: {
        id: undefined,
        employee_id: undefined,
        extraction_id: undefined,
        patient_id: undefined,
        medical_id: undefined
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Editando Distribución',
        update_items: 'Hemocomponentes de Distribución',
        create: 'Creando Distribución'
      },
      rules: {},
      downloadLoading: false,
      totalHC: 0
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
    handleCommand(element) {
      switch (element.option) {
        case 'global':
          this.handlePrintFormGlobal()
          break
        case 'particular':
          this.handlePrintFormParticular()
          break
        default:
      }
    },
    handleCommandButtons(option, row) {
      switch (option) {
        case 'modify':
          this.$router.push({ name: 'distribution-edit', params: { id: row.id }})
          break
        case 'cancel':
          this.handleCancel(row)
          break
        default:
      }
    },
    getList() {
      this.listLoading = true
      const tempListQuery = Object.assign({}, this.listQuery)

      if (tempListQuery.date_range && tempListQuery.date_range.length === 2) {
        tempListQuery.date_range[1] = moment(tempListQuery.date_range[1], 'YYYY-MM-DD').add(1, 'days').format('YYYY-MM-DD')
      }
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'distributions',
          query: distributions.listDistribution(tempListQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.distributions.results
        this.total = data.distributions.totalCount
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
    handlePrint(row) {
      this.reportDialogVisible = true
      this.reportDialogLoading = true
      this.temp = Object.assign({}, row)
      printDistribution(this.temp.id).then(
        response => {
          this.pdf = response
          this.reportDialogLoading = false
        }
      )
    },
    handlePrintFormGlobal() {
      this.reportDialogVisible = true
      this.reportDialogLoading = true
      printDistributionRequestGlobal().then(
        response => {
          this.pdf = response
          this.reportDialogLoading = false
        }
      )
    },
    handlePrintFormParticular() {
      this.reportDialogVisible = true
      this.reportDialogLoading = true
      printDistributionRequestParticular().then(
        response => {
          this.pdf = response
          this.reportDialogLoading = false
        }
      )
    },
    handleCreate() {
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.temp = null
    },
    handleUpdateItems(row) {
      this.dialogStatus = 'update_items'
      this.dialogFormVisible = true
      this.temp = row
    },
    handleCloseForm() {
      this.dialogFormVisible = false
      this.getList()
    },
    handleCancel(row) {
      const tempData = Object.assign({}, row)

      this.$confirm('Está seguro de marcar como CANCELADO?', 'Confirmación', {
        confirmButtonText: 'Si',
        cancelButtonText: 'Cancelar',
        type: 'warning'
      }).then(() => {
        graphqlRequest(
          {
            from: this.$route.name,
            query: distributions.updateDistribution(tempData),
            variables: { id: tempData.id, status: 'CANCELED' }
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
              message: 'Se ha cancelado la distribución',
              type: 'success',
              duration: 2000
            })
          }
        })
      }).catch(() => {})
    },
    handleDelivered(row) {
      const tempData = Object.assign({}, row)
      if (tempData.total_itemfragmentations === 0) {
        this.$notify({
          title: 'Falta Hemocomponentes',
          message: 'Necesitas agregar al menos un Hemocomponente',
          type: 'warning',
          duration: 4000
        })
        return
      }
      this.$confirm('Está seguro de marcar como ENTREGADO?', 'Confirmación', {
        confirmButtonText: 'Si',
        cancelButtonText: 'Cancelar',
        type: 'warning'
      }).then(() => {
        graphqlRequest(
          {
            from: this.$route.name,
            query: distributions.updateDistribution(),
            variables: { id: tempData.id, status: 'DELIVERED' }
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
              message: 'Se ha marcado como entregado',
              type: 'success',
              duration: 2000
            })
          }
        })
      }).catch(() => {})
    },
    getTypeColor(status) {
      var option = allOptions['distributions'].reduce((acc, cur) => {
        acc[cur.key] = cur.tag_type
        return acc
      }, {})
      return option[status]
    }
  }
}
</script>

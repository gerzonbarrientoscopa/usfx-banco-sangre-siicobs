<template>
  <div v-if="row" class="createPost-container">
    <b>{{ row.name }}</b> - {{ row.init_at | toHumanDatetime }} {{ row.end_at | toHumanDatetime }}
    <el-row class="row-bg" justify="space-between" type="flex">
      <el-col :span="18"><h4>Resultados de la Colecta</h4></el-col>
      <el-col :span="3">
        <el-button class="pull-right" icon="el-icon-download" @click="handlePrint()">{{ 'Reporte' }}
        </el-button>
      </el-col>
      <el-col :span="3">
        <el-dropdown size="mini" @command="handleDownloadVolunteer">
          <el-button type="primary">
            Fichas <i class="el-icon-arrow-down el-icon--right" />
          </el-button>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item :command="{option: 'all', row: row}">Todos</el-dropdown-item>
            <el-dropdown-item :command="{option: 'all_only_first_page', row: row}">Todos primera hoja</el-dropdown-item>
            <el-dropdown-item :command="{option: 'extraction_all', row: row}">Donaciones Efectivas Todas las hojas</el-dropdown-item>
            <el-dropdown-item :command="{option: 'extraction_only_first_page', row: row}">Donaciones Efectivas Primera hoja</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </el-col>
    </el-row>
    <br>
    <div class="filter-container">
      <el-input
        v-model.lazy="listQuery.search"
        :autofocus="'autofocus'"
        :placeholder="$t('models.donation.search')"
        class="filter-item"
        clearable
        prefix-icon="el-icon-search"
        @input="handleFilter"
      />
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
      <el-table-column :label="$t('models.donation.register_at')" align="center" fixed width="170px">
        <template slot-scope="scope">
          <span>{{ scope.row.register_at | toHumanDate }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.donor.code')" align="center" width="110px">
        <template slot-scope="scope">
          <strong>{{ scope.row.donor.code }}</strong>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.donor.names')" align="left" width="220px">
        <template slot-scope="scope">
          <span>{{ scope.row.donor | fullName }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.donation.status')" align="center" width="155px">
        <template slot-scope="scope">
          <el-tag :type="getStatus(scope.row)">{{ scope.row | statusFilter }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.donation.type_donation')" align="left" width="200px">
        <template slot-scope="scope">
          <span>{{ scope.row.type_donation | typeDonationFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.donation.place')" align="center" width="155px">
        <template slot-scope="scope">
          <span v-if="scope.row.place">{{ scope.row.place.name }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.donation.last_donation_at')" align="center" width="200px">
        <template slot-scope="scope">
          <span>{{ scope.row.last_donation_at }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.donation.employee')" align="center" width="300">
        <template slot-scope="scope">
          <span>{{ scope.row.employee | fullName }}</span>
        </template>
      </el-table-column>

      <el-table-column
        :label="$t('actions')"
        align="center"
        class-name="small-padding"
        fixed="right"
        width="120"
      >
        <template slot-scope="scope">
          <el-button
            v-if="checkPermission(['change_donation'])"
            size="mini"
            @click.stop.prevent="updateData(scope.row)"
          >
            {{ $t('unassign') }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="pagination-container">
      <el-pagination
        v-show="total>0"
        :current-page="listQuery.page"
        :page-size="listQuery.limit"
        :page-sizes="[10, 20, 30, 50]"
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
      append-to-body
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
import { printDonorTicketVolunteer, printPromotions } from '@/api/event'
import ReportDialog from '../../report-dialog/ReportDialog'
import { graphqlRequest } from '@/api/graphql'
import donations from '@/query/donation'

const typeDonationOptions = [
  { key: 'VA', display_name: 'VOLUNTARIA ALTRUISTA' },
  { key: 'RS', display_name: 'REPOSICION SOLIDARIA' },
  { key: 'RE', display_name: 'REPOSICION EXIGIDA' },
  { key: 'DA', display_name: 'DONACION AUTOLOGA' }
]

const typeDonationKeyValue = typeDonationOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'EventDetail',
  components: { ReportDialog },
  directives: {},
  filters: {
    typeDonationFilter(type) {
      return typeDonationKeyValue[type]
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
    }
  },
  props: {
    row: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      pdf: null,
      downloadLoading: false,
      reportTitle: '',
      reportDialogLoading: false,
      reportDialogVisible: false,
      tableKey: 0,
      list: null,
      listLoading: false,
      total: null,
      listQuery: { page: 1, limit: 10, offset: 0, search: '', ordering: '-donor__code', event_id: undefined }
    }
  },
  watch: {
    row: function() {
      this.listQuery.page = 1
      this.listQuery.offset = 0

      this.determineAction()
    }
  },
  created() {
    this.determineAction()
  },
  methods: {
    checkPermission,
    determineAction() {
      this.getList()
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

    updateData(row) {
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'updateDonation',
          query: donations.updateDonation(),
          variables: { id: row.id, event_id: null }
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
    },
    getList() {
      this.listLoading = true
      this.listQuery.event_id = this.row.id
      graphqlRequest(
        {
          from: this.$route.name,
          query: donations.listForEvent(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.donations.results
        this.total = data.donations.totalCount
        this.listLoading = false
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.listQuery.offset = 0
      this.getList()
    },
    handleSizeChange(val) {
      this.listQuery.limit = val
      this.getList()
    },
    handleCurrentChange(val) {
      this.listQuery.page = val
      this.listQuery.offset = this.listQuery.limit * (val - 1)
      this.getList()
    },
    handlePrint() {
      this.reportDialogVisible = true
      this.reportDialogLoading = true
      this.temp = Object.assign({}, this.row)
      printPromotions(this.temp.id).then(
        response => {
          this.reportTitle = 'Reporte de Donaciones del Evento: ' + this.temp.name
          this.pdf = response
          this.reportDialogLoading = false
        }
      )
    },
    handleDownloadVolunteer(element) {
      this.reportDialogVisible = true
      this.reportDialogLoading = true
      this.temp = Object.assign({}, this.row)
      printDonorTicketVolunteer(this.temp.id, element.option).then(
        response => {
          this.pdf = response
          this.reportDialogLoading = false
        }
      )
    }
  }
}
</script>


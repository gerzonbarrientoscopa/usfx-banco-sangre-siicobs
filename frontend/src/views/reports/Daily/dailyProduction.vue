<template>
  <div class="app-container">
    <div class="filter-container">
      <el-row :gutter="20">
        <el-col :md="16">
          <div class="block">
            <span class="demonstration">Fecha</span>
            <el-date-picker
              v-model="listQuery.extra.date_init"
              :clearable="false"
              :picker-options="pickerOptions"
              format="dd-MM-yyyy"
              placeholder="Fecha Inicial"
              type="date"
              value-format="yyyy-MM-dd"
              @change="handleFilter"
            />
          </div>
        </el-col>
      </el-row>
    </div>
    <div class="filter-container">
      <el-input
        v-model="listQuery.search"
        :autofocus="'autofocus'"
        :placeholder="$t('donors.search')"
        class="filter-item"
        clearable
        prefix-icon="el-icon-search"
        @input="handleFilter"
      />
      <el-button
        :loading="downloadLoading"
        class="filter-item"
        icon="el-icon-download"
        style="margin-left: 10px;"
        type="primary"
        @click="handlePrint"
      >Imprimir
      </el-button>
    </div>
    <div id="print">
      <h1 style="text-align: center">Reporte diario de produccion {{ listQuery.extra.date_init | toHumanDate }}</h1>
      <el-table
        :key="tableKey"
        v-loading="listLoading"
        :data="list"
        :summary-method="getSummaries"
        border
        fit
        highlight-current-row
        show-summary
        stripe
        style="width: 100%;"
      >
        <el-table-column :label="$t('models.report.production.register_at')" align="center">
          <template slot-scope="scope">
            <span v-if="scope.row.release">{{ scope.row.release.register_at | toHumanDate }}</span>
            <span v-if="scope.row.discard">{{ scope.row.discard.register_at | toHumanDate }}</span>
          </template>
        </el-table-column>
        <el-table-column :label="$t('models.donor.code')" align="center" width="110px">
          <template slot-scope="scope">
            <strong>{{ scope.row.donor_code }}</strong>
          </template>
        </el-table-column>
        <el-table-column :label="$t('models.report.fragmentation.type_hemocomponent')" align="center">
          <el-table-column :label="$t('models.report.fragmentation.pg')" align="center" width="60px">
            <template slot-scope="scope">
              <span v-if="scope.row.typehemocomponent.id===1">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.pfc')" align="center" width="60px">
            <template slot-scope="scope">
              <span v-if="scope.row.typehemocomponent.id===2">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.pc')" align="center" width="60px">
            <template slot-scope="scope">
              <span v-if="scope.row.typehemocomponent.id===3">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.crio')" align="center" width="60px">
            <template slot-scope="scope">
              <span v-if="scope.row.typehemocomponent.id===4">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.grl')" align="center" width="60px">
            <template slot-scope="scope">
              <span v-if="scope.row.typehemocomponent.id===5">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.cp')" align="center" width="60px">
            <template slot-scope="scope">
              <span v-if="scope.row.typehemocomponent.id===6">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.cpaf')" align="center" width="60px">
            <template slot-scope="scope">
              <span v-if="scope.row.typehemocomponent.id===7">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.st')" align="center" width="60px">
            <template slot-scope="scope">
              <span v-if="scope.row.typehemocomponent.id===8">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.stped')" align="center" width="60px">
            <template slot-scope="scope">
              <span v-if="scope.row.typehemocomponent.id===9">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.pgped')" align="center" width="60px">
            <template slot-scope="scope">
              <span v-if="scope.row.typehemocomponent.id===10">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.pfcped')" align="center" width="60px">
            <template slot-scope="scope">
              <span v-if="scope.row.typehemocomponent.id===11">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.pcped')" align="center" width="60px">
            <template slot-scope="scope">
              <span v-if="scope.row.typehemocomponent.id===12">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.grlped')" align="center" width="60px">
            <template slot-scope="scope">
              <span v-if="scope.row.typehemocomponent.id===13">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.ec')" align="center" width="60px">
            <template slot-scope="scope">
              <span v-if="scope.row.typehemocomponent.id===15">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.bv')" align="center" width="60px">
            <template slot-scope="scope">
              <span v-if="scope.row.typehemocomponent.id===16">X</span>
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column :label="$t('models.report.production.release')" align="center" width="60px">
          <template slot-scope="scope">
            <span v-if="scope.row.release">X</span>
          </template>
        </el-table-column>
        <el-table-column :label="$t('models.report.production.discard')" align="center" width="60px">
          <template slot-scope="scope">
            <span v-if="scope.row.discard">X</span>
          </template>
        </el-table-column>
      </el-table>
    </div>

  </div>
</template>

<script>
import { graphqlRequest } from '@/api/graphql'
import moment from 'moment/moment'
import itemFragmentations from '@/query/itemFragmentation'
import { debounce } from 'debounce'
import { reportToday } from '@/api/itemFragmentation'

export default {
  name: 'DailyProduction',
  components: { },
  directives: { },
  filters: {},
  data() {
    return {
      pdf: null,
      reportDialogVisible: false,
      reportDialogLoading: false,
      pickerOptions: {
        disabledDate(time) {
          return time.getTime() > Date.now()
        }
      },
      tableKey: 0,
      list: null,
      total: null,
      loading: false,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 200,
        offset: 0,
        search: '',
        ordering: '-id',
        only_event: false,
        extra: {
          date_init: moment().startOf('day').format('YYYY-MM-DD'),
          date_end: moment().add(1, 'days').format('YYYY-MM-DD'),
          gender: '',
          event: '',
          rejected: '',
          etary: '',
          typeDonation: '',
          reasonRejected: ''
        }
      },
      downloadLoading: false,
      reasons: []
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getSummaries(param) {
      const sums = ['Totales', '-', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      for (const l in this.list) {
        if (this.list[l].typehemocomponent.id === 1) sums[2]++
        if (this.list[l].typehemocomponent.id === 2) sums[3]++
        if (this.list[l].typehemocomponent.id === 3) sums[4]++
        if (this.list[l].typehemocomponent.id === 4) sums[5]++
        if (this.list[l].typehemocomponent.id === 5) sums[6]++
        if (this.list[l].typehemocomponent.id === 6) sums[7]++
        if (this.list[l].typehemocomponent.id === 7) sums[8]++
        if (this.list[l].typehemocomponent.id === 8) sums[9]++
        if (this.list[l].typehemocomponent.id === 9) sums[10]++
        if (this.list[l].typehemocomponent.id === 10) sums[11]++
        if (this.list[l].typehemocomponent.id === 11) sums[12]++
        if (this.list[l].typehemocomponent.id === 12) sums[13]++
        if (this.list[l].typehemocomponent.id === 13) sums[14]++
        if (this.list[l].typehemocomponent.id === 15) sums[15]++
        if (this.list[l].typehemocomponent.id === 16) sums[16]++
        if (this.list[l].release) sums[17]++
        if (this.list[l].discard) sums[18]++
      }
      return sums
    },
    getList() {
      this.listLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          query: itemFragmentations.listProductionReport(this.listQuery)
        }
      ).then(response => {
        const data = response.data

        this.list = data.itemfragmentations.results
        this.total = data.itemfragmentations.totalCount
        this.listLoading = false
      })
    },
    handleFilter: debounce(function(e) {
      this.listQuery.extra.date_end = moment(this.listQuery.extra.date_init, 'YYYY-MM-DD').add(0, 'days').format('YYYY-MM-DD')
      this.listQuery.page = 1
      this.listQuery.offset = 0
      this.getList()
    }, 500),

    handleDownload(response, filename) {
      const url = window.URL.createObjectURL(new Blob([response]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', filename)
      document.body.appendChild(link)
      link.click()
    },
    handlePrint() {
      this.$notify({
        title: 'Generando Reporte',
        message: 'Se esta generenando el reporte',
        type: 'success',
        duration: 2000
      })
      const filename = 'Reporte de Producción Diaria ' + moment(this.listQuery.extra.date_init, 'YYYY-MM-DD').format('DD-MM-YYYY') + '.pdf'

      reportToday(this.listQuery).then(
        response => {
          this.handleDownload(response, filename)
        }
      )
    }
  }
}
</script>

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
      <h1 style="text-align: center">Reporte diario de distribucion {{ listQuery.extra.date_init | toHumanDate }}</h1>
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
        <el-table-column :label="$t('models.distribution.register_at')" align="center" width="150px">
          <template slot-scope="scope">
            <span>{{ scope.row.register_at | toHumanDate }}</span>
          </template>
        </el-table-column>
        <el-table-column :label="$t('models.distribution.uuid')" align="center" width="220px">
          <template slot-scope="scope">
            {{ scope.row.uuid }}
          </template>
        </el-table-column>
        <el-table-column :label="$t('models.distribution.patient')" align="center" width="320px">
          <template slot-scope="scope">
            <span> {{ scope.row.patient | fullName }}</span>
          </template>
        </el-table-column>
        <el-table-column :label="$t('models.report.distribution.institution')" align="center" width="320px">
          <template slot-scope="scope">
            <span>{{ scope.row.institution.name }}</span>
          </template>
        </el-table-column>
        <el-table-column :label="$t('models.report.distribution.type_patient')" align="center" width="200px">
          <el-table-column :label="$t('models.report.distribution.particular')" align="center" width="100px">
            <template slot-scope="scope">
              <span v-if="!scope.row.institution">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.distribution.agreement')" align="center" width="100px">
            <template slot-scope="scope">
              <span v-if="scope.row.institution">X</span>
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column :label="$t('models.distribution.type_payment')" align="center" width="200px">
          <el-table-column :label="$t('models.report.distribution.bill')" align="center" width="100px">
            <template slot-scope="scope">
              <span v-if="scope.row.type_payment===0">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.distribution.agreement')" align="center" width="100px">
            <template slot-scope="scope">
              <span v-if="scope.row.type_payment===1">X</span>
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column :label="$t('models.report.distribution.quantity')" align="center" width="320px">
          <template slot-scope="scope">
            <span>{{ scope.row.itemfragmentations.length }}</span>
          </template>
        </el-table-column>
      </el-table>
    </div>

  </div>
</template>

<script>
import { graphqlRequest } from '@/api/graphql'
import moment from 'moment/moment'
import distributions from '@/query/distribution'
import { debounce } from 'debounce'
import { reportToday } from '@/api/distribution'

export default {
  name: 'DailyDistribution',
  components: { },
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
          date_end: moment().add(1, 'days').format('YYYY-MM-DD')
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
      const sums = ['Totales', '-', '-', 0, 0, 0, 0, 0]
      for (const l in this.list) {
        if (!this.list[l].institution) sums[3]++
        if (this.list[l].institution) sums[4]++
        if (this.list[l].type_payment === 0) sums[5]++
        if (this.list[l].type_payment === 1) sums[6]++
        if (this.list[l].itemfragmentations) {
          if (this.list[l].itemfragmentations.length > 0) sums[7] += this.list[l].itemfragmentations.length
        }
      }
      return sums
    },
    getList() {
      this.listLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          query: distributions.reportList(this.listQuery)
        }
      ).then(response => {
        const data = response.data

        this.list = data.distributions.results
        this.total = data.distributions.totalCount
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
      const filename = 'Reporte de Distribución Diaria ' + moment(this.listQuery.extra.date_init, 'YYYY-MM-DD').format('DD-MM-YYYY') + '.pdf'

      reportToday(this.listQuery).then(
        response => {
          this.handleDownload(response, filename)
        }
      )
    }
  }
}
</script>

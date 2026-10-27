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
        <el-col :md="8">
          <div class="block">
            <el-button
              :loading="downloadLoading"
              class="filter-item"
              icon="el-icon-download"
              style="margin-left: 10px;"
              type="primary"
              @click="handlePrint"
            >Imprimir
            </el-button>
          </div></el-col>
      </el-row>
    </div>

    <table-immunoserology :list="list" :loading="listLoading" />

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
  </div>
</template>

<script>
import moment from 'moment/moment'
import { reportToday } from '@/api/immunoserology'
import { graphqlRequest } from '@/api/graphql'
import immunoserologies from '@/query/immunoserology'
import TableImmunoserology from '@/components/Reports/TableImmunoserology'

export default {
  name: 'DailyImmunoserology',
  components: { TableImmunoserology },
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
      list: null,
      total: null,
      loading: false,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
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
    getList() {
      this.listLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          query: immunoserologies.listReport(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.immunoserologies.results
        this.total = data.immunoserologies.totalCount
        this.listLoading = false
      })
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
    handleFilter() {
      this.listQuery.extra.date_end = moment(this.listQuery.extra.date_init, 'YYYY-MM-DD').add(0, 'days').format('YYYY-MM-DD')
      this.getList()
    },
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
      const filename = 'Reporte de Immunoserologia Diaria ' + moment(this.listQuery.extra.date_init, 'YYYY-MM-DD').format('DD-MM-YYYY') + '.pdf'

      reportToday(this.listQuery).then(
        response => {
          this.handleDownload(response, filename)
        }
      )
    }
  }
}
</script>

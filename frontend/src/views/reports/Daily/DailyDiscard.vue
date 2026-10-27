<template>
  <div class="app-container">
    <div class="filter-container">
      <el-row :gutter="20">
        <el-col :md="18">
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
        <el-col :md="6">
          <el-button
            :loading="downloadLoading"
            class="filter-item"
            icon="el-icon-download"
            style="margin-left: 10px;"
            type="primary"
            @click="handlePrint"
          >Imprimir
          </el-button>
        </el-col>
      </el-row>
    </div>

    <table-discard :list="list" :loading="listLoading" />

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
import { printDiscardAct, reportToday } from '@/api/discard'
import { graphqlRequest } from '@/api/graphql'
import discards from '@/query/discard'
import { mapGetters } from 'vuex'
import TableDiscard from '@/components/Reports/TableDiscard'

export default {
  name: 'DailyDiscard',
  components: { TableDiscard },
  directives: {},
  filters: {},
  data() {
    return {
      pdf: null,
      fullscreenLoading: false,
      pickerOptions: {
        disabledDate(time) {
          return time.getTime() > Date.now()
        }
      },
      tableKey: 0,
      list: null,
      total: null,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        offset: 0,
        search: '',
        ordering: '-id',
        only_event: false,
        time: moment(new Date()).format('hh:mm'),
        observer_id: '',
        responsible_id: '',
        administrator_id: '',
        director_id: '',
        extra: {
          date_init: moment().startOf('day').format('YYYY-MM-DD'),
          date_end: moment().add(1, 'days').format('YYYY-MM-DD')
        }
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
    getList() {
      this.listLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          query: discards.listDailyDiscardReport(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.discards.results
        this.total = data.discards.totalCount
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
      const filename = 'Reporte de Descarte Diario ' + moment(this.listQuery.extra.date_init, 'YYYY-MM-DD').format('DD-MM-YYYY') + '.pdf'

      reportToday(this.listQuery).then(
        response => {
          this.handleDownload(response, filename)
        }
      )
    },
    handlePrintAct() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          this.fullscreenLoading = true
          this.$notify({
            title: 'Generando Reporte',
            message: 'Se esta generando el reporte',
            type: 'success',
            duration: 2000
          })
          const filename = 'Acta de Descarte Diario ' + moment(this.listQuery.extra.date_init, 'YYYY-MM-DD').format('DD-MM-YYYY') + '.pdf'

          printDiscardAct(this.listQuery).then(
            response => {
              this.fullscreenLoading = false
              this.handleDownload(response, filename)
            }
          )
        } else {
          this.$notify({
            title: 'Mensaje',
            message: 'Por favor complete el formulario',
            type: 'warning',
            duration: 2000
          })
          return false
        }
      })
    }
  }
}
</script>

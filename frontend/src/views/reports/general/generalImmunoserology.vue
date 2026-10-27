<template>
  <div class="app-container">
    <div class="filter-container">
      <el-row :gutter="20">
        <el-col :md="8">
          <div class="block">
            <span class="demonstration">Fecha Inicial</span>
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
            <span class="demonstration">Fecha Final</span>
            <el-date-picker
              v-model="listQuery.extra.date_end"
              :clearable="false"
              :picker-options="pickerOptions"
              format="dd-MM-yyyy"
              placeholder="Fecha Final"
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
      <el-tooltip :enterable="false" class="filter-item" content="Reporte General de Liberaciones (Resumen)" effect="dark">
        <el-button v-loading.fullscreen.lock="fullscreenLoading" type="default" @click="handlePrintGeneral">
          <font-awesome-icon icon="download" />
        </el-button>
      </el-tooltip>
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
import checkPermission from '@/utils/permission'
import { graphqlRequest } from '@/api/graphql'
import immunoserologies from '@/query/immunoserology'
import { debounce } from 'debounce'
import moment from 'moment'
import { printGeneralImmunoserology } from '@/api/report'
import TableImmunoserology from '@/components/Reports/TableImmunoserology'

export default {
  name: 'GeneralImmunoserology',
  components: { TableImmunoserology },
  data() {
    return {
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
          date_init: moment().startOf('month').format('YYYY-MM-DD'),
          date_end: moment().format('YYYY-MM-DD')
        }
      },
      pdf: null,
      fullscreenLoading: false
    }
  },
  created() {
    this.getList()
  },
  methods: {
    checkPermission,
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
    handleDowload(response, filename) {
      this.fullscreenLoading = false
      const url = window.URL.createObjectURL(new Blob([response]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'report_' + filename + '_' + this.listQuery['extra']['date_init'] + '_to_' + this.listQuery['extra']['date_end'] + '.pdf')
      document.body.appendChild(link)
      link.click()
    },
    handlePrintGeneral() {
      this.fullscreenLoading = true
      this.$notify({
        title: 'Generando Reporte',
        message: 'Se esta generando el reporte',
        type: 'success',
        duration: 2000
      })
      const filename = 'Immunoserologia'

      printGeneralImmunoserology(this.listQuery).then(
        response => {
          this.fullscreenLoading = false
          this.handleDowload(response, filename)
        }
      )
    }
  }
}
</script>

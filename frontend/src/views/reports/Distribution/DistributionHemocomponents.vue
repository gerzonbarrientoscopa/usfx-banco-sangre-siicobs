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
      <el-row :gutter="20" style="width: 100%">
        <el-col :md="8">
          <span class="demonstration">Tipo de Pago</span>
          <div class="block">
            <el-select
              v-model="listQuery.type_payment"
              :placeholder="$t('please_select')"
              class="filter-item"
              clearable
              @change="getList"
            >
              <el-option
                v-for="item in RECEIPT_OPTIONS"
                :key="item.key"
                :label="item.display_name"
                :value="item.key"
              />
            </el-select>
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
      <el-tooltip :enterable="false" class="filter-item" content="Reporte General de Distribucion por Hemocomponentes" effect="dark">
        <el-button v-loading.fullscreen.lock="fullscreenLoading" type="default" @click="handlePrintGeneral">
          <font-awesome-icon icon="download" />
        </el-button>
      </el-tooltip>
    </div>

    <table-distribution-itemfragmentation :list="list" :loading="listLoading" />

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
import distributionItemfragmentations from '@/query/distributionItemFragmentation'
import { debounce } from 'debounce'
import moment from 'moment'
import { printGeneralDistributionItemfragmentation } from '@/api/report'
import { mapGetters } from 'vuex'
import TableDistributionItemfragmentation from '@/components/Reports/TableDistributionItemfragmentation'

export const RECEIPT_OPTIONS = [
  { key: '', display_name: 'TODOS' },
  { key: 0, display_name: 'FACTURA' },
  { key: 1, display_name: 'CONVENIO' }
]

export default {
  name: 'GeneralDistributionItemfragmentation',
  components: { TableDistributionItemfragmentation },
  data() {
    return {
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
        limit: 20,
        offset: 0,
        search: '',
        ordering: '-id',
        only_event: false,
        employee_id: '',
        institution_id: '',
        type_payment: '',
        institution__is_public: '',
        etary: '',
        extra: {
          date_init: moment().startOf('month').format('YYYY-MM-DD'),
          date_end: moment().format('YYYY-MM-DD')
        }
      },
      pdf: null,
      fullscreenLoading: false,
      institutions: null,
      institutionLoading: false,
      listInstitutionQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-id', id: undefined },
      RECEIPT_OPTIONS
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
    getList() {
      this.listLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          query: distributionItemfragmentations.listReport(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.distribution_itemfragmentations.results
        this.total = data.distribution_itemfragmentations.totalCount
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
      const filename = 'distribution de hemocomponentes'

      printGeneralDistributionItemfragmentation(this.listQuery).then(
        response => {
          this.fullscreenLoading = false
          this.handleDowload(response, filename)
        }
      )
    }
  }
}
</script>

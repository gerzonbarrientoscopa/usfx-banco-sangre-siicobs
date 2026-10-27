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
          <span class="demonstration">Responsable:</span>
          <div class="block">
            <el-select
              v-model="listQuery.employee_id"
              :placeholder="$t('please_select')"
              automatic-dropdown
              class="filter-item"
              clearable
              filterable
              @change="getList"
            >
              <el-option
                v-for="item in employees"
                :key="item.id"
                :label="item.first_name +' '+ item.middle_name +' '+ item.last_name "
                :value="item.id"
              />
            </el-select>
          </div>
        </el-col>
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
                v-for="item in TYPE_PAYMENT_OPTIONS"
                :key="item.key"
                :label="item.display_name"
                :value="item.key"
              />
            </el-select>
          </div>
        </el-col>
        <el-col :md="8">
          <span class="demonstration">Grupo Etario</span>
          <div class="block">
            <el-select v-model="listQuery.etary" clearable placeholder="Por favor seleccione" @change="handleFilter">
              <el-option
                v-for="item in [{value: '', label: 'Todos'}, {value: '18-25', label: '18-25'}, {value: '26-30', label: '26-30'} , {value: '31-40', label: '31-40'}, {value: '41-50', label: '41-50'}, {value: '51-60', label: '51-60'}, {value: '61-65', label: '61-65'} ]"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>
        </el-col>
      </el-row>
    </div>
    <div class="filter-container">
      <el-row :gutter="20" style="width: 100%">
        <el-col :md="8">
          <span class="demonstration">Institución</span>
          <div class="block">
            <el-select
              v-model="listQuery.institution_id"
              :loading="institutionLoading"
              :placeholder="$t('please_select')"
              :remote-method="remoteMethodInstitution"
              automatic-dropdown
              class="filter-item"
              clearable
              filterable
              remote
              @change="getList"
            >
              <el-option
                v-for="item in institutions"
                :key="item.id"
                :label="item.name"
                :value="item.id"
              />
            </el-select>
          </div>
        </el-col>
        <el-col :md="8">
          <span class="demonstration">Tipo de Institución</span>
          <div class="block">
            <el-select
              v-model="listQuery.institution__type"
              :placeholder="$t('please_select')"
              class="filter-item"
              clearable
              @change="getList"
            >
              <el-option
                v-for="item in INSTITUTION_TYPE_OPTIONS"
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
      <el-tooltip :enterable="false" class="filter-item" content="Reporte General de Distribuciones" effect="dark">
        <el-button v-loading.fullscreen.lock="fullscreenLoading" type="default" @click="handlePrintGeneral">
          <font-awesome-icon icon="download" />
        </el-button>
      </el-tooltip>
    </div>

    <table-distribution :list="list" :loading="listLoading" />

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
import distributions from '@/query/distribution'
import { debounce } from 'debounce'
import moment from 'moment'
import { printGeneralDistribution } from '@/api/report'
import { mapGetters } from 'vuex'
import institutions from '@/query/institution'
import TableDistribution from '@/components/Reports/TableDistribution'
import {INSTITUTION_TYPE_OPTIONS, RECEIPT_OPTIONS, TYPE_PAYMENT_OPTIONS} from '@/utils/const'

export default {
  name: 'GeneralDistribution',
  components: { TableDistribution },
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
      INSTITUTION_TYPE_OPTIONS,
      TYPE_PAYMENT_OPTIONS
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
    this.getListInstitutions()
  },
  methods: {
    checkPermission,
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
    getListInstitutions() {
      this.institutionLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'institutions',
          query: institutions.distribution_select(this.listInstitutionQuery)
        }
      ).then(response => {
        const data = response.data
        this.institutions = data.institutions.results
        this.institutionLoading = false
      })
    },
    remoteMethodInstitution(query) {
      if (query !== '') {
        this.listInstitutionQuery.search = query
      } else {
        this.listInstitutionQuery.search = ''
      }
      this.getListInstitutions()
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
      const filename = 'distribution'

      printGeneralDistribution(this.listQuery).then(
        response => {
          this.fullscreenLoading = false
          this.handleDowload(response, filename)
        }
      )
    }
  }
}
</script>

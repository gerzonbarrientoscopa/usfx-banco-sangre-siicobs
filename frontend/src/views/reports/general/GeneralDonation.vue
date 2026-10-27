<template>
  <div class="app-container">
    <div class="filter-container">
      <el-row :gutter="20">
        <el-col :md="6">
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
        <el-col :md="6">
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
        <el-col :md="6">
          <span class="demonstration">Intencion de Donación</span>
          <el-select v-model="listQuery.extra.extraction" placeholder="Select" @change="handleFilter">
            <el-option
              v-for="item in [{value: '', label: 'Todos'}, {value: '0', label: 'No Efectiva'}, {value: '1', label: 'Efectiva'} ]"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-col>
        <el-col v-if="listQuery.extra.extraction === '1'" :md="6">
          <span class="demonstration">Auto Excluido</span>
          <el-select v-model="listQuery.extra.selfexclusion" placeholder="Select" @change="handleFilter">
            <el-option
              v-for="item in [{value: '', label: 'Todos'}, {value: '0', label: 'No'}, {value: '1', label: 'Si'} ]"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-col>
        <el-col v-if="listQuery.extra.extraction === '1'" :md="6">
          <span class="demonstration">Extracción Fallida</span>
          <el-select v-model="listQuery.extra.adversereaction" placeholder="Select" @change="handleFilter">
            <el-option
              v-for="item in [{value: '', label: 'Todos'}, {value: '0', label: 'No'}, {value: '1', label: 'Si'} ]"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-col>
        <el-col :md="6">
          <span class="demonstration">Colectas</span>
          <el-select v-model="listQuery.extra.event" placeholder="Select" @change="handleFilter">
            <el-option
              v-for="item in [{value: '', label: 'Todos'}, {value: '0', label: 'Internas'}, {value: '1', label: 'Externas'} ]"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-col>
        <el-col :md="8">
          <span class="demonstration">Tipo de Donación</span>
          <el-select v-model="listQuery.extra.typeDonation" placeholder="Select" @change="handleFilter">
            <el-option
              v-for="item in typeDonationOptions"
              :key="item.key"
              :label="item.display_name"
              :value="item.key"
            />
          </el-select>
        </el-col>
        <el-col :md="8">
          <span class="demonstration">Tipo de Procedimiento</span>
          <el-select v-model="listQuery.extra.typeProcess" placeholder="Select" @change="handleFilter">
            <el-option
              v-for="item in typeProcessOptions"
              :key="item.key"
              :label="item.display_name"
              :value="item.key"
            />
          </el-select>
        </el-col>
        <el-col :md="6">
          <span class="demonstration">Género</span>
          <el-select v-model="listQuery.extra.gender" placeholder="Select" @change="handleFilter">
            <el-option
              v-for="item in [{value: '', label: 'Todos'}, {value: 'F', label: 'Femenino'}, {value: 'M', label: 'Masculino'} ]"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-col>
        <el-col :md="8">
          <span class="demonstration">Grupo Etario</span>
          <el-select v-model="listQuery.extra.etary" placeholder="Select" @change="handleFilter">
            <el-option
              v-for="item in [{value: '', label: 'Todos'}, {value: '18-25', label: '18-25'}, {value: '26-30', label: '26-30'} , {value: '31-40', label: '31-40'}, {value: '41-50', label: '41-50'}, {value: '51-60', label: '51-60'}, {value: '61-65', label: '61-65'} ]"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-col>
        <el-col :md="8">
          <span class="demonstration">Diferidos</span>
          <el-select v-model="listQuery.extra.rejected" placeholder="Select" @change="handleFilter">
            <el-option
              v-for="item in [{value: '', label: 'Todos'}, {value: '0', label: 'Todos los No Diferidos'}, {value: '1', label: 'Todos los Diferidos'}, {value: '2', label: 'Diferidos Temporales'}, {value: '3', label: 'Diferidos Permanentes'} ]"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-col>
        <el-col v-if="listQuery.extra.rejected === '1'" :md="8">
          <span class="demonstration">Razon de diferimiento</span>
          <el-select v-model="listQuery.extra.reasonRejected" clearable placeholder="Select" @change="handleFilter">
            <el-option
              v-for="item in reasons"
              :key="item.id"
              :label="'[' + item.type + '] ' + item.name"
              :value="item.id"
            />
          </el-select>
        </el-col>

        <el-col :md="8">
          <span class="demonstration">&nbsp;</span>
          <br>
          <el-button type="default" @click="resetFilters">Eliminar Filtros</el-button>
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
      <el-tooltip :enterable="false" class="filter-item" content="Reporte General" effect="dark">
        <el-button v-loading.fullscreen.lock="fullscreenLoading" type="default" @click="handlePrint">
          <font-awesome-icon icon="download" />
        </el-button>
      </el-tooltip>
<!--      <el-tooltip :enterable="false" class="filter-item" content="Reporte General de Donaciones" effect="dark">-->
<!--        <el-button v-loading.fullscreen.lock="fullscreenLoading" @click="handlePrintDonation">-->
<!--          <font-awesome-icon icon="download" />-->
<!--        </el-button>-->
<!--      </el-tooltip>-->
<!--      <el-tooltip :enterable="false" class="filter-item" content="Reporte General de Pre-Tamizaje" effect="dark">-->
<!--        <el-button v-loading.fullscreen.lock="fullscreenLoading" @click="handlePrintExam">-->
<!--          <font-awesome-icon icon="download" />-->
<!--        </el-button>-->
<!--      </el-tooltip>-->
<!--      <el-tooltip :enterable="false" class="filter-item" content="Reporte General de Analisis Fisico" effect="dark">-->
<!--        <el-button v-loading.fullscreen.lock="fullscreenLoading" type="success" @click="handlePrintPhysicalAnalysis">-->
<!--          <font-awesome-icon icon="download" />-->
<!--        </el-button>-->
<!--      </el-tooltip>-->
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      stripe
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
      <el-table-column :label="$t('models.donation.type_process')" align="left" width="200px">
        <template slot-scope="scope">
          <span>{{ scope.row.type_process | typeProcessFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.donation.event')" align="left" width="200px">
        <template slot-scope="scope">
          <span v-if="scope.row.event">{{ scope.row.event.name }}</span>
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
  </div>
</template>

<script>
import {
  printReportGeneral,
  printReportGeneralDonation,
  printReportGeneralExam,
  printReportGeneralPhysicalAnalysis
} from '@/api/report'
import { graphqlRequest } from '@/api/graphql'
import moment from 'moment'
import donations from '@/query/donation'
import reasons from '@/query/reason'
import { debounce } from 'debounce'

const typeDonationOptions = [
  { key: '', display_name: 'Todos' },
  { key: 'VA', display_name: 'VOLUNTARIA ALTRUISTA' },
  { key: 'RS', display_name: 'REPOSICION SOLIDARIA' },
  { key: 'RE', display_name: 'REPOSICION EXIGIDA' },
  { key: 'DA', display_name: 'DONACION AUTOLOGA' }
]

const typeProcessOptions = [
  { key: '', display_name: 'Todos' },
  { key: 'NO', display_name: 'NORMAL' },
  { key: 'NA', display_name: 'AFERESIS NORMAL' },
]

const statusOptions = [
  { key: 'NU', display_name: 'NUEVO' },
  { key: 'EP', display_name: 'EN PROCESO' },
  { key: 'CO', display_name: 'COMPLETADO' },
  { key: 'RE', display_name: 'DIFERIDO' }
]

const typeDonationKeyValue = typeDonationOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

const typeProcessKeyValue = typeProcessOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'DonationList',
  components: {},
  directives: {},
  filters: {
    typeDonationFilter(type) {
      return typeDonationKeyValue[type]
    },
    typeProcessFilter(type) {
      return typeProcessKeyValue[type]
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
      listQueryReason: { page: 1, limit: 20, offset: 0, search: '', ordering: 'type,name' },
      listQuery: {
        page: 1,
        limit: 20,
        offset: 0,
        search: '',
        ordering: '-id',
        only_event: false,
        extra: {
          date_init: moment().startOf('month').format('YYYY-MM-DD'),
          date_end: moment().format('YYYY-MM-DD'),
          gender: '',
          event: '',
          selfexclusion: '',
          extraction: '',
          rejected: '',
          etary: '',
          typeDonation: '',
          typeProcess: '',
          reasonRejected: '',
          adversereaction: ''
        }
      },
      typeDonationOptions,
      typeProcessOptions,
      statusOptions,
      reasons: [],
      dialogStatus: '',
      textMap: {
        general: 'REPORTE GENERAL',
        donation: 'REPORTE DE DONACIONES',
        exam: 'REPORTE DE PRE-TAMIZAJE',
        physicalAnalysis: 'REPORTE DE ANALISIS FISICO'
      },
      fullscreenLoading: false
    }
  },
  created() {
    this.getList()
    this.getListReasons()
  },
  methods: {
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
    resetFilters() {
      const date_init_temp = this.listQuery.extra.date_init
      const date_end_temp = this.listQuery.extra.date_end

      this.listQuery.extra = {
        date_init: date_init_temp,
        date_end: date_end_temp,
        gender: '',
        event: '',
        selfexclusion: '',
        extraction: '',
        rejected: '',
        etary: '',
        typeDonation: '',
        typeProcess: '',
        reasonRejected: '',
        adversereaction: ''
      }
      this.handleFilter()
    },
    getList() {
      this.listLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          query: donations.report(this.listQuery)
        }
      ).then(response => {
        const data = response.data

        this.list = data.donations.results
        this.total = data.donations.totalCount
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
    getListReasons() {
      graphqlRequest(
        {
          from: this.$route.name,
          query: reasons.list(this.listQueryReason)
        }
      ).then(response => {
        const data = response.data
        this.reasons = data.reasons.results
      })
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
    handlePrint() {
      this.fullscreenLoading = true
      this.$notify({
        title: 'Generando Reporte',
        message: 'Se esta generenando el reporte',
        type: 'success',
        duration: 2000
      })
      const filename = 'general'

      printReportGeneral(this.listQuery).then(
        response => {
          this.fullscreenLoading = false
          this.handleDowload(response, filename)
        }
      )
    },
    handlePrintDonation() {
      this.fullscreenLoading = true
      this.$notify({
        title: 'Generando Reporte',
        message: 'Se esta generenando el reporte',
        type: 'success',
        duration: 2000
      })
      const filename = 'exam'

      printReportGeneralDonation(this.listQuery).then(
        response => {
          this.fullscreenLoading = false
          this.handleDowload(response, filename)
        }
      )
    },
    handlePrintExam() {
      this.fullscreenLoading = true
      this.$notify({
        title: 'Generando Reporte',
        message: 'Se esta generenando el reporte',
        type: 'success',
        duration: 2000
      })
      const filename = 'exam'

      printReportGeneralExam(this.listQuery).then(
        response => {
          this.fullscreenLoading = false
          this.handleDowload(response, filename)
        }
      )
    },
    handlePrintPhysicalAnalysis() {
      this.fullscreenLoading = true
      this.$notify({
        title: 'Generando Reporte',
        message: 'Se esta generenando el reporte',
        type: 'success',
        duration: 2000
      })
      const filename = 'physicalAnalysis'
      printReportGeneralPhysicalAnalysis(this.listQuery).then(
        response => {
          this.fullscreenLoading = false
          this.handleDowload(response, filename)
        }
      )
    }
  }
}
</script>

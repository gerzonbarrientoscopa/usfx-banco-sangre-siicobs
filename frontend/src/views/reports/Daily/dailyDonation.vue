<template>
  <div class="app-container">
    <div class="filter-container">
      <el-row :gutter="20">
        <el-col :md="10">
          <div class="block">
            <span class="demonstration">Fecha</span>
            <el-date-picker
              v-model="listQuery.extra.date_init"
              :clearable="false"
              :picker-options="pickerOptions"
              format="dd-MM-yyyy"
              placeholder="Fecha"
              type="date"
              value-format="yyyy-MM-dd"
              @change="handleFilter"
            />
          </div>
        </el-col>
        <el-col :md="8">
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
      <h1 style="text-align: center">Reporte diario de donaciones {{ listQuery.extra.date_init | toHumanDate }}</h1>
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
        <el-table-column :label="'Fecha'" align="center" fixed width="100px">
          <template slot-scope="scope">
            <span>{{ scope.row.register_at | toHumanDate }}</span>
          </template>
        </el-table-column>
        <el-table-column :label="$t('models.donor.code')" align="center" width="70px">
          <template slot-scope="scope">
            <strong>{{ scope.row.donor.code }}</strong>
          </template>
        </el-table-column>
        <el-table-column :label="'Género'" align="center">
          <el-table-column :label="$t('models.report.male')" align="center" prop="donor" width="40px">
            <template slot-scope="scope">
              <span v-if="scope.row.donor.gender==='M'">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.female')" align="center" prop="donor.gender" width="40px">
            <template slot-scope="scope">
              <span v-if="scope.row.donor.gender==='F'">X</span>
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column :label="'Estado Donación'" align="center">
          <el-table-column :label="$t('models.report.daily.effective')" align="center" width="75px">
            <template slot-scope="scope">
              <span v-if="scope.row.extraction">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.daily.differed')" align="center" width="75px">
            <template slot-scope="scope">
              <span v-if="!scope.row.extraction">X</span>
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column :label="$t('models.report.daily.group_etary')" align="center">
          <el-table-column :label="$t('models.report.ge18')" align="center" width="60px">
            <template slot-scope="scope">
              <span v-if="scope.row.donor.age<26">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.ge26')" align="center" width="60px">
            <template slot-scope="scope">
              <span v-if="scope.row.donor.age<31 && scope.row.donor.age>25">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.ge31')" align="center" width="60px">
            <template slot-scope="scope">
              <span v-if="scope.row.donor.age<41 && scope.row.donor.age>30">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.ge41')" align="center" width="60px">
            <template slot-scope="scope">
              <span v-if="scope.row.donor.age<51 && scope.row.donor.age>40">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.ge51')" align="center" width="60px">
            <template slot-scope="scope">
              <span v-if="scope.row.donor.age<61 && scope.row.donor.age>50">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.ge61')" align="center" width="60px">
            <template slot-scope="scope">
              <span v-if="scope.row.donor.age>60">X</span>
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column :label="$t('models.report.daily.type_donation')" align="center">
          <el-table-column :label="$t('models.report.altruist_volunteer')" align="center" width="50px">
            <template slot-scope="scope">
              <span v-if="scope.row.type_donation==='VA'">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.solidary_replacement')" align="center" width="50px">
            <template slot-scope="scope">
              <span v-if="scope.row.type_donation==='RS'">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.replacement_required')" align="center" width="50px">
            <template slot-scope="scope">
              <span v-if="scope.row.type_donation==='RE'">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.autonomous_donation')" align="center" width="50px">
            <template slot-scope="scope">
              <span v-if="scope.row.type_donation==='DA'">X</span>
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column :label="'Pruebas/Uso Reactivo'" align="center">
          <el-table-column :label="'HTTO'" align="center" width="50px">
            <template slot-scope="scope">
              <span v-if="scope.row.exam.hematocrit">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="'GRUPO'" align="center" width="50px">
            <template slot-scope="scope">
              <span v-if="scope.row.exam.blood_group">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="'RPR'" align="center" width="50px">
            <template slot-scope="scope">
              <span v-if="scope.row.exam.rpr">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="'CHAGAS HAI'" align="center" width="50px">
            <template slot-scope="scope">
              <span v-if="scope.row.exam.chagas">X</span>
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column :label="'Diferimientos'" align="center">
          <el-table-column :label="'Pre-Tamizaje'" align="center" width="50px">
            <template slot-scope="scope">
              <span v-if="scope.row.rejected && scope.row.rejected.resource === 'Exam'">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="'Tamizaje'" align="center" width="50px">
            <template slot-scope="scope">
              <span v-if="scope.row.rejected && scope.row.rejected.resource === 'PhysicalAnalysis'">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="'Historia'" align="center" width="50px">
            <template slot-scope="scope">
              <span v-if="scope.row.rejected && scope.row.rejected.resource === 'ClinicalHistory'">X</span>
            </template>
          </el-table-column>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import { graphqlRequest } from '@/api/graphql'
import moment from 'moment'
import donations from '@/query/donation'
import { debounce } from 'debounce'
import { reportToday } from '@/api/donation'

export default {
  name: 'DailyDonation',
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
        ordering: '-donor__code',
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
      const { columns, data } = param
      const sums = []
      columns.forEach((column, index) => {
        if (index === 0) {
          sums[index] = 'Totales'
          return
        } else {
          sums[index] = 0
        }
      })
      if (data) {
        data.forEach((item, index) => {
          if (data[index].donor) sums[1]++
          if (data[index].donor.gender === 'M') sums[2]++
          if (data[index].donor.gender === 'F') sums[3]++
          if (data[index].extraction) sums[4]++
          if (!data[index].extraction) sums[5]++
          if (data[index].donor.age < 26) sums[6]++
          if (data[index].donor.age > 26 && data[index].donor.age < 31) sums[7]++
          if (data[index].donor.age > 30 && data[index].donor.age < 41) sums[8]++
          if (data[index].donor.age > 40 && data[index].donor.age < 51) sums[9]++
          if (data[index].donor.age > 50 && data[index].donor.age < 61) sums[10]++
          if (data[index].donor.age > 61) sums[11]++
          if (data[index].type_donation === 'VA') sums[12]++
          if (data[index].type_donation === 'RS') sums[13]++
          if (data[index].type_donation === 'RE') sums[14]++
          if (data[index].type_donation === 'DA') sums[15]++
          if (data[index].exam.hematocrit) sums[16]++
          if (data[index].exam.blood_group) sums[17]++
          if (data[index].exam.rpr) sums[18]++
          if (data[index].exam.chagas) sums[19]++
          if (data[index].rejected && data[index].rejected.resource === 'Exam') sums[20]++
          if (data[index].rejected && data[index].rejected.resource === 'PhysicalAnaysis') sums[21]++
          if (data[index].rejected && data[index].rejected.resource === 'ClinicalHistory') sums[22]++
        })
      }

      return sums
    },
    getList() {
      this.listLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          query: donations.reportDailyDonation(this.listQuery)
        }
      ).then(response => {
        const data = response.data

        this.list = data.donations.results
        this.total = data.donations.totalCount
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
      const filename = 'Reporte de Donación Diaria ' + moment(this.listQuery.extra.date_init, 'YYYY-MM-DD').format('DD-MM-YYYY') + '.pdf'

      reportToday(this.listQuery).then(
        response => {
          this.handleDownload(response, filename)
        }
      )
    }
  }
}
</script>

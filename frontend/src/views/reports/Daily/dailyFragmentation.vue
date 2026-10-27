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
          <span class="demonstration">Responsable</span>
          <el-select
            v-model="listQuery.extra.employee_id"
            :placeholder="$t('please_select')"
            automatic-dropdown
            class="filter-item"
            clearable
            filterable
            @change="handleFilter"
          >
            <el-option
              v-for="item in employees"
              :key="item.id"
              :label="item.first_name +' '+ item.middle_name +' '+ item.last_name "
              :value="item.id"
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
      <h1 style="text-align: center">Reporte diario de fraccionamiento {{ listQuery.extra.date_init | toHumanDate }}</h1>
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
        <el-table-column :label="$t('models.donor.register_at')" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.extraction.donation.register_at | toHumanDate }}</span>
          </template>
        </el-table-column>
        <el-table-column :label="$t('models.donor.code')" align="center" width="110px">
          <template slot-scope="scope">
            <strong>{{ scope.row.extraction.donation.donor.code }}</strong>
          </template>
        </el-table-column>
        <el-table-column :label="$t('models.report.fragmentation.type_bag')" align="center">
          <el-table-column :label="$t('models.report.fragmentation.simple')" align="center" width="100px">
            <template slot-scope="scope">
              <span v-if="scope.row.extraction.bags_quantity===1">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.double')" align="center" width="100px">
            <template slot-scope="scope">
              <span v-if="scope.row.extraction.bags_quantity===2">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.triple')" align="center" width="100px">
            <template slot-scope="scope">
              <span v-if="scope.row.extraction.bags_quantity===3">X</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.quadruple')" align="center" width="100px">
            <template slot-scope="scope">
              <span v-if="scope.row.extraction.bags_quantity===4">X</span>
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column :label="$t('models.report.fragmentation.type_hemocomponent')" align="center">
          <el-table-column :label="$t('models.report.fragmentation.pg')" align="center" width="60px">
            <template slot-scope="scope">
              <span>{{ isTypeHecomponent(scope.row.itemfragmentations, 1) }}</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.pfc')" align="center" width="60px">
            <template slot-scope="scope">
              <span>{{ isTypeHecomponent(scope.row.itemfragmentations, 2) }}</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.pc')" align="center" width="60px">
            <template slot-scope="scope">
              <span>{{ isTypeHecomponent(scope.row.itemfragmentations, 3) }}</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.crio')" align="center" width="60px">
            <template slot-scope="scope">
              <span>{{ isTypeHecomponent(scope.row.itemfragmentations, 4) }}</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.grl')" align="center" width="60px">
            <template slot-scope="scope">
              <span>{{ isTypeHecomponent(scope.row.itemfragmentations, 5) }}</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.cp')" align="center" width="60px">
            <template slot-scope="scope">
              <span>{{ isTypeHecomponent(scope.row.itemfragmentations, 6) }}</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.cpaf')" align="center" width="60px">
            <template slot-scope="scope">
              <span>{{ isTypeHecomponent(scope.row.itemfragmentations, 7) }}</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.st')" align="center" width="60px">
            <template slot-scope="scope">
              <span>{{ isTypeHecomponent(scope.row.itemfragmentations, 8) }}</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.stped')" align="center" width="60px">
            <template slot-scope="scope">
              <span>{{ isTypeHecomponent(scope.row.itemfragmentations, 9) }}</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.pgped')" align="center" width="60px">
            <template slot-scope="scope">
              <span>{{ isTypeHecomponent(scope.row.itemfragmentations, 10) }}</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.pfcped')" align="center" width="60px">
            <template slot-scope="scope">
              <span>{{ isTypeHecomponent(scope.row.itemfragmentations, 11) }}</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.pcped')" align="center" width="60px">
            <template slot-scope="scope">
              <span>{{ isTypeHecomponent(scope.row.itemfragmentations, 12) }}</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.grlped')" align="center" width="60px">
            <template slot-scope="scope">
              <span>{{ isTypeHecomponent(scope.row.itemfragmentations, 13) }}</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.ec')" align="center" width="60px">
            <template slot-scope="scope">
              <span>{{ isTypeHecomponent(scope.row.itemfragmentations, 15) }}</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.report.fragmentation.bv')" align="center" width="60px">
            <template slot-scope="scope">
              <span>{{ isTypeHecomponent(scope.row.itemfragmentations, 16) }}</span>
            </template>
          </el-table-column>
        </el-table-column>
      </el-table>
    </div>

  </div>
</template>

<script>
import { graphqlRequest } from '@/api/graphql'
import moment from 'moment/moment'
import fragmentations from '@/query/fragmentation'
import { debounce } from 'debounce'
import { mapGetters } from 'vuex'
import { reportToday } from '@/api/fragmentation'

export default {
  name: 'DailyFragmentation',
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
          employee_id: ''
        }
      },
      downloadLoading: false,
      reasons: []
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
    getSummaries(param) {
      const sums = ['Totales', '-', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      for (const l in this.list) {
        if (this.list[l].extraction.bags_quantity === 1) sums[2]++
        if (this.list[l].extraction.bags_quantity === 2) sums[3]++
        if (this.list[l].extraction.bags_quantity === 3) sums[4]++
        if (this.list[l].extraction.bags_quantity === 4) sums[5]++

        if (this.isTypeHecomponent(this.list[l].itemfragmentations, 1, true)) sums[6]++
        if (this.isTypeHecomponent(this.list[l].itemfragmentations, 2, true)) sums[7]++
        if (this.isTypeHecomponent(this.list[l].itemfragmentations, 3, true)) sums[8]++
        if (this.isTypeHecomponent(this.list[l].itemfragmentations, 4, true)) sums[9]++
        if (this.isTypeHecomponent(this.list[l].itemfragmentations, 5, true)) sums[10]++
        if (this.isTypeHecomponent(this.list[l].itemfragmentations, 6, true)) sums[11]++
        if (this.isTypeHecomponent(this.list[l].itemfragmentations, 7, true)) sums[12]++
        if (this.isTypeHecomponent(this.list[l].itemfragmentations, 8, true)) sums[13]++
        if (this.isTypeHecomponent(this.list[l].itemfragmentations, 9, true)) sums[14]++
        if (this.isTypeHecomponent(this.list[l].itemfragmentations, 10, true)) sums[15]++
        if (this.isTypeHecomponent(this.list[l].itemfragmentations, 11, true)) sums[16]++
        if (this.isTypeHecomponent(this.list[l].itemfragmentations, 12, true)) sums[17]++
        if (this.isTypeHecomponent(this.list[l].itemfragmentations, 13, true)) sums[18]++
        if (this.isTypeHecomponent(this.list[l].itemfragmentations, 15, true)) sums[19]++
        if (this.isTypeHecomponent(this.list[l].itemfragmentations, 16, true)) sums[20]++
      }
      return sums
    },
    getList() {
      this.listLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          query: fragmentations.listReportFragmentation(this.listQuery)
        }
      ).then(response => {
        const data = response.data

        this.list = data.fragmentations.results
        this.total = data.fragmentations.totalCount
        this.listLoading = false
      })
    },
    handleFilter: debounce(function(e) {
      this.listQuery.extra.date_end = moment(this.listQuery.extra.date_init, 'YYYY-MM-DD').add(1, 'days').format('YYYY-MM-DD')
      this.listQuery.page = 1
      this.listQuery.offset = 0
      this.getList()
    }, 500),
    isTypeHecomponent(items, id, number) {
      let string = ''
      items.forEach(function(value, index) {
        if (value.typehemocomponent.id === id) {
          string += 'X'
        }
      })
      if (number) {
        return string.length
      }
      return string
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
      const filename = 'Reporte de Fraccionamiento Diaria ' + moment(this.listQuery.extra.date_init, 'YYYY-MM-DD').format('DD-MM-YYYY') + '.pdf'

      reportToday(this.listQuery).then(
        response => {
          this.handleDownload(response, filename)
        }
      )
    }
  }
}
</script>

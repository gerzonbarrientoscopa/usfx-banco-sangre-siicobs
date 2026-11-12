<template>
  <div class="app-container">
    <div class="filter-container">
      <el-row :gutter="20">
        <el-col :md="8">
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
            <span class="demonstration">Hemocomponente</span>
            <el-select
              v-model="listQuery.typehemocomponent_id"
              filterable
              @change="handleFilter"
            >
              <el-option label="Todos" value="all" />
              <el-option
                v-for="item in typeHemocomponents"
                :key="item.id"
                :label="item.name"
                :value="item.id"
              >
                <span style="float: left">{{ item.name }}</span>
                <span style="float: right; color: #8492a6; font-size: 13px">{{ item.acronym }}</span>
              </el-option>
            </el-select>
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

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      :default-sort="{prop: 'register_at', order: 'descending'}"
      border
      fit
      highlight-current-row
      style="width: 100%;"
    >
      <el-table-column
        :label="$t('models.release.register_at')"
        align="center"
        fixed
        prop="register_at"
        sortable="custom"
        width="100px"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.register_at | toHumanDate }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.release.code')" align="center" width="100px">
        <template slot-scope="scope">
          <span>
            <strong>{{ scope.row.itemfragmentation.donor_code }}</strong>
          </span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.release.hemocomponent')" align="center" width="255px">
        <template slot-scope="scope">
          <span>{{ scope.row.itemfragmentation.typehemocomponent.name }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.release.extraction_date')" align="center" width="160px">
        <template slot-scope="scope">
          <span>{{ scope.row.itemfragmentation.fragmentation.extraction.register_at | toHumanDate }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.release.expiration_date')" align="center" width="160px">
        <template slot-scope="scope">
          <span>{{ scope.row.itemfragmentation.expiration_date | toHumanDate }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.release.observations')" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.observations }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.release.employee')" align="center">
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
import moment from 'moment/moment'
import { reportToday } from '@/api/release'
import { graphqlRequest } from '@/api/graphql'
import releases from '@/query/release'
import typehemocomponents from '@/query/type-hemocomponent'

export default {
  name: 'DailyRelease',
  components: {},
  directives: {},
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
        limit: 20,
        offset: 0,
        search: '',
        ordering: '-id',
        only_event: false,
        typehemocomponent_id: 'all',
        extra: {
          date_init: moment().startOf('day').format('YYYY-MM-DD'),
          date_end: moment().add(1, 'days').format('YYYY-MM-DD')
        }
      },
      downloadLoading: false,
      reasons: [],
      typeHemocomponents: [],
      listTypeHemocomponentQuery: {
        page: 1,
        limit: 100,
        offset: 0,
        search: '',
        ordering: 'position,name'
      }
    }
  },
  created() {
    this.getTypeHemocomponents()
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          query: releases.listDailyReleaseReport(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.releases.results
        this.total = data.releases.totalCount
        this.listLoading = false
      })
    },
    getTypeHemocomponents() {
      graphqlRequest({
        from: this.$route.name,
        service: 'typehemocomponents',
        query: typehemocomponents.package_select(this.listTypeHemocomponentQuery)
      }).then(response => {
        this.typeHemocomponents = response.data.typehemocomponents.results
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
      this.listQuery.page = 1
      this.listQuery.offset = 0
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
      const filename = 'Reporte de Liberacion Diaria ' + moment(this.listQuery.extra.date_init, 'YYYY-MM-DD').format('DD-MM-YYYY') + '.pdf'

      reportToday(this.listQuery).then(
        response => {
          this.handleDownload(response, filename)
        }
      )
    }
  }
}
</script>

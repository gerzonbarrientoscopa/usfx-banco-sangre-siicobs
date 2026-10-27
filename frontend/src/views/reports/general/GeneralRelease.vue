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
      <el-tooltip :enterable="false" class="filter-item" content="Reporte General de Liberaciones (Lista)" effect="dark">
        <el-button v-loading.fullscreen.lock="fullscreenLoading" @click="handlePrintGeneralList">
          <font-awesome-icon icon="download" />
        </el-button>
      </el-tooltip>
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
      <el-table-column :label="$t('models.release.register_at')" align="center" fixed prop="register_at" sortable="custom" width="100px">
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
      <el-table-column :label="$t('models.release.hemocomponent')" align="center" width="260px">
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
      <el-table-column :label="$t('models.release.observations')" align="center" width="155px">
        <template slot-scope="scope">
          <span>{{ scope.row.observations }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.release.employee')" align="center" width="255px">
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
import checkPermission from '@/utils/permission'
import { graphqlRequest } from '@/api/graphql'
import releases from '@/query/release'
import { debounce } from 'debounce'
import moment from 'moment'
import { printGeneralListRelease, printGeneralRelease } from '@/api/report'

export default {
  name: 'GeneralRelease',
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
        extra: {
          date_init: moment().startOf('month').format('YYYY-MM-DD'),
          date_end: moment().format('YYYY-MM-DD')
        }
      },
      pdf: null,
      temp: {},
      fullscreenLoading: false
    }
  },
  computed: {},
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
          query: releases.listReleaseReport(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.releases.results
        this.total = data.releases.totalCount
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
      const filename = 'release'

      printGeneralRelease(this.listQuery).then(
        response => {
          this.fullscreenLoading = false
          this.handleDowload(response, filename)
        }
      )
    },
    handlePrintGeneralList() {
      this.fullscreenLoading = true
      this.$notify({
        title: 'Generando Reporte',
        message: 'Se esta generando el reporte',
        type: 'success',
        duration: 2000
      })
      const filename = 'release-list'

      printGeneralListRelease(this.listQuery).then(
        response => {
          this.fullscreenLoading = false
          this.handleDowload(response, filename)
        }
      )
    }
  }
}
</script>

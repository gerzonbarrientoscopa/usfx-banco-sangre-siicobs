<template>
  <div class="app-container">
    <div class="filter-container">
      <el-row :gutter="20" style="width: 100%">
        <el-col :md="8">
          <div class="block">
            <div class="demonstration">Fecha Inicial / Fecha Final</div>
            <el-date-picker
              v-model="listQuery.date_range"
              :picker-options="pickerRangeOptions"
              align="right"
              end-placeholder="Fecha Final"
              range-separator="A"
              start-placeholder="Fecha Inicial"
              format="dd-MM-yyyy"
              type="daterange"
              value-format="yyyy-MM-dd"
              unlink-panels
              @change="handleFilter"
            />
          </div>
        </el-col>
        <el-col :md="12">
          <div class="block">
            <span class="demonstration">Hemocomponente</span>
            <el-select v-model="listQuery.typehemocomponent_id" clearable filterable placeholder="Select" @change="handleFilter">
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

      </el-row>
    </div>
    <div class="filter-container">
      <el-row :gutter="20" style="width: 100%">
        <el-col :md="8">
          <div>
            <el-radio-group v-model="listQuery.typeFilter" @change="handleFilter">
              <el-radio-button label="">Todos</el-radio-button>
              <el-radio-button label="release">Liberados</el-radio-button>
              <el-radio-button label="discard">Descartados</el-radio-button>
            </el-radio-group>
          </div>
        </el-col>
        <el-col :md="16">
          <el-input
            v-model.lazy="listQuery.search"
            :placeholder="$t('donors.search')"
            :autofocus="'autofocus'"
            clearable
            prefix-icon="el-icon-search"
            class="filter-item"
            @input="handleFilter"
          />
        </el-col>
      </el-row>
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      :default-sort="{prop: 'register_at', order: 'descending'}"
      :row-class-name="tableRowClassName"
      border
      fit
      highlight-current-row
      style="width: 100%;"
      @sort-change="handleOrderChange"
    >
      <el-table-column :label="$t('models.storage.register_at')" align="center" fixed prop="register_at" sortable="custom" width="150px">
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.fragmentation.extraction.register_at | toHumanDate }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.storage.code')" align="center" prop="donor_code" sortable="custom" width="100px">
        <template slot-scope="scope">
          <span v-if="scope.row.fragmentation">
            <strong>{{ scope.row.donor_code }}</strong>
          </span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.storage.name')" align="center" width="350px">
        <template slot-scope="scope">
          <span>
            {{ scope.row.typehemocomponent.name }}
          </span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.storage.type_irregular_antibody')" align="center" width="255px">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.type_irregular_antibody">{{ scope.row.type_irregular_antibody.name }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.storage.weight')" align="right" width="80px">
        <template slot-scope="scope">
          <span>{{ scope.row.weight }} ml.</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.storage.expiration_date')" align="center" prop="expiration_date" sortable="custom" width="190px">
        <template slot-scope="scope">
          <span>{{ scope.row.expiration_date | toHumanDate }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.storage.pre_discard')" align="center" width="155px">
        <template slot-scope="scope">
          <span>{{ scope.row.typediscard ? 'SI' : 'NO' }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.storage.status')" align="center" width="200px">
        <template slot-scope="scope">
          <el-tag>
            <span>{{ getStatus(scope.row) }}</span>
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.storage.employee')" align="center" min-width="450">
        <template slot-scope="scope">
          <span>{{ scope.row.fragmentation.employee | fullName }}</span>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination-container">
      <el-pagination
        v-show="total>0"
        :current-page="listQuery.page"
        :page-sizes="[10,20,30, 50]"
        :page-size="listQuery.limit"
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
import itemFragmentations from '@/query/itemFragmentation'
import { debounce } from 'debounce'
import { defaultshorcouts } from '@/utils/date-utils'
import moment from 'moment'
import typehemocomponents from '@/query/type-hemocomponent'

export default {
  name: 'HemocomponentList',
  data() {
    return {
      pickerRangeOptions: {
        disabledDate(time) {
          return time.getTime() > Date.now()
        },
        shortcuts: defaultshorcouts()
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
        ordering: '-register_at',
        typehemocomponent_id: '',
        typeFilter: '',
        date_range: [moment().startOf('month').format('YYYY-MM-DD'), moment().format('YYYY-MM-DD')]
      },
      listTypeHemocomponentQuery: { page: 1, limit: 50, offset: 0, search: '', ordering: 'name' },
      temp: { id: undefined },
      typeHemocomponents: [],
      typeHemocomponentLoading: false
    }
  },
  computed: {},
  watch: {},
  created() {
    this.getList()
    this.getListTypeHemocomponents()
  },
  methods: {
    checkPermission,
    getStatus(row) {
      if (row && row.distributionitemfragmentations && row.distributionitemfragmentations.length > 0) {
        return 'DISTRIBUIDO'
      } else if (row.discard) {
        return 'DESCARTADO'
      } else if (row.release) {
        return 'LIBERADO'
      } else if (row.fragmentation.extraction.donation.immunohematology || row.fragmentation.extraction.donation.immunoserology) {
        return 'EN LABORATORIO'
      } else {
        return 'EN FRACCIONAMIENTO'
      }
    },
    tableRowClassName({ row, rowIndex }) {
      const isReactiveInmunoserologia = this.isReactiveInmunoserology(row.fragmentation.extraction.donation.immunoserology)

      if (isReactiveInmunoserologia) {
        return 'error-row'
      } else if (row.typediscard !== null) {
        return 'warning-row'
      }
      return ''
    },
    isRelease(row) {
      return row.release !== null || row.discard !== null || row.typediscard !== null || this.isReactiveInmunoserology(row.fragmentation.extraction.donation.immunoserology)
    },
    isReactiveInmunoserology(immunoserology) {
      if (immunoserology === null) {
        return false
      } else {
        return (immunoserology.chagas_hai === 'R' || immunoserology.hiv === 'R' || immunoserology.hbsag === 'R' ||
                        immunoserology.hvc === 'R' || immunoserology.cheia === 'R' || immunoserology.rpr === 'R')
      }
    },
    getList() {
      this.listLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'itemFragmentations',
          query: itemFragmentations.listHemocomponents(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.itemfragmentations.results
        this.total = data.itemfragmentations.totalCount
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
    handleOrderChange(val) {
      if (val['prop']) {
        this.listQuery.ordering = (val['order'] === 'descending' ? '-' : '') + val['prop']
        this.getList()
      }
    },
    getListTypeHemocomponents() {
      this.typeHemocomponentLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'typehemocomponents',
          query: typehemocomponents.package_select(this.listTypeHemocomponentQuery)
        }
      ).then(response => {
        const data = response.data
        this.typeHemocomponents = data.typehemocomponents.results
        this.typeHemocomponentLoading = false
      })
    }
  }
}
</script>
<style>
  .el-table .warning-row {
    background: oldlace;
  }

  .el-table .success-row {
    background: #f0f9eb;
  }
  .el-table .error-row {
    background: rgba(255, 0, 4, 0.22);
  }
  .el-table .warning-fg {
    color: #f79e1b;
  }

  .el-table .success-fg {
    color: #f0f9eb;
  }
  .el-table .error-fg {
    color: rgba(255, 21, 29, 0.98);
  }
</style>

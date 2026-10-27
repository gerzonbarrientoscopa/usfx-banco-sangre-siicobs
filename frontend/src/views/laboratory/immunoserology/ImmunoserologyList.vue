<template>
  <div class="app-container">
    <div class="filter-container">
      <el-row :gutter="20">
        <el-col :md="20">
          <div class="block">
            <div class="demonstration">Fecha Inicial / Fecha Final</div>
            <el-date-picker
              v-model="listQuery.date_range"
              :picker-options="pickerRangeOptions"
              align="right"
              end-placeholder="Fecha Final"
              format="dd-MM-yyyy"
              range-separator="A"
              start-placeholder="Fecha Inicial"
              type="daterange"
              unlink-panels
              value-format="yyyy-MM-dd"
              @change="handleFilter"
            />
          </div>
        </el-col>

      </el-row>
    </div>
    <div class="filter-container">
      <el-input
        v-model.lazy="listQuery.search"
        :autofocus="'autofocus'"
        :placeholder="$t('donors.search')"
        class="filter-item"
        clearable
        prefix-icon="el-icon-search"
        @input="handleFilter"
      />
      <el-button
        v-if="checkPermission(['add_immunoserology'])"
        class="filter-item"

        style="margin-left: 10px;"
        type="primary"
        @click="handleCreate"
      >{{ $t('add') }}
      </el-button>
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
    >
      <el-table-column :label="$t('models.immunoserology.register_at')" align="center" fixed width="130px">
        <template slot-scope="scope">
          <span>{{ scope.row.register_at | toHumanDate }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.immunoserology.code')" align="center" width="155px">
        <template slot-scope="scope">
          <span v-if="scope.row.donation">{{ scope.row.donation.donor.code }}</span>
          <el-tag v-if="scope.row.is_reactive" type="danger">REACTIVO</el-tag>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.immunoserology.chagas_hai')" align="center" width="140px">
        <template slot-scope="scope">
          <p :class="{ 'text_red': scope.row.chagas_hai === 'R' }">{{ scope.row.chagas_hai | typeReactFilter }}</p>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.immunoserology.cheia')" align="center" width="140px">
        <template slot-scope="scope">
          <p :class="{ 'text_red': scope.row.cheia === 'R' }">{{ scope.row.cheia | typeReactFilter }}</p>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.immunoserology.rpr')" align="center" width="140px">
        <template slot-scope="scope">
          <p :class="{ 'text_red': scope.row.rpr === 'R' }">{{ scope.row.rpr | typeReactFilter }}</p>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.immunoserology.hvc')" align="center" width="140px">
        <template slot-scope="scope">
          <p :class="{ 'text_red': scope.row.hvc === 'R' }">{{ scope.row.hvc | typeReactFilter }}</p>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.immunoserology.hbsag')" align="center" width="140px">
        <template slot-scope="scope">
          <p :class="{ 'text_red': scope.row.hbsag === 'R' }">{{ scope.row.hbsag | typeReactFilter }}</p>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.immunoserology.hiv')" align="center" width="140px">
        <template slot-scope="scope">
          <p :class="{ 'text_red': scope.row.hiv === 'R' }">{{ scope.row.hiv | typeReactFilter }}</p>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.immunoserology.employee')" align="center" width="350px">
        <template slot-scope="scope">
          <span>{{ scope.row.employee | fullName }}</span>
        </template>
      </el-table-column>
      <el-table-column
        :label="$t('actions')"
        align="center"
        class-name="small-padding"
        fixed="right"
        width="230"
      >
        <template slot-scope="scope">
          <el-button
            v-if="checkPermission(['change_immunoserology'])"
            size="mini"
            type="primary"
            @click="handleUpdate(scope.row)"
          >{{ $t('edit') }}</el-button>
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

    <el-dialog :before-close="handleCloseForm" :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible" destroy-on-close top="10px" width="90%">
      <immunoserology-form ref="history" :row="temp" @dialogStatus="handleCloseForm" />
    </el-dialog>

  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import ImmunoserologyForm from './ImmunoserologyForm'
import { graphqlRequest } from '@/api/graphql'
import immunoserologies from '@/query/immunoserology'
import { debounce } from 'debounce'
import moment from 'moment'
import { defaultshorcouts } from '@/utils/date-utils'

const typeReactOptions = [
  { key: 'R', display_name: 'REACTIVO' },
  { key: 'NR', display_name: 'NO REACTIVO' },
  { key: 'IN', display_name: 'INDETERMINADO' }
]

const typeReactKeyValue = typeReactOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})
export default {
  name: 'ImmunoserologyList',
  components: { ImmunoserologyForm },
  directives: {},
  filters: {
    typeReactFilter(type) {
      return typeReactKeyValue[type]
    }
  },
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
      typeReactOptions,
      listQuery: {
        page: 1, limit: 20, offset: 0, search: '', ordering: '-id',
        date_range: [moment().startOf('month').format('YYYY-MM-DD'), moment().format('YYYY-MM-DD')]
      },
      temp: {
        id: undefined
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Editando Serología',
        create: 'Creando Serología'
      },
      rules: {}
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
          service: 'immunoseologies',
          query: immunoserologies.list(this.listQuery)
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
    handleModifyStatus(row, status) {
      this.$message({
        message: '操作成功',
        type: 'success'
      })
      row.status = status
    },
    handleCreate() {
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.temp = null
    },
    handleUpdate(row) {
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.temp = row
    },
    handleCloseForm() {
      this.dialogFormVisible = false
      this.getList()
    }
  }
}
</script>

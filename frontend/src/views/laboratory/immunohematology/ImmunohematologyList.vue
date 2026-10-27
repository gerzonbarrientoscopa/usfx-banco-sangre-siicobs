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
        v-if="checkPermission(['add_immunohematology'])"
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
      <el-table-column :label="$t('models.immunohematology.register_at')" align="center" fixed width="120px">
        <template slot-scope="scope">
          <span>{{ scope.row.register_at | toHumanDate }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.immunohematology.code')" align="center" width="120px">
        <template slot-scope="scope">
          <span>{{ scope.row.donation.donor.code }}  </span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.immunohematology.direct_abo')" align="center" width="150px">
        <template slot-scope="scope">
          <span :inner-html.prop="scope.row.direct_abo | bloodGroupToHtml" />
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.immunohematology.factor_rh')" align="center" width="120px">
        <template slot-scope="scope">
          {{ scope.row.factor_rh | rhOptionsFilter }}
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.immunohematology.antikell')" align="center" width="95px">
        <template slot-scope="scope">
          <span>{{ scope.row.antikell | optionsGeneral }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.immunohematology.exist_irregular_antibody')" align="center" width="160px">
        <template slot-scope="scope">
          <span>{{ scope.row.exist_irregular_antibody ? 'POSITIVO': 'NEGATIVO' }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.immunohematology.employee')" align="center" width="350px">
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
            v-if="checkPermission(['change_immunohematology'])"
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

    <el-dialog
      :before-close="handleCloseForm"
      :title="textMap[dialogStatus]"
      :visible.sync="dialogFormVisible"
      destroy-on-close
      width="98%"
    >
      <immunohematology-form :row="temp" @dialogStatus="handleCloseForm" />
    </el-dialog>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import ImmunohematologyForm from './ImmunohematologyForm'
import { graphqlRequest } from '@/api/graphql'
import immunohematologies from '@/query/immunohematology'
import { debounce } from 'debounce'
import { RH_OPTIONS } from '@/utils/const'
import moment from 'moment'
import { defaultshorcouts } from '@/utils/date-utils'

const rhOptionKeyValue = RH_OPTIONS.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'ImmunohematologyList',
  components: { ImmunohematologyForm },
  directives: {},
  filters: {
    rhOptionsFilter(type) {
      return rhOptionKeyValue[type]
    },
    optionsGeneral(type) {
      if (type === '-') {
        return 'NEG'
      }
      return type
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
      listQuery: {
        page: 1, limit: 20, offset: 0, search: '', ordering: '-id',
        date_range: [moment().startOf('month').format('YYYY-MM-DD'), moment().format('YYYY-MM-DD')]
      },
      temp: {
        id: undefined,
        employee: undefined
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Editando Inmunohematología',
        create: 'Creando Inmunohematología'
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
          query: immunohematologies.list(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.immunohematologies.results
        this.total = data.immunohematologies.totalCount
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

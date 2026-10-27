<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model="listQuery.search"
        :placeholder="$t('donors.search')"
        :autofocus="'autofocus'"
        prefix-icon="el-icon-search"
        clearable
        class="filter-refreshment"
        @input="handleFilter"
      />
      <el-button
        v-if="checkPermission(['add_menu'])"
        class="filter-refreshment"
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
      <el-table-column :label="$t('models.menu.register_at')" align="left">
        <template slot-scope="scope">
          <span>{{ scope.row.register_at | toHumanDatetime }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.menu.name')" align="left">
        <template slot-scope="scope">
          <span>{{ scope.row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.menu.only_volunteer')" align="center">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.only_volunteer"> SI </el-tag>
          <el-tag v-if="!scope.row.only_volunteer"> NO </el-tag>
        </template>
      </el-table-column>
      <el-table-column
        :label="$t('actions')"
        fixed="right"
        align="center"
        width="250"
        class-name="small-padding"
      >
        <template slot-scope="scope">
          <el-button v-if="checkPermission(['change_menu'])" size="mini" @click="handleUpdate(scope.row)">{{ $t('edit') }}</el-button>
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

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible" :before-close="handleCloseForm" width="90%" destroy-on-close>
      <menu-form :row="temp" @dialogStatus="handleCloseForm" />
    </el-dialog>

  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import MenuForm from './MenuForm'
import { graphqlRequest } from '@/api/graphql'
import menus from '@/query/menu'
import { debounce } from 'debounce'

const typeOptions = [
  { key: '0', display_name: 'COMESTIBLE' },
  { key: '1', display_name: 'INCENTIVO' }
]

const typeKeyValue = typeOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'MenuList',
  components: { MenuForm },
  directives: {},
  filters: {
    typeFilter(type) {
      return typeKeyValue[type]
    }
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: null,
      listLoading: true,
      listQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-register_at' },
      temp: {},
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: { update: 'Editando Menu de Refrigerios', create: 'Creando Menu de Refrigerios' },
      downloadLoading: false,
      dialogShowVisible: false,
      typeOptions
    }
  },
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
          query: menus.list(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.menus.results
        this.total = data.menus.totalCount
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
    },
    handleShow(row) {
      this.temp = row
      this.dialogShowVisible = true
    },
    handleCloseDetail() {
      this.dialogShowVisible = false
    }
  }
}
</script>

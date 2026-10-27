<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model.lazy="listQuery.search"
        :autofocus="'autofocus'"
        :placeholder="$t('search')"
        class="filter-item"
        clearable
        prefix-icon="el-icon-search"
        @input="handleFilter"
      />
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
      @row-click="handleEdit"
    >
      <el-table-column :label="$t('models.event.name')">
        <template slot-scope="scope">
          <span>{{ scope.row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.event.init_at')" align="center" width="200px">
        <template slot-scope="scope">
          <span>{{ scope.row.init_at | toHumanDatetime }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.event.end_at')" align="center" width="230px">
        <template slot-scope="scope">
          <span>{{ scope.row.end_at | toHumanDatetime }}</span>
        </template>
      </el-table-column>

      <el-table-column
        :label="$t('actions')"
        align="center"
        class-name="small-padding"
        fixed="right"
        width="250"
      >
        <template slot-scope="scope">
          <el-button v-if="checkPermission(['change_event']) && scope.row.is_active" size="mini" @click.stop.prevent="handleClose(scope.row)">{{ $t('close') }}</el-button>
          <el-button v-if="checkPermission(['delete_event'])" size="mini" @click.stop.prevent="handleDelete(scope.row)">{{ $t('delete') }}</el-button>
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

    <el-dialog :title="$t('views.events.show.title')" :visible.sync="dialogShowVisible" destroy-on-close width="90%">
      <el-row>
        <el-col :md="24">
          <div class="grid-content">
            <event-detail :row="temp" @dialogStatus="handleCloseDetail" />
          </div>
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import EventDetail from './tab/EventDetail'
import { graphqlRequest } from '@/api/graphql'
import events from '@/query/event'

export default {
  name: 'Event',
  components: { EventDetail },
  directives: {},
  filters: {},
  data() {
    return {
      tableKey: 0,
      list: null,
      total: null,
      listLoading: true,
      listQuery: { page: 1, limit: 20, offset: 0, search: '', search_field: 'name', ordering: '-init_at' },
      temp: {},
      dialogStatus: '',
      textMap: { update: 'Editando Evento', create: 'Creando Evento' },
      downloadLoading: false,
      dialogShowVisible: false
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
          query: events.list(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.events.results
        this.total = data.events.totalCount
        this.listLoading = false
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.listQuery.offset = 0
      this.getList()
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
    handleShowDetail(row) {
      this.temp = row
      this.dialogShowVisible = true
    },
    handleCloseDetail() {
      this.dialogShowVisible = false
      this.temp = null
    },
    handleClose(row) {
      this.$confirm(`¿Está seguro de cerrar el evento ${row.name} ?
      Si realiza esta operación el evento actual ya no se mostrará para registrar en nuevas donaciones`, 'Cerrando Evento', {
        confirmButtonText: this.$t('confirmButtonText'),
        cancelButtonText: this.$t('cancelButtonText'),
        type: 'warning'
      }).then(() => {
        const tempData = Object.assign({}, row)
        tempData.is_active = false
        graphqlRequest(
          {
            from: this.$route.name,
            service: 'updateEvent',
            query: events.updateEvent(),
            variables: tempData
          }
        ).then(response => {
          if (response.errors) {
            this.$notify({
              title: 'Estado',
              message: response.errors[0].message,
              type: 'error',
              duration: 2000
            })
          } else {
            this.dialogFormVisible = false
            this.getList()
            this.$notify({
              title: 'Estado',
              message: 'Se ha cerrado el Evento',
              type: 'success',
              duration: 2000
            })
          }
        })
      }).catch(() => {
        // cancel
      })
    },
    handleDelete(row) {
      this.$confirm(`¿Está seguro de eliminar el evento ${row.name} ?`, {
        confirmButtonText: this.$t('confirmButtonText'),
        cancelButtonText: this.$t('cancelButtonText'),
        type: 'warning'
      }).then(() => {
        const tempData = Object.assign({}, row)
        tempData.is_active = false
        graphqlRequest(
          {
            from: this.$route.name,
            service: 'deleteEvent',
            query: events.deleteEvent(),
            variables: tempData
          }
        ).then(response => {
          if (response.errors) {
            this.$notify({
              title: 'Estado',
              message: response.errors[0].message,
              type: 'error',
              duration: 2000
            })
          } else {
            this.dialogFormVisible = false
            this.getList()
            this.$notify({
              title: 'Estado',
              message: 'Se ha eliminado el Evento',
              type: 'success',
              duration: 2000
            })
          }
        })
      }).catch(() => {
        // cancel
      })
    },
    handleEdit(row, event) {
      this.$router.push({ name: 'eventDetail', params: { id: row.id }})
    }
  }
}
</script>

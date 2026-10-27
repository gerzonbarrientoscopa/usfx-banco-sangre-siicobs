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
        v-if="checkPermission(['add_extractionrefreshment'])"
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

      <el-table-column :label="$t('models.extractionRefreshment.register_at')" align="center" fixed width="150px">
        <template slot-scope="scope">
          <span>{{ scope.row.register_at | toHumanDate }}</span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.donor.code')" align="center" width="150px">
        <template slot-scope="scope">
          <span><strong>{{ scope.row.extraction.donation.donor.code }}</strong></span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.extractionRefreshment.menu')" width="350px">
        <template slot-scope="scope">
          <span>{{ scope.row.menu.name }}</span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.exam.employee')" align="center">
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
          <el-button v-if="checkPermission(['change_extractionrefreshment'])" size="mini" @click="handleUpdate(scope.row)">{{ $t('edit') }}</el-button>
          <el-button
            v-if="checkPermission(['delete_extractionrefreshment']) && scope.row.status!=='deleted'"
            size="mini"

            @click="handleDelete(scope.row)"
          >{{ $t('delete') }}
          </el-button>
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

    <el-dialog :before-close="handleCloseForm" :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible" destroy-on-close width="60%">
      <extraction-refreshment-form :row="temp" @dialogStatus="handleCloseForm" />
    </el-dialog>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import { graphqlRequest } from '@/api/graphql'
import extractionRefreshments from '@/query/extractionRefreshment'
import { debounce } from 'debounce'
import moment from 'moment'
import { mapGetters } from 'vuex'
import { defaultshorcouts } from '@/utils/date-utils'
import ExtractionRefreshmentForm from '@/views/extractions/refreshment/ExtractionRefreshmentForm'
export default {
  name: 'ExtractionRefreshmentList',
  components: { ExtractionRefreshmentForm },
  directives: {},
  filters: {},
  data() {
    return {
      pickerRangeOptions: {
        shortcuts: defaultshorcouts()
      },
      tableKey: 0,
      extractions: null,
      list: null,
      total: null,
      loading: false,
      loadingMenu: false,
      loadingExtraction: false,
      listLoading: true,
      listExtractionQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-id' },
      listMenuQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-id' },
      listQuery: {
        page: 1,
        limit: 20,
        offset: 0,
        search: '',
        ordering: '-register_at,-extraction__donation__donor__code',
        date_range: [moment().startOf('month').format('YYYY-MM-DD'), moment().format('YYYY-MM-DD')]
      },
      temp: {
        id: undefined,
        extraction_id: undefined,
        menu_id: undefined,
        name: '',
        remark: '',
        timestamp: new Date(),
        title: '',
        type: '',
        status: 'published'
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Editando Asignacion de Refrigerio',
        create: 'Creando Asignacion de  Refrigerio'
      },
      downloadLoading: false,
      list_menu: []
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
    checkPermission,
    getList() {
      this.listLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'extractions',
          query: extractionRefreshments.list(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.extractionrefreshments.results
        this.total = data.extractionrefreshments.totalCount
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
    handleDelete(row) {
      this.$confirm(this.$t('messageConfirmDelete'), 'Warning', {
        confirmButtonText: this.$t('confirmButtonText'),
        cancelButtonText: this.$t('cancelButtonText'),
        type: 'warning'
      }).then(() => {
        const tempData = Object.assign({}, row)
        graphqlRequest(
          {
            from: this.$route.name,
            service: 'deleteExtractionRefreshment',
            query: extractionRefreshments.deleteExtractionRefreshment(),
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
            this.getList()
            this.$notify({
              title: 'Estado',
              message: 'Registro eliminado',
              type: 'success',
              duration: 2000
            })
          }
        })
      }).catch(() => {
        // cancel
      })
    }
  }
}
</script>

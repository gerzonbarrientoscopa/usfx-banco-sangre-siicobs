<template>
  <div class="app-container">
    <el-table
      :data="list"
      style="width: 100%"
    >
      <el-table-column type="index" width="50px" />
      <el-table-column label="Codigo" width="100px">
        <template slot-scope="scope">
          {{ scope.row.donor_code }}
        </template>
      </el-table-column>
      <el-table-column label="Tipo de Hemocomponente">
        <template slot-scope="scope">
          {{ scope.row.typehemocomponent.name }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="Fecha de Expiración" width="160px">
        <template slot-scope="scope">
          {{ scope.row.expiration_date | toHumanDate }}
        </template>
      </el-table-column>
      <el-table-column align="left" label="Peso" width="100px">
        <template slot-scope="scope">
          {{ scope.row.weight }} gr.
        </template>
      </el-table-column>
      <el-table-column label="Tipo de Descarte">
        <template slot-scope="scope">
          <span v-if="scope.row.typediscard"> {{ scope.row.typediscard.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Observaciones">
        <template slot-scope="scope">
          {{ scope.row.observations }}
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
import itemFragmentations from '@/query/itemFragmentation'
import { debounce } from 'debounce'

export default {
  name: 'FragmentationItemList',
  components: {},
  directives: {},
  filters: {},
  props: {
    fragmentation: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: null,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        offset: 0,
        search: '',
        fragmentation__id: '',
        ordering: 'id'
      },
      temp: {}
    }
  },
  watch: {
    fragmentation: function() {
      this.getList()
    }
  },
  created() {
    this.getList()
  },
  mounted() {
    this.getList()
  },
  methods: {
    checkPermission,
    getList() {
      this.listLoading = true
      const tempListQuery = Object.assign({}, this.listQuery)
      if (this.fragmentation) {
        tempListQuery.fragmentation__id = this.fragmentation.id
      }

      graphqlRequest(
        {
          from: this.$route.name,
          service: 'itemfragmentations',
          query: itemFragmentations.listFragmentation(tempListQuery)
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
    }
  }
}
</script>


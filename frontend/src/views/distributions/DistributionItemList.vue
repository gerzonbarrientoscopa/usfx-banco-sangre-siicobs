<template>
  <div class="app-container">
    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
    >
      <el-table-column align="center" type="index" width="50" />
      <el-table-column align="center" label="Código" width="100">
        <template slot-scope="scope">
          <strong>{{ scope.row.itemfragmentation.donor_code }}</strong>
        </template>
      </el-table-column>
      <el-table-column label="Tipo de Hemocomponente" min-width="350">
        <template slot-scope="scope">
          {{ scope.row.itemfragmentation.typehemocomponent.name }}
        </template>
      </el-table-column>
      <el-table-column label="Tubuladura" width="120">
        <template slot-scope="scope">
          {{ scope.row.itemfragmentation.fragmentation.extraction.tubing }}
        </template>
      </el-table-column>
      <el-table-column label="Volumen" width="100">
        <template slot-scope="scope">
          {{ scope.row.itemfragmentation.weight }} ml.
        </template>
      </el-table-column>
      <el-table-column label="Estado" width="150">
        <template slot-scope="scope">
          <el-tag :type="scope.row.distributionitemfragmentationrefunded ? 'danger': ''">
            {{ getStatus(scope.row.distributionitemfragmentationrefunded) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column
        :label="$t('actions')"
        align="center"
        class-name="small-padding"
        fixed="right"
        width="130"
      >
        <template slot-scope="scope">
          <el-button
            v-if="checkPermission(['add_distributionitemfragmentationrefunded']) && !scope.row.distributionitemfragmentationrefunded && (distribution.status!=='CANCELED' && distribution.status!=='IN_PROGRESS')"
            size="mini"
            type="primary"
            @click="updateData(scope.row)"
          >Devolver
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
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import { graphqlRequest } from '@/api/graphql'
import distributionItemFragmentation from '@/query/distributionItemFragmentation'
import { debounce } from 'debounce'

export default {
  name: 'DistributionItemList',
  components: {},
  directives: {},
  filters: {},
  props: {
    distribution: {
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
        distribution__id: '',
        ordering: 'id'
      },
      temp: {}
    }
  },
  watch: {
    distribution: function() {
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
    updateData(row) {
      this.$prompt('Está seguro de marcar como Devuelto?', 'Confirmación', {
        confirmButtonText: 'Si',
        cancelButtonText: 'Cancelar',
        inputPattern: /^(?! *$)[a-zA-Z.+ '-]+$/,
        inputErrorMessage: 'Por favor describa porque se esta devolviendo el Hemocomponente',
        inputPlaceholder: 'Razon',
        type: 'warning'
      }).then((option) => {
        graphqlRequest(
          {
            from: this.$route.name,
            service: 'create_distribution_item_fragmentation_refunded',
            query: distributionItemFragmentation.change_item_distribution(),
            variables: { id: row.id, reason: option.value }
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
              message: 'Se ha actualizado',
              type: 'success',
              duration: 2000
            })
          }
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: 'Cancelado'
        })
      })
    },
    getList() {
      this.listLoading = true
      const tempListQuery = Object.assign({}, this.listQuery)
      if (this.distribution) {
        tempListQuery.distribution__id = this.distribution.id
      }

      graphqlRequest(
        {
          from: this.$route.name,
          service: 'distribution_item_fragmentations',
          query: distributionItemFragmentation.list(tempListQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.distribution_itemfragmentations.results
        this.total = data.distribution_itemfragmentations.totalCount
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
    getStatus(status) {
      switch (this.distribution.status) {
        case 'NEW':
        case 'IN_PROGRESS':
          return 'EN PROCESO'
        case 'CANCELED':
          return 'CANCELADO'
        default:
          return status ? 'DEVUELTO' : 'ENTREGADO'
      }
    }
  }
}
</script>


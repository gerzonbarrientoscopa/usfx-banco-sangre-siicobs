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
      <el-table-column :label="$t('models.immunohematology.register_at')" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.register_at | toHumanDate }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.immunohematology.status')" align="center">
        <template slot-scope="scope">
          <el-tag v-if="donation.id === scope.row.donation.id">ACTUAL</el-tag>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.immunohematology.direct_abo')" align="center">
        <template slot-scope="scope">
          <span :inner-html.prop="scope.row.direct_abo | bloodGroupToHtml" />
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.immunohematology.factor_rh')" align="center">
        <template slot-scope="scope">
          {{ scope.row.factor_rh | rhOptionsFilter }}
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.immunohematology.phenotype')" align="center">
        <template slot-scope="scope">
          {{ scope.row.phenotype }}
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.immunohematology.type_irregular_antibody')" align="center" width="250">
        <template slot-scope="scope">
          <span>{{ get_type_irregular_antibody(scope.row) }}</span>
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
import immunohematologies from '@/query/immunohematology'
import { RH_OPTIONS } from '@/utils/const'

const rhOptionKeyValue = RH_OPTIONS.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'HistoryImmunohematologyDonor',
  components: { },
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
  props: {
    donation: {
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
        ordering: '-register_at',
        donation__donor__id: ''
      }
    }
  },
  watch: {
    donation: function() {
      this.getList()
    }
  },
  created() {
    this.getList()
  },
  methods: {
    checkPermission,
    get_type_irregular_antibody(row) {
      const state = (row.alb && row.alb.indexOf('+') !== -1) ||
          (row.fsi && row.fsi.indexOf('+') !== -1) ||
          (row.liss && row.liss.indexOf('+') !== -1) ||
          (row.coombs && row.coombs.indexOf('+') !== -1) ||

          (row.p2alb && row.p2alb.indexOf('+') !== -1) ||
          (row.p2fsi && row.p2fsi.indexOf('+') !== -1) ||
          (row.p2liss && row.p2liss.indexOf('+') !== -1) ||
          (row.p2coombs && row.p2coombs.indexOf('+') !== -1) ||

          (row.p3alb && row.p3alb.indexOf('+') !== -1) ||
          (row.p3fsi && row.p3fsi.indexOf('+') !== -1) ||
          (row.p3liss && row.p3liss.indexOf('+') !== -1) ||
          (row.p3coombs && row.p3coombs.indexOf('+') !== -1)
      if (state == null || state === false) {
        return 'NEGATIVO'
      } else {
        return 'POSITIVO'
      }
    },
    getList() {
      this.listLoading = true
      this.listQuery.donation__donor__id = this.donation.donor.id
      graphqlRequest(
        {
          from: this.$route.name,
          query: immunohematologies.short_list(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.immunohematologies.results
        this.total = data.immunohematologies.totalCount
        this.listLoading = false
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
    }
  }
}
</script>

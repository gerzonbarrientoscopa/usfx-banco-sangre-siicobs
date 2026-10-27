<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model.lazy="listQuery.search"
        :autofocus="'autofocus'"
        :placeholder="$t('models.donation.search')"
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
      stripe
      style="width: 100%;"
    >
      <el-table-column
        :label="$t('models.donation.register_at')"
        align="center"
        fixed
        prop="register_at"
        sortable="custom"
        width="190px"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.register_at | toHumanDate }}</span>
        </template>
      </el-table-column>
      <el-table-column
        :label="$t('models.donor.code')"
        align="center"
        prop="donor__code"
        sortable="custom"
        width="120px"
      >
        <template slot-scope="scope">
          <strong>{{ scope.row.donor.code }}</strong>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.donor.names')" align="left" width="220px">
        <template slot-scope="scope">
          <span>{{ scope.row.donor | fullName }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.donation.type_donation')" align="left" width="200px">
        <template slot-scope="scope">
          <span>{{ scope.row.type_donation | typeDonationFilter }}</span>
          <br>
          <small>{{ scope.row.patient | fullName }}</small>
        </template>
      </el-table-column>
      <el-table-column v-if="isAreaPromotion" :label="$t('models.donation.event')" align="left" width="200px">
        <template slot-scope="scope">
          <span v-if="scope.row.event">{{ scope.row.event.name }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.donation.place')" align="center" width="155px">
        <template slot-scope="scope">
          <span v-if="scope.row.place">{{ scope.row.place.name }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.donation.last_donation_at')" align="center" width="200px">
        <template slot-scope="scope">
          <span>{{ scope.row.last_donation_at }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.donation.employee')" align="center" width="300">
        <template slot-scope="scope">
          <span>{{ scope.row.employee | fullName }}</span>
        </template>
      </el-table-column>
      <el-table-column
        :label="$t('actions')"
        align="center"
        class-name="small-padding"
        fixed="right"
        width="120"
      >
        <template slot-scope="scope">
          <el-button
            v-if="checkPermission(['change_donation'])"
            size="mini"
            @click.stop.prevent="updateData(scope.row)"
          >
            {{ $t('assign') }}
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
import { mapGetters } from 'vuex'
import { graphqlRequest } from '@/api/graphql'
import { debounce } from 'debounce'
import donations from '@/query/donation'

const typeDonationOptions = [
  { key: 'VA', display_name: 'VOLUNTARIA ALTRUISTA' },
  { key: 'RS', display_name: 'REPOSICION SOLIDARIA' },
  { key: 'RE', display_name: 'REPOSICION EXIGIDA' },
  { key: 'DA', display_name: 'DONACION AUTOLOGA' }
]

const statusOptions = [
  { key: 'NU', display_name: 'NUEVO' },
  { key: 'EP', display_name: 'EN PROCESO' },
  { key: 'CO', display_name: 'COMPLETADO' },
  { key: 'RE', display_name: 'DIFERIDO' }
]

const typeDonationKeyValue = typeDonationOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'EventAddDonation',
  directives: {},
  filters: {
    typeDonationFilter(type) {
      return typeDonationKeyValue[type]
    }
  },
  props: {
    row: {
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
        ordering: '-donor__code'
      },
      typeDonationOptions,
      statusOptions,
      isAreaPromotion: false
    }
  },
  computed: {
    ...mapGetters([
      'employees',
      'employee_id'
    ])
  },
  watch: {
    row: function() {
      this.getList()
    }
  },
  created() {
    this.getList()
  },
  methods: {
    checkPermission,
    getList() {
      this.listQuery.only_event = false
      this.listLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'donations',
          query: donations.listWithoutEvent(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.donations.results
        this.total = data.donations.totalCount
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
    updateData(row) {
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'updateDonation',
          query: donations.updateDonation(),
          variables: { id: row.id, event_id: this.row.id }
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
          this.dialogFormVisible = false
          this.$notify({
            title: 'Estado',
            message: 'Registro actualizado',
            type: 'success',
            duration: 2000
          })
        }
      })
    }
  }
}
</script>

<style>
.el-table .warning-row {
  background: rgba(249, 0, 4, 0.22);
}

.el-table .success-row {
  background: #f0f9eb;
}

.red {
  background-color: red;
}

.orange {
  background-color: orange;
}

.yellow {
  background-color: yellow;
}

.white {
  background-color: transparent;
}

.circle {
  width: 13px;
  height: 13px;
  border-radius: 50%;
  -moz-border-radius: 50px;
  -webkit-border-radius: 50px;
  display: inline-block;
}
</style>

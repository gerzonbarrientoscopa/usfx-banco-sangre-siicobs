<template>
  <div>
    <div class="pagination-container" style="margin-top: 0">
      <el-pagination
        v-show="total>0"
        :current-page="listQuery.page"
        :page-sizes="[50, 100]"
        :page-size="listQuery.limit"
        :total="total"
        background
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
    <div class="components-container board">
      <Kanban :key="1" :list="list1" :group="group" class="kanban todo" header-text="Tamizaje y Pretamizaje" />
      <Kanban :key="2" :list="list2" :group="group" class="kanban working" header-text="Extraccion" />
      <Kanban :key="3" :list="list3" :group="group" class="kanban done" header-text="Fraccionamiento" />
      <Kanban :key="4" :list="list4" :group="group" class="kanban quarantine" header-text="Cuarentena" />
    </div>
  </div>
</template>

<script>
import Kanban from '@/components/Kanban'
import { graphqlRequest } from '@/api/graphql'
import donations from '@/query/donation'

export default {
  components: {
    Kanban
  },
  filters: {
    statusFilter(status) {
      const statusMap = {
        'NU': 'NUEVO',
        'EP': 'EN PROCESO',
        'CO': 'COMPLETADO',
        'RE': 'DIFERIDO'
      }
      return statusMap[status]
    },
    statusColorFilter(status) {
      const statusMap = {
        'NU': '',
        'EP': 'warning',
        'CO': 'success',
        'RE': 'danger'
      }
      return statusMap[status]
    },
    orderNoFilter(str) {
      return str.substring(0, 30)
    }
  },
  data() {
    return {
      list: null,
      total: null,
      listQuery: {
        page: 1,
        limit: 100,
        offset: 0,
        search: '',
        ordering: '-register_at',
        from: 'main',
        extra: {
          date_init: '',
          date_end: '',
          patient_id: ''
        }
      },
      group: 'mission',
      list1: [],
      list2: [],
      list3: [],
      list4: []
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'donations',
          query: donations.list_dashboard(this.listQuery)
        }
      ).then(response => {
        const data = response.data

        this.list = data.donations.results
        this.total = data.donations.totalCount
        this.listLoading = false
        this.filterForBoard()
      })
    },
    filterForBoard() {
      const list_one = []
      const list_two = []
      const list_three = []
      const list_four = []
      this.list.forEach(function(item, index, array) {
        const data = { name: item.register_at.toString(10) + ' >>' + item.donor.code.toString(10) + '<<', id: item.id }
        if (item.donor.code === 39521) {
          console.log(item)
        }
        if (item.extraction !== null && item.extraction.fragmentation !== null && (item.immunoserology !== null || item.immunohematology !== null)) {
          list_four.push(data)
        } else if (item.extraction !== null && item.extraction.fragmentation !== null) {
          list_three.push(data)
        } else if (item.extraction !== null && item.extraction.fragmentation === null) {
          list_two.push(data)
        } else if (item.extraction === null) {
          list_one.push(data)
        } else {
          console.log('sin clasificar')
        }
      })
      this.list1 = list_one
      this.list2 = list_two
      this.list3 = list_three
      this.list4 = list_four
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
<style lang="scss">
  .board {
    width: 100%;
    margin-left: 2px;
    display: flex;
    justify-content: space-around;
    flex-direction: row;
    align-items: flex-start;
  }
  .kanban {
    &.todo {
      .board-column-header {
        background: #4A9FF9;
      }
    }
    &.working {
      .board-column-header {
        background: #f9944a;
      }
    }
    &.done {
      .board-column-header {
        background: #2ac06d;
      }
    }
    &.quarantine {
      .board-column-header {
        background: #c0560d;
      }
    }
  }
</style>

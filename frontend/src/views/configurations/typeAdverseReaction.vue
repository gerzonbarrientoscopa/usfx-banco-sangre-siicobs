<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model="listQuery.search"
        :placeholder="$t('search')"
        :autofocus="'autofocus'"
        prefix-icon="el-icon-search"
        clearable
        class="filter-item"
        @input="handleFilter"
      />
      <el-button
        v-if="checkPermission(['add_typeadversereaction'])"
        class="filter-item"
        style="margin-left: 10px;"
        type="primary"
        icon="el-icon-plus"
        @click="handleCreate"
      >
        {{ $t('add') }}
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
      <el-table-column type="index" width="50" label="#" />

      <el-table-column :label="$t('models.typeAdverseReaction.name')" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.typeAdverseReaction.show_in_conventional')" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.show_in_conventional | yesNoFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.typeAdverseReaction.show_in_apheresis')" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.show_in_apheresis | yesNoFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.typeAdverseReaction.level')" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.level | levelTypeFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('actions')" align="center" class-name="small-padding" fixed="right" width="230">
        <template slot-scope="scope">
          <el-button v-if="checkPermission(['change_typeadversereaction'])" type="primary" size="mini" @click="handleUpdate(scope.row)">
            {{ $t('edit') }}
          </el-button>
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

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible" width="60%">
      <el-form ref="dataForm" :model="temp" :rules="rules" label-position="right" label-width="250px" style="width: 100%;">
        <el-row :gutter="20">
          <el-col :sm="24" :md="24">
            <div class="grid-content">
              <el-form-item :label="$t('models.typeAdverseReaction.name')" prop="name">
                <el-input v-model="temp.name" @input.native="setUpperCase(temp, 'name', $event)" />
              </el-form-item>
              <el-form-item :label="$t('models.typeAdverseReaction.show_in_conventional')" prop="show_in_conventional">
                <el-radio-group v-model="temp.show_in_conventional">
                  <el-radio-button :label="false">No</el-radio-button>
                  <el-radio-button :label="true">Si</el-radio-button>
                </el-radio-group>
              </el-form-item>
              <el-form-item :label="$t('models.typeAdverseReaction.show_in_apheresis')" prop="show_in_apheresis">
                <el-radio-group v-model="temp.show_in_apheresis">
                  <el-radio-button :label="false">No</el-radio-button>
                  <el-radio-button :label="true">Si</el-radio-button>
                </el-radio-group>
              </el-form-item>
              <el-form-item :label="$t('models.typeAdverseReaction.level')" prop="level">
                <el-radio-group v-model="temp.level">
                  <el-radio-button v-for="item in CATEGORY_TYPE_REACTION_OPTIONS" :key="item.key" :label="item.key">
                    {{ item.display_name }}
                  </el-radio-button>
                </el-radio-group>
              </el-form-item>
            </div>
          </el-col>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          {{ $t('cancelButtonText') }}
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">
          {{ $t('confirmButtonText') }}
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import { graphqlRequest } from '@/api/graphql'
import typeAdverseReactions from '@/query/typeAdverseReaction'
import { debounce } from 'debounce'
import { CATEGORY_TYPE_REACTION_OPTIONS } from '@/utils/const'

const typeKeyValue = CATEGORY_TYPE_REACTION_OPTIONS.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'TypeAdverseReaction',
  filters: {
    levelTypeFilter(type) {
      return typeKeyValue[type]
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
        ordering: '-id'
      },
      showReviewer: false,
      for_loop: 0,
      temp: {
        id: undefined,
        name: '',
        type: ''
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Modificando Tipo de Reacción Adversa',
        create: 'Agregando Tipo de Reacción Adversa'
      },
      rules: {
        name: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        show_in_conventional: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        show_in_apheresis: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        level: [{ required: true, message: this.$t('is_required'), trigger: 'change' }]
      },
      downloadLoading: false,
      CATEGORY_TYPE_REACTION_OPTIONS
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
          query: typeAdverseReactions.list(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.typeadversereactions.results
        this.total = data.typeadversereactions.totalCount
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
        message: 'Se modifico el estado de una fila',
        type: 'success'
      })
      row.status = status
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        name: '',
        type: '',
        show_in_conventional: false,
        show_in_apheresis: false,
        level: 'LOW'
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'createTypeAdverseReaction',
              query: typeAdverseReactions.createTypeAdverseReaction(),
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
              this.dialogFormVisible = false
              this.$notify({
                title: 'Estado',
                message: 'Registro creado',
                type: 'success',
                duration: 2000
              })
            }
          })
        }
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.temp.timestamp = new Date(this.temp.timestamp)
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'updateTypeAdverseReaction',
              query: typeAdverseReactions.updateTypeAdverseReaction(),
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
      })
    }
  }
}
</script>

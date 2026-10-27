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
        v-if="checkPermission(['add_clinicalhistoryquestion'])"
        class="filter-item"
        style="margin-left: 10px;"
        type="primary"

        @click="handleCreate"
      >
        {{ $t('add') }}
      </el-button>
      <el-checkbox
        v-model="showReviewer"
        class="filter-item"
        style="margin-left:15px;"
        @change="tableKey=tableKey+1"
      >
        {{ $t('models.questionnaire.register_at') }}
      </el-checkbox>
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
      <el-table-column label="#" type="index" width="50" />

      <el-table-column :label="$t('models.questionnaire.title')" width="360px">
        <template slot-scope="scope">
          <span>{{ scope.row.title }}</span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.questionnaire.is_active')" width="200px" align="center">
        <template slot-scope="scope">
          <span>{{ handleSelectStatus(scope.row.is_active) }}</span>
        </template>
      </el-table-column>

      <el-table-column v-if="showReviewer" :label="$t('models.questionnaire.register_at')" align="left">
        <template slot-scope="scope">
          <span>{{ scope.row.register_at }}</span>
        </template>
      </el-table-column>

      <el-table-column
        :label="$t('actions')"
        fixed="right"
        align="center"
        width="300"
        class-title="small-padding"
      >
        <template slot-scope="scope">
          <el-button v-if="checkPermission(['change_clinicalhistoryquestion'])" size="mini" @click="handleUpdate(scope.row)">
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

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible" width="60%" destroy-on-close>
      <el-form
        ref="dataForm"
        :rules="rules"
        :model="temp"
        label-position="left"
        label-width="120px"
        style="width: 100%;"
      >
        <el-row :gutter="20">
          <el-col :sm="24" :md="24">
            <div class="grid-content">
              <el-form-item :label="$t('models.questionnaire.title')" prop="title">
                <el-input v-model="temp.title" @input.native="setUpperCase(temp, 'title', $event)" />
              </el-form-item>

              <el-form-item :label="$t('models.questionnaire.questions')" prop="title">
                <div class="editor-container">
                  <json-editor ref="jsonEditor" v-model="temp.questions" />
                </div>
              </el-form-item>

              <el-form-item :label="$t('models.questionnaire.is_active')" prop="is_active">
                <el-checkbox v-model="temp.is_active">
                  <span v-if="temp.is_active">Activo</span>
                  <span v-else>Inactivo</span>
                </el-checkbox>
              </el-form-item>
            </div>
          </el-col>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          {{ $t('cancelButtonText') }}
        </el-button>
        <el-button @click="dialogStatus==='create'?createData():updateData()">
          {{ $t('confirmButtonText') }}
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import JsonEditor from '@/components/JsonEditor'
import { graphqlRequest } from '@/api/graphql'
import clinicalHistoryQuestions from '@/query/clinicalHistoryQuestion'
import { debounce } from 'debounce'

const selectOptions = [
  { key: 'S', display_name: 'Seleccion Simple' },
  { key: 'T', display_name: 'Pregunta Abierta' }
]

export default {
  title: 'Questionnaire',
  components: { JsonEditor },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: null,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        importance: undefined,
        title: undefined,
        offset: 0,
        search: '',
        ordering: '-id'
      },
      showReviewer: false,
      for_loop: 0,
      selectOptions,
      temp: {
        id: undefined,
        title: '',
        questions: [],
        is_active: false
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Editando Cuestionario',
        create: 'Creando Cuestionario'
      },
      rules: {
        title: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        option_title: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        subtitle: [{ trigger: 'blur' }],
        option_subtitle: [{ trigger: 'blur' }],
        status: [{ trigger: 'blur' }]
      },
      downloadLoading: false
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
          query: clinicalHistoryQuestions.list(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.clinicalhistoryquestions.results
        this.total = data.clinicalhistoryquestions.totalCount
        this.listLoading = false
      })
    },
    handleSelectStatus(is_active) {
      return is_active ? 'Activo' : 'Inactivo'
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
        title: '',
        questions: [],
        is_active: false
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
              service: 'createClinicalHistory',
              query: clinicalHistoryQuestions.createClinicalHistory(),
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
      this.temp = Object.assign({}, row)
      this.temp.questions = JSON.parse(this.temp.questions)
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
              service: 'updateClinicalHistory',
              query: clinicalHistoryQuestions.updateClinicalHistory(),
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

<style scoped>
  .editor-container{
    position: relative;
    height: 100%;
  }
</style>

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
        <el-col :md="4">
          <span class="demonstration">Total</span>
          <br>
          <strong style="font-size: 2em">
            {{ total }}
          </strong>
        </el-col>
      </el-row>
    </div>
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
      <el-button
        v-if="checkPermission(['add_serologyprotocol'])"
        class="filter-item"
        icon="el-icon-plus"
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
      <el-table-column :label="$t('models.serologyProtocol.register_at')" align="left" fixed width="150px">
        <template slot-scope="scope">
          <span>{{ scope.row.register_at | toHumanDate }}</span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.serologyProtocol.method')" align="left" fixed width="200px">
        <template slot-scope="scope">
          <span>{{ scope.row.method }}</span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.serologyProtocol.kit')" align="left" width="200px">
        <template slot-scope="scope">
          <span>{{ scope.row.kit }}</span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.serologyProtocol.due_date_at')" align="left" width="110px">
        <template slot-scope="scope">
          <span>{{ scope.row.due_date_at | toHumanDate }}</span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.serologyProtocol.lot')" align="left" width="150px">
        <template slot-scope="scope">
          <span>{{ scope.row.lot }}</span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.serologyProtocol.industry')" align="left" width="220px">
        <template slot-scope="scope">
          <span>{{ scope.row.industry }}</span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.serologyProtocol.test')" align="left" width="130px">
        <template slot-scope="scope">
          <span>{{ scope.row.test }}</span>
        </template>
      </el-table-column>

      <el-table-column
        :label="$t('actions')"
        align="center"
        class-name="small-padding"
        fixed="right"
        width="270px"
      >
        <template slot-scope="scope">
          <el-button
            v-if="checkPermission(['change_serologyprotocol'])"
            size="mini"
            type="primary"
            @click="handleUpdate(scope.row)"
          >{{ $t('edit') }}</el-button>
          <el-button size="mini" type="default" @click="handlePrintSerologyProtocol(scope.row)">{{ $t('print') }}</el-button>
          <el-button
            v-if="scope.row.status!=='deleted'"
            size="mini"
            type="danger"
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

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible" destroy-on-close width="80%">
      <el-form
        ref="dataForm"
        :model="temp"
        :rules="rules"
        label-position="right"
        label-width="200px"
        style="width: 100%;"
      >
        <el-row :gutter="20">
          <el-col :md="24" :sm="24">
            <div class="grid-content">
              <el-row :gutter="20">
                <el-col :md="12" :sm="24">
                  <el-form-item :label="$t('models.serologyProtocol.register_at')" prop="register_at">
                    <el-date-picker
                      v-model="temp.register_at"
                      :placeholder="$t('models.serologyProtocol.register_at')"
                      format="dd-MM-yyyy"
                      type="date"
                      value-format="yyyy-MM-dd"
                    />
                  </el-form-item>
                  <el-form-item :label="$t('models.serologyProtocol.method')" prop="method">
                    <el-autocomplete v-model="temp.method" :fetch-suggestions="querySearchMethod" :trigger-on-focus="false" />
                  </el-form-item>

                  <el-form-item :label="$t('models.serologyProtocol.kit')" prop="kit">
                    <el-autocomplete v-model="temp.kit" :fetch-suggestions="querySearchKit" :trigger-on-focus="false" />
                  </el-form-item>

                  <el-form-item :label="$t('models.serologyProtocol.due_date_at')" prop="due_date_at">
                    <el-date-picker
                      v-model="temp.due_date_at"
                      :placeholder="$t('models.serologyProtocol.due_date_at')"
                      format="dd-MM-yyyy"
                      type="date"
                      value-format="yyyy-MM-dd"
                    />
                  </el-form-item>

                  <el-form-item :label="$t('models.serologyProtocol.lot')" prop="lot">
                    <el-input v-model="temp.lot" @input.native="setUpperCase(temp, 'lot', $event)" />
                  </el-form-item>

                  <el-form-item :label="$t('models.serologyProtocol.industry')" prop="industry">
                    <el-autocomplete v-model="temp.industry" :fetch-suggestions="querySearchIndustry" :trigger-on-focus="false" />
                  </el-form-item>
                </el-col>
                <el-col :md="12" :sm="24">
                  <el-form-item :label="$t('models.serologyProtocol.test')" prop="test">
                    <el-input-number v-model.number="temp.test" :min="18000000" :step="1" />
                  </el-form-item>

                  <el-form-item :label="$t('models.serologyProtocol.type')" prop="type">
                    <p v-if="dialogStatus==='update'" style="margin-top: 0;"><strong>{{ temp.type | typeOptionsFilter }}</strong></p>
                    <el-select v-if="dialogStatus === 'create'" v-model="temp.type" :placeholder="$t('please_select')" automatic-dropdown class="filter-item">
                      <el-option
                        v-for="item in typeOptions"
                        :key="item.key"
                        :label="item.display_name"
                        :value="item.key"
                      />
                    </el-select>
                  </el-form-item>
                  <el-form-item :label="$t('models.serologyProtocol.cutt_off')" prop="cutt_off">
                    <el-input v-model="temp.cutt_off" />
                  </el-form-item>
                  <el-form-item :label="$t('models.serologyProtocol.cutt_off_min')" prop="cutt_off_min">
                    <el-input v-model="temp.cutt_off_min" />
                  </el-form-item>
                  <el-form-item :label="$t('models.serologyProtocol.cutt_off_max')" prop="cutt_off_max">
                    <el-input v-model="temp.cutt_off_max" />
                  </el-form-item>
                  <el-form-item :label="$t('models.exam.employee')" prop="employee_id">
                    <el-select
                      v-model="temp.employee_id"
                      :placeholder="$t('please_select')"
                      automatic-dropdown
                      class="filter-item"
                      filterable
                    >
                      <el-option
                        v-for="item in employees"
                        :key="item.id"
                        :label="item.first_name +' '+ item.middle_name +' '+ item.last_name "
                        :value="item.id"
                      />
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>
              <table :key="'test'" class="table">
                <tbody>
                  <tr>
                    <td>&nbsp;</td>
                    <td v-for="n in 12" :key="n" align="center" class="title">{{ n }} </td>
                  </tr>
                  <tr v-for="(row, index_v) in temp.values" :key="index_v">
                    <td align="center" class="title">{{ String.fromCharCode(index_v + 65) }}</td>
                    <td v-for="(col, index2) in row" :key="index2" :class="{'error': col.is_duplicated }" align="center">
                      <el-form-item label-width="0" style="margin: 0; padding: 0">
                        <el-input
                          :ref="'comp'+(index2 + 1) +''+ index_v"
                          v-model="col.value"
                          :tabindex="(index2 + 1) +''+ index_v"
                          @blur="validate(col.value, index_v, index2)"
                          @keyup.enter.native="getFocus(index2 + 1, index_v)"
                        />
                        <span class="text-carrot-400">{{ col.result_machine }}</span>
                      </el-form-item>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </el-col>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">{{ $t('cancelButtonText') }}</el-button>
        <el-button @click="dialogUploadVisible = true">Importar Resultados de Maquina</el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">
          {{ $t('confirmButtonText') }}
        </el-button>
      </div>
    </el-dialog>

    <el-dialog :visible.sync="dialogUploadVisible" destroy-on-close title="Importar Resultados de Maquina" width="60%">
      <el-row>
        <el-col :md="24">
          <upload-excel-component :before-upload="beforeUpload" :on-success="handleSuccess" />
          <div align="center">
            <br>
            <el-alert
              v-if="loadSections"
              :closable="false"
              show-icon
              title="EL ARCHIVO FUE CARGADO CORRECTAMENTE, POR FAVOR SELECCIONE UNA SECCIÓN"
              type="success"
            />
            <br>
            <el-button-group v-if="loadSections">
              <el-button type="primary" @click="chargeSection(1)">SECCIÓN 1</el-button>
              <el-button type="primary" @click="chargeSection(2)">SECCIÓN 2</el-button>
              <el-button type="primary" @click="chargeSection(3)">SECCIÓN 3</el-button>
              <el-button type="primary" @click="chargeSection(4)">SECCIÓN 4</el-button>
            </el-button-group>
          </div>
        </el-col>
      </el-row>
    </el-dialog>

    <el-dialog
      :visible.sync="reportDialogVisible"
      center
      title="PROTOCOLO DE SEROLOGIA"
      top="10px"
      width="100%"
    >
      <report-dialog v-if="!reportDialogLoading" :row="pdf" />
      <div v-if="reportDialogLoading" class="loading-report">
        <i class="el-icon-loading" style="font-size: 80px" />
      </div>
    </el-dialog>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import { printSerologyProtocol } from '@/api/serologyProtocol'
import { mapGetters } from 'vuex'
import UploadExcelComponent from '@/components/UploadExcel/index.vue'
import ReportDialog from '../report-dialog/ReportDialog'
import { debounce } from 'debounce'
import moment from 'moment'
import { defaultshorcouts } from '@/utils/date-utils'
import serologyProtocols from '../../query/serologyprotocol'
import { graphqlRequest } from '@/api/graphql'

const typeOptions = [
  { key: '0', display_name: 'CHAGAS WIENER' },
  { key: '1', display_name: 'CHAGAS BIOS CHILE' },
  { key: '2', display_name: 'HCV DIALAB' },
  { key: '3', display_name: 'HBsAg BIO-RAD ' },
  { key: '4', display_name: 'HIV BIO-RAD' },
  { key: '5', display_name: 'HAI-CHAGAS' },
  { key: '6', display_name: 'R.P.R. SIFILIS' },
  { key: '7', display_name: 'TPHA SIFILIS' }
]

const typeOptionsValue = typeOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'SerologyProtocol',
  components: { UploadExcelComponent, ReportDialog },
  filters: {
    typeOptionsFilter(type) {
      return typeOptionsValue[type]
    }
  },
  data() {
    return {
      pickerRangeOptions: {
        disabledDate(time) {
          return time.getTime() > Date.now()
        },
        shortcuts: defaultshorcouts()
      },
      pdf: null,
      reportDialogVisible: false,
      reportDialogLoading: false,
      index: 0,
      section1: [],
      section2: [],
      section3: [],
      section4: [],
      loadSections: false,
      tableExcel: null,
      tableKey: 0,
      typeOptions,
      list: null,
      typePatientLoading: true,
      typeHemocomponentLoading: true,
      typePatients: [],
      typeHemocomponents: [],
      total: null,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        offset: 0,
        search: '',
        ordering: '-register_at,-created_at',
        date_range: [moment().startOf('month').format('YYYY-MM-DD'), moment().format('YYYY-MM-DD')]
      },
      temp: {
        id: undefined,
        method: '',
        kit: '',
        due_date_at: moment().format('YYYY-MM-DD'),
        lot: '',
        industry: '',
        test: 1,
        type: '',
        values: [],
        section: null,
        cutt_off: '',
        cutt_off_min: '',
        cutt_off_max: '',
        register_at: moment().format('YYYY-MM-DD')
      },
      dialogFormVisible: false,
      dialogUploadVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Editando Protocolo de Serologia',
        create: 'Creando Protocolo de Serologia'
      },
      rules: {
        test: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }, {
          type: 'number',
          message: 'Debe ser número',
          trigger: 'blur'
        }],
        method: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        kit: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        lot: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        industry: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        data: [],
        type: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        due_date_at: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        register_at: [{ required: true, message: this.$t('is_required') }]
      },
      downloadLoading: false
    }
  },
  computed: {
    ...mapGetters([
      'employees',
      'employee_id'
    ])
  },
  watch: {
    'temp.type': function(value) {
      if (value !== null) {
        if (value === '0') {
          this.temp.values[0][0].value = 'CN'
          this.temp.values[1][0].value = 'CP'
          this.temp.values[2][0].value = ''
          this.temp.values[3][0].value = ''
        } else if (value === '1') {
          this.temp.values[0][0].value = 'CN1'
          this.temp.values[1][0].value = 'CN2'
          this.temp.values[2][0].value = 'CP1'
          this.temp.values[3][0].value = 'CP2'
        } else if (value === '2') {
          this.temp.values[0][0].value = 'B'
          this.temp.values[1][0].value = 'CN'
          this.temp.values[2][0].value = 'CP'
          this.temp.values[3][0].value = ''
        } else if (value === '3') {
          this.temp.values[0][0].value = 'CN1'
          this.temp.values[1][0].value = 'CN2'
          this.temp.values[2][0].value = 'CP1'
          this.temp.values[3][0].value = 'CP2'
        } else if (value === '4') {
          this.temp.values[0][0].value = 'CN1'
          this.temp.values[1][0].value = 'CN2'
          this.temp.values[2][0].value = 'CPAg'
          this.temp.values[3][0].value = 'CPAb'
        } else if (value === '5') {
          this.temp.values[0][0].value = 'CN'
          this.temp.values[1][0].value = 'CP'
          this.temp.values[2][0].value = ''
          this.temp.values[3][0].value = ''
        } else if (value === '6') {
          this.temp.values[0][0].value = 'CN'
          this.temp.values[1][0].value = 'CP'
          this.temp.values[2][0].value = ''
          this.temp.values[3][0].value = ''
        } else if (value === '7') {
          this.temp.values[0][0].value = 'CN'
          this.temp.values[1][0].value = 'CP'
          this.temp.values[2][0].value = ''
          this.temp.values[3][0].value = ''
        }
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    checkPermission,
    validate(value, i, j) {
      const charValue = value
      if (value !== '') {
        value = parseInt(value)
        if (isNaN(value)) {
          const valuePermits = ['CN', 'CP', 'CN1', 'CN2', 'CP1', 'CP2', 'CPAg', 'CPAb', 'CIN', 'CIP']
          if (!valuePermits.includes(charValue)) {
            this.$notify({
              title: 'Error',
              message: 'El dato ingresado no es valido',
              type: 'warning',
              duration: 5000
            })
            this.temp.values[i][j].value = ''
          }
        } else {
          for (let x = 0; x < 8; x++) {
            for (let y = 0; y < 12; y++) {
              if (parseInt(this.temp.values[x][y].value) === value && (x !== i || y !== j)) {
                this.$notify({
                  title: 'Error',
                  message: 'Registro duplicado, verifique por favor',
                  type: 'warning',
                  duration: 5000
                })
                this.temp.values[x][y].is_duplicated = true
              }
            }
          }
        }
      }
    },
    getFocus(col, row) {
      if (col === 12 && row === 7) {
        return
      }

      if (row === 7) {
        row = -1
        col = col + 1
      }
      const nextRef = 'comp' + col + '' + (row + 1)
      this.$refs[nextRef][0].$refs.input.focus()
    },
    beforeUpload(file) {
      const isLt1M = file.size / 1024 / 1024 < 1
      if (isLt1M) {
        return true
      }
      this.$message({
        message: 'Please do not upload files larger than 1m in size.',
        type: 'warning'
      })
      return false
    },
    handleSuccess({ results, header, fExcel, filename }) {
      this.tableExcel = fExcel
      const str = this.temp.test.toString()
      if (filename.indexOf(str) > -1) {
        let i = 0
        for (const key in this.tableExcel) {
          const value = this.tableExcel[key].w
          if (i > 23 && !isNaN(value) && i < 127) {
            this.section1.push(value)
          }
          if (i > 140 && !isNaN(value) && i < 257) {
            this.section2.push(value)
          }
          if (i > 257 && !isNaN(value) && i < 372) {
            this.section3.push(value)
          }
          if (i > 374 && !isNaN(value) && i < 487) {
            this.section4.push(value)
          }
          i++
        }
        this.loadSections = true
        console.log(this.section1)
        console.log(this.section2)
        console.log(this.section3)
        console.log(this.section4)
      } else {
        this.$notify({
          title: 'Nombre de Archivo Incorrecto',
          message: 'El nombre del archivo que desea subir no corresponde con el nombre del Protocolo de Serologia que esta creando por favor verifique',
          type: 'warning',
          duration: 5000
        })
      }
    },
    chargeSection(id) {
      let section
      if (id === 1) section = this.section1
      else if (id === 2) section = this.section2
      else if (id === 3) section = this.section3
      else if (id === 4) section = this.section4
      else section = null
      let k = 0
      if (section) {
        for (let i = 0; i < 8; i++) {
          for (let j = 0; j < 12; j++, k++) {
            this.temp.values[i][j].result_machine = section[k]
          }
        }
      }
      this.dialogUploadVisible = false
      this.loadSections = false
    },
    getList() {
      this.listLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'serologyprotocols',
          query: serologyProtocols.listSerologyProtocols(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.serologyprotocols.results
        this.total = data.serologyprotocols.totalCount
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
      const tempValues = []
      for (let x = 0; x < 8; x++) {
        const temRow = []
        for (let y = 0; y < 12; y++) {
          temRow.push({ value: '', result_machine: '', is_duplicated: false })
        }
        tempValues.push(temRow)
      }

      this.temp = {
        id: undefined,
        method: '',
        kit: '',
        due_date_at: moment().format('YYYY-MM-DD'),
        lot: '',
        industry: '',
        test: 1,
        values: tempValues,
        register_at: moment().format('YYYY-MM-DD')
      }
      const tempData = Object.assign({}, this.temp)
      this.temp = tempData
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      const tempData = Object.assign({}, this.temp)
      tempData.employee_id = this.employee_id
      this.temp = tempData
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
              service: 'createSerologyProtocol',
              query: serologyProtocols.createSerologyProtocol(),
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
      const tempData = Object.assign({}, row) // copy obj
      tempData.employee_id = tempData.employee.id
      this.temp = tempData
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
              service: 'updateSerologyProtocol',
              query: serologyProtocols.updateSerologyProtocol(),
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
            service: 'deleteSerologyProtocol',
            query: serologyProtocols.deleteSerologyProtocol(),
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
              message: 'Registro eliminado',
              type: 'success',
              duration: 2000
            })
          }
        })
      }).catch(() => {
        // cancel
      })
    },
    querySearchMethod(queryString, cb) {
      var links = [
        { 'value': 'ELISA' },
        { 'value': 'HAI-CHAGAS' },
        { 'value': 'RPR' },
        { 'value': 'TPHA' }
      ]
      var results = queryString ? links.filter(this.createFilter(queryString)) : links
      cb(results)
    },
    querySearchKit(queryString, cb) {
      var links = [
        { 'value': 'CHAGAS' },
        { 'value': 'VIH' },
        { 'value': 'HB' },
        { 'value': 'HCV' },
        { 'value': 'HAI-CHAGAS' },
        { 'value': 'RPR' },
        { 'value': 'TPHA' }
      ]
      var results = queryString ? links.filter(this.createFilter(queryString)) : links
      cb(results)
    },
    querySearchIndustry(queryString, cb) {
      var links = [
        { 'value': 'Austria' },
        { 'value': 'France' },
        { 'value': 'Santiago,Chile' },
        { 'value': 'Argentina' },
        { 'value': 'Spain' }
      ]
      var results = queryString ? links.filter(this.createFilter(queryString)) : links
      cb(results)
    },
    createFilter(queryString) {
      return (link) => {
        return (link.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0)
      }
    },
    handlePrintSerologyProtocol(row) {
      this.reportDialogVisible = true
      this.reportDialogLoading = true
      this.temp = Object.assign({}, row)
      printSerologyProtocol(this.temp.id).then(
        response => {
          this.pdf = response
          this.reportDialogLoading = false
        }
      )
    }
  }
}
</script>
<style>
  .title{
    font-weight: bold !important;
    font-size: 20px !important;
    vertical-align: middle;
  }
  .error input{
    color: red;
  }
  .el-autocomplete{
    display: block;
  }
</style>

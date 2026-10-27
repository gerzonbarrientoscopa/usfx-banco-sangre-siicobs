<template>
  <div class="app-container">
    <div class="filter-container">
      <el-row :gutter="20">
        <el-col :md="20">
          <div class="block">
            <div class="demonstration">Fecha Inicial / Fecha Final</div>
            <el-date-picker
              v-model="listQuery.date_range"
              :picker-options="pickerOptions"
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
        v-if="checkPermission(['add_selfexclusion'])"
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
      <el-table-column :label="$t('models.donor.register_at')" align="center" fixed width="140px">
        <template slot-scope="scope">
          <span>{{ scope.row.register_at | toHumanDate }}</span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.donor.code')" align="center" width="120px">
        <template slot-scope="scope">
          <span><strong>{{ scope.row.extraction.donation.donor.code }}</strong></span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.donation.employee')" align="center">
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
          <el-button v-if="checkPermission(['change_selfexclusion'])" size="mini" @click="handleUpdate(scope.row)">{{ $t('edit') }}</el-button>
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
      <el-row :gutter="20">
        <el-col :md="12">
          <el-form
            ref="dataForm"
            :model="temp"
            :rules="rules"
            label-position="right"
            label-width="180px"
            style="width: 100%;"
          >
            <div class="grid-content">
              <el-form-item :label="$t('models.extraction.donation')" prop="extraction_id">
                <el-select
                  v-if="dialogStatus === 'create'"
                  v-model="temp.extraction_id"
                  :loading="loadingExtraction"
                  :placeholder="$t('please_select')"
                  :remote-method="remoteMethodExtraction"
                  automatic-dropdown
                  class="filter-item"
                  filterable
                  remote
                >
                  <el-option
                    v-for="item in extractions"
                    :key="item.id"
                    :label="item.donation.donor.code"
                    :value="item.id"
                  >
                    <span style="float: left"><strong>{{ item.donation.donor.code }}</strong></span>
                    <span style="float: right; color: #8492a6; font-size: 13px">{{ item.donation.register_at| toHumanDateMonthLetter }}</span>
                  </el-option>
                </el-select>
                <span v-if="dialogStatus === 'update'" class="text-text-turquoise" style="font-weight: bolder">
                  {{ temp.extraction.donation.donor | donorCodeFullName }}
                </span>
              </el-form-item>
              <el-form-item :label="$t('models.extraction.register_at')" prop="register_at">
                <el-date-picker
                  v-model="temp.register_at"
                  :placeholder="$t('models.extraction.register_at')"
                  format="dd-MM-yyyy"
                  type="date"
                  value-format="yyyy-MM-dd"
                />
              </el-form-item>

              <el-form-item :label="$t('models.extraction.observations')" prop="observations">
                <el-input v-model="temp.observations" :rows="2" type="textarea" @input.native="setUpperCase(temp, 'observations', $event)" />
              </el-form-item>
              <el-form-item :label="$t('models.extraction.employee')" prop="employee_id">
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
            </div>
          </el-form>
        </el-col>
      </el-row>

      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">{{ $t('cancel') }}</el-button>
        <el-button @click="dialogStatus==='create'?createData():updateData()">{{ $t('confirm') }}</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import { mapGetters } from 'vuex'
import { graphqlRequest } from '@/api/graphql'
import selfExclusion from '@/query/selfExclusion'
import extractions from '@/query/extraction'
import { debounce } from 'debounce'
import moment from 'moment'

export default {
  name: 'SelfExclusion',
  data() {
    return {
      pickerOptions: {
        disabledDate(time) {
          return time.getTime() > Date.now()
        },
        shortcuts: [{
          text: 'Mes Actual',
          onClick(picker) {
            const start = moment().startOf('month').format('YYYY-MM-DD')
            const end = moment().format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
          }
        }, {
          text: 'Mes Anterior',
          onClick(picker) {
            const start = moment().subtract(1, 'months').startOf('month').format('YYYY-MM-DD')
            const end = moment().subtract(1, 'months').endOf('month').format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
          }
        }, {
          text: 'Año Actual',
          onClick(picker) {
            var thisYear = (new Date()).getFullYear()
            var startDate = new Date('1/1/' + thisYear)
            const start = moment(startDate.valueOf()).format('YYYY-MM-DD')
            const end = moment().format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
          }
        }]
      },
      pdf: null,
      reportDialogVisible: false,
      reportDialogLoading: false,
      tableKey: 0,
      extractions: null,
      donation: {
        donor: null,
        place: null
      },
      list: null,
      total: null,
      loading: false,
      listLoading: true,
      listExtractionQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-id' },
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
        observations: '',
        employee_id: undefined,
        register_at: moment().format('YYYY-MM-DD')
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Editando',
        create: 'Creando'
      },
      // datos de rechazo
      rules: {
        register_at: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        extraction_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        observations: [],
        employee_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }]
      },
      downloadLoading: false,
      loadingExtraction: false
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
    getListExtractions() {
      this.loadingExtraction = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'selfexclusions',
          query: extractions.selfExclusionExtractionSelect(this.listExtractionQuery)
        }
      ).then(response => {
        const data = response.data
        this.extractions = data.extractions.results
        this.loadingExtraction = false
      })
    },
    remoteMethodExtraction(query) {
      if (query !== '') {
        this.listExtractionQuery.search = query
      } else {
        this.listExtractionQuery.search = ''
      }
      this.getListExtractions()
    },
    getList() {
      this.listLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          query: selfExclusion.listSelfExclusion(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.selfexclusions.results
        this.total = data.selfexclusions.totalCount
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
        message: '操作成功',
        type: 'success'
      })
      row.status = status
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        extraction_id: undefined,
        observations: '',
        employee_id: undefined,
        register_at: moment().format('YYYY-MM-DD')
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.getListExtractions()

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
          tempData.register_id = this.employee_id
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'createSelfExclusion',
              query: selfExclusion.createSelfExclusion(),
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
      const tempData = Object.assign({}, row)
      tempData.extraction_id = tempData.extraction.id
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
          tempData.register_id = this.employee_id
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'updateSelfExclusion',
              query: selfExclusion.updateSelfExclusion(),
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

<template>
  <div class="app-container">
    <el-form
      ref="dataForm"
      :model="temp"
      :rules="rules"
      label-position="left"
      label-width="160px"
      style="width: 100%;"
    >
      <el-row :gutter="20">
        <el-col :md="24" :sm="24">
          <div class="grid-content">
            <el-table
              :data="temp.itemfragmentations"
              style="width: 100%"
            >
              <el-table-column
                label="Tipo de Hemocomponente"
              >
                <template slot-scope="scope">
                  <span>{{ scope.row.itemfragmentation.typehemocomponent.name }}</span>
                </template>
              </el-table-column>
              <el-table-column
                label="Fecha de Expiración"
              >
                <template slot-scope="scope">
                  <span>{{ scope.row.itemfragmentation.expiration_date | toHumanDatetime }}</span>
                </template>
              </el-table-column>
              <el-table-column
                label="Volumen"
              >
                <template slot-scope="scope">
                  <span>{{ scope.row.itemfragmentation.weight }} ml.</span>
                </template>
              </el-table-column>
              <el-table-column
                :label="$t('actions')"
                align="center"
                class-name="small-padding"
                fixed="right"
                width="250"
              >
                <template slot-scope="scope">
                  <el-button size="mini" @click="handleRemove(scope.$index, scope.row)">Quitar {{ scope.rowIndex }}</el-button>
                </template>
              </el-table-column>
            </el-table>
            <br>
            <el-form-item>
              <el-button @click="handleShowItemDialog()">
                Agregar Items
              </el-button>
              <el-button @click="updateData()">
                {{ $t('confirm') }}
              </el-button>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
    </el-form>
    <el-dialog
      :visible.sync="innerVisible"
      append-to-body
      destroy-on-close
      title="Hemocomponentes"
      width="90%"
    >
      <div class="filter-container">
        <el-row :gutter="10" style="width: 100%">
          <el-col :md="8">
            <el-select
              v-model="listQuery.typehemocomponent_id"
              :loading="typeHemocomponentLoading"
              :remote-method="remoteMethod"
              automatic-dropdown
              class="filter-item"
              clearable
              filterable
              placeholder="Tipo de Hemocomponente"
              remote
              @change="handleShowItemDialog()"
            >
              <el-option
                v-for="item in typeHemocomponents"
                :key="item.id"
                :label="item.name "
                :value="item.id"
              />
            </el-select>
          </el-col>
          <el-col :md="16">
            <el-input
              v-model.lazy="listQuery.search"
              :autofocus="'autofocus'"
              :placeholder="'Buscar'"
              class="filter-item"
              clearable
              prefix-icon="el-icon-search"
              style="width: 100%;"
              @input="handleFilter"
            />
          </el-col>
        </el-row>
      </div>
      <el-table
        :data="itemFragmentations"
        style="width: 100%"
      >
        <el-table-column
          label="Codigo"
          width="150"
        >
          <template slot-scope="scope">
            <span><strong>{{ scope.row.donor_code }}</strong></span>
          </template>
        </el-table-column>
        <el-table-column
          label="Tipo de Hemocomponente"
        >
          <template slot-scope="scope">
            <span>{{ scope.row.typehemocomponent.name }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="Fecha de Expiración"
          width="170"
        >
          <template slot-scope="scope">
            <span>{{ scope.row.expiration_date | toHumanDatetime }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="Tubuladura"
          width="150"
        >
          <template slot-scope="scope">
            <span>{{ scope.row.fragmentation.extraction.tubing }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="Volumen"
          width="150"
        >
          <template slot-scope="scope">
            <span>{{ scope.row.weight }} ml.</span>
          </template>
        </el-table-column>
        <el-table-column
          :label="$t('actions')"
          align="center"
          class-name="small-padding"
          fixed="right"
          width="150"
        >
          <template slot-scope="scope">
            <el-button size="mini" @click="handleAddItem(scope.$index, scope.row)">Agregar</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination-container">
        <el-pagination
          v-show="total>0"
          :current-page="listQuery.page"
          :page-size="listQuery.limit"
          :page-sizes="[10, 20, 30, 50]"
          :total="total"
          background
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-dialog>

  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import distributions from '@/query/distribution'
import { debounce } from 'debounce'
import { graphqlRequest } from '@/api/graphql'
import itemFragmentations from '@/query/itemFragmentation'
import typehemocomponents from '@/query/type-hemocomponent'

export default {
  name: 'DistributionItemForms',
  props: {
    row: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      isEdit: false,
      tableKey: 0,
      patients: null,
      medicals: null,
      institutions: null,
      list: null,
      total: null,
      loading: false,
      listLoading: true,
      institutionLoading: false,
      patientLoading: false,
      medicalLoading: false,
      listPatientQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-id' },
      listMedicalQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-id' },
      listInstitutionQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-id' },
      listQuery: { page: 1, limit: 50, offset: 0, search: '', ordering: '-id', typehemocomponent_id: '' },
      temp: {
        id: undefined,
        employee_id: undefined,
        extraction_id: undefined,
        patient_id: undefined,
        medical_id: undefined,
        institution_id: undefined,
        itemfragmentations: [],
        service_transfunctional: '',
        observations: '',
        type_payment: ''
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Editando Distribucion',
        create: 'Creando Distribucion'
      },
      rules: { },
      downloadLoading: false,
      totalHC: 0,
      innerVisible: false,
      itemFragmentations: [],
      typeHemocomponents: [],
      typeHemocomponentLoading: false,
      listTypeHemocomponentQuery: { page: 1, limit: 20, title: undefined, offset: 0, search: '', ordering: '-name' }
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
      this.determineAction()
    }
  },
  mounted() {
    this.determineAction()
  },
  methods: {
    determineAction() {
      this.handleUpdate(this.row)
    },
    getListTypeHemocomponents() {
      this.typeHemocomponentLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'typehemocomponents',
          query: typehemocomponents.package_select(this.listTypeHemocomponentQuery)
        }
      ).then(response => {
        const data = response.data
        this.typeHemocomponents = data.typehemocomponents.results
        this.typeHemocomponentLoading = false
      })
    },
    remoteMethod(query) {
      if (query !== '') {
        this.listTypeHemocomponentQuery.search = query
      } else {
        this.listTypeHemocomponentQuery.search = ''
      }
      this.getListTypeHemocomponents()
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        employee_id: undefined,
        extraction_id: undefined,
        patient_id: undefined,
        medical_id: undefined,
        institution_id: undefined,
        itemfragmentations: []
      }
    },
    handleUpdate(row) {
      const tempData = { id: row.id }
      if (!tempData.itemfragmentations) tempData.itemfragmentations = []
      this.temp = tempData
      this.dialogStatus = 'update'
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          if (this.temp.itemfragmentations.length === 0) {
            this.$confirm('No hay Hemocomponentes. Desea continuar?', 'Warning', {
              confirmButtonText: 'Si, Estoy Seguro',
              cancelButtonText: 'Cancelar',
              type: 'warning'
            }).then(() => {
              this.updateItemDistribution()
            }).catch(() => {
              this.$message({
                type: 'info',
                message: 'Por favor agregue hemocomponentes'
              })
            })
          } else {
            this.updateItemDistribution()
          }
        }
      })
    },
    formattedItemDistribution(tempData) {
      const newListMenus = []
      tempData.itemfragmentations.forEach(function(obj, idx) {
        newListMenus.push({ id: obj.itemfragmentation.id })
      })
      return newListMenus
    },
    updateItemDistribution() {
      const tempData = Object.assign({}, this.temp)
      tempData.itemfragmentations = this.formattedItemDistribution(tempData)
      tempData.status = 'IN_PROGRESS'

      graphqlRequest(
        {
          from: this.$route.name,
          query: distributions.updateDistribution(),
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
          this.$emit('dialogStatus', false)
          this.$emit('distribution', response)
          this.resetTemp()
          this.$notify({
            title: 'Estado',
            message: 'Se ha actualizado',
            type: 'success',
            duration: 2000
          })
          this.$router.replace({ path: '/distributions' })
        }
      })
    },
    handleAddItem(index, row) {
      const tempData = Object.assign({}, this.temp)
      tempData.itemfragmentations.push({ itemfragmentation: row })
      this.temp = tempData
      delete this.itemFragmentations.splice(index, 1)
    },
    handleRemove(index, row) {
      var tempData = Object.assign({}, this.temp)
      var newItems = []
      var oldItems = tempData.itemfragmentations
      oldItems.forEach(function(obj, idx) {
        if (index !== idx) {
          newItems.push(obj)
        }
      })
      tempData.itemfragmentations = newItems
      this.temp = tempData
    },
    handleShowItemDialog() {
      this.getListTypeHemocomponents()
      this.listLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'distributions',
          query: itemFragmentations.listAddingDistributions(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.itemFragmentations = data.itemfragmentations.results
        this.total = data.itemfragmentations.totalCount
        this.innerVisible = true

        const tempData = Object.assign({}, this.temp)
        const newListItems = []

        this.itemFragmentations.forEach(function(obj, idx) {
          const findItemAdded = tempData.itemfragmentations.filter(element => element.itemfragmentation.id === obj.id)
          if (findItemAdded.length === 0) {
            newListItems.push(obj)
          }
        })
        this.itemFragmentations = newListItems

        this.listLoading = false
      })
    },
    handleFilter: debounce(function(e) {
      this.listQuery.page = 1
      this.handleShowItemDialog()
    }, 500),
    handleSizeChange(val) {
      this.listQuery.limit = val
      this.handleShowItemDialog()
    },
    handleCurrentChange(val) {
      this.listQuery.page = val
      this.listQuery.offset = this.listQuery.limit * (val - 1)
      this.handleShowItemDialog()
    }
  }
}
</script>

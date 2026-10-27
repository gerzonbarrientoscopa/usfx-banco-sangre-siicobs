<template>
  <div>
    <div class="app-container">
      <el-row :gutter="20">
        <el-col :md="24" :sm="24">
          <div class="grid-content">
            <div class="createPost-container">
              <el-form
                ref="dataForm"
                :model="temp"
                :rules="rules"
                label-position="right"
                label-width="200px"
                style="width: 100%;"
              >
                <el-row :gutter="20">
                  <el-col :md="12" :sm="12">
                    <div class="grid-content">
                      <el-form-item :label="$t('models.fragmentation.donation')" prop="extraction_id">
                        <el-select
                          v-if="!isEdit"
                          v-model="temp.extraction_id"
                          :loading="loading"
                          :placeholder="$t('please_select')"
                          :remote-method="remoteMethod"
                          automatic-dropdown
                          class="filter-item"
                          filterable
                          remote
                          @change="getExtraction(temp.extraction_id)"
                        >
                          <el-option
                            v-for="item in extractions"
                            :key="item.id"
                            :label="item.donation.donor.code"
                            :value="item.id"
                          >
                            <span style="float: left"><strong>{{ item.donation.donor.code }}</strong></span>
                            <span
                              style="float: right; color: #8492a6; font-size: 13px"
                            >&nbsp;[{{ item.hours_past }} Hrs.]</span>
                            <span style="float: right; color: #8492a6; font-size: 13px">{{ item.donation.register_at| toHumanDateMonthLetter }}</span>
                          </el-option>
                        </el-select>
                        <span v-if="isEdit" class="text-text-turquoise" style="font-weight: bolder">
                          {{ temp.donor_code }}<br> Extracción:
                          <span style="color: #8492a6; font-size: 13px">{{ temp.extraction.register_at| toHumanDateMonthLetter }}</span>
                        </span>
                      </el-form-item>
                      <el-form-item :label="$t('models.fragmentation.quality_bag')" prop="quality_bag">
                        <el-radio-group v-model="temp.quality_bag" class="el-row--flex">
                          <el-radio-button v-for="item in qualityBagOptions" :key="item.key" :label="item.key">
                            {{ item.display_name }}
                          </el-radio-button>
                        </el-radio-group>
                      </el-form-item>
                    </div>
                  </el-col>
                  <el-col :md="12" :sm="12">
                    <div class="grid-content">
                      <el-form-item :label="$t('models.fragmentation.register_at')" prop="register_at">
                        <el-date-picker
                          v-model="temp.register_at"
                          :picker-options="dateTimePickerOptions"
                          format="dd-MM-yyyy HH:mm"
                          placeholder="Seleccione fecha y hora"
                          type="datetime"
                          value-format="yyyy-MM-dd HH:mm"
                        />
                      </el-form-item>

                      <el-form-item :label="$t('models.fragmentation.total_hc')" prop="total_hc">
                        <el-input-number
                          v-model.number="temp.total_hc"
                          :min="extraction != null ? extraction.bags_quantity: 0"
                          type="number"
                          @change="updateItemsFromBagsQuantity"
                        >
                          <template slot="append">total</template>
                        </el-input-number>
                      </el-form-item>
                    </div>
                  </el-col>
                </el-row>
                <el-form-item :label="$t('models.fragmentation.observations')" prop="observations">
                  <el-input v-model="temp.observations" :rows="2" type="textarea" @input.native="setUpperCase(temp, 'observations', $event)" />
                </el-form-item>
                <el-table
                  :data="temp.itemfragmentations"
                  style="width: 100%"
                >
                  <el-table-column
                    type="index"
                    width="30"
                  />
                  <el-table-column label="Hemocomponente" width="300px">
                    <template slot-scope="scope">
                      <el-select
                        v-model="temp.itemfragmentations[scope.$index].typehemocomponent_id"
                        :disabled="isEdit && !checkPermission(['changetype_itemfragmentation'])"
                        :placeholder="$t('please_select')"
                        automatic-dropdown
                        class="filter-item"
                        clearable
                        filterable
                        @change="setTypeHemocomponent(scope)"
                      >
                        <el-option
                          v-for="item in items"
                          :key="item.id"
                          :label="item.name"
                          :value="item.id"
                        >
                          <span style="float: left"><strong>{{ item.name }}</strong></span>
                        </el-option>
                      </el-select>
                    </template>
                  </el-table-column>

                  <el-table-column align="center" label="Fecha de Expiracion" width="250px">
                    <template slot-scope="scope">
                      <el-form-item label-width="0px" style="margin-bottom: 0">
                        <el-date-picker
                          v-model="scope.row.expiration_date"
                          :clearable="false"
                          :default-value="temp.register_at"
                          :disabled="scope.row.typehemocomponent_id === null || scope.row['typehemocomponent_id'] === 16"
                          :editable="false"
                          :picker-options="pickerRangeOptions"
                          :readonly=" !scope.row.is_max_expiration_days"
                          default-time="00:00"
                          format="dd-MM-yyyy HH:mm"
                          type="datetime"
                          @focus="buildDateRange(scope)"
                        />
                      </el-form-item>
                    </template>
                  </el-table-column>
                  <el-table-column label="Peso (Volumen ml.)" width="150px">
                    <template slot-scope="scope">
                      <el-form-item label-width="0px" style="margin-bottom: 0">
                        <el-input-number
                          v-model.number="scope.row.weight"
                          :disabled="scope.row.typehemocomponent.id === 16"
                          :min="0"
                          :precision="2"
                          :step="0.1"
                          size="small"
                        />
                      </el-form-item>
                    </template>
                  </el-table-column>
                  <el-table-column label="Descarte" width="250px">
                    <template slot-scope="scope">
                      <el-select
                        v-model="temp.itemfragmentations[scope.$index].typediscard_id"
                        :placeholder="$t('please_select')"
                        automatic-dropdown
                        class="filter-item"
                        clearable
                        filterable
                        @change="setTypeDiscard(scope)"
                      >
                        <el-option
                          v-for="item in temp.itemfragmentations[scope.$index].typediscards"
                          :key="item.id"
                          :label="item.name"
                          :value="item.id"
                        >
                          <span style="float: left"><strong>{{ item.name }}</strong></span>
                        </el-option>
                      </el-select>
                    </template>
                  </el-table-column>
                  <el-table-column label="Observaciones">
                    <template slot-scope="scope">
                      <el-form-item label-width="0px" prop="observations" style="margin-bottom: 0">
                        <el-input v-model="scope.row.observations" :rows="2" type="textarea" @input.native="setUpperCase(scope.row, 'observations', $event)" />
                      </el-form-item>
                    </template>
                  </el-table-column>
                  <el-table-column
                    v-if="isEdit && temp.total_hc < temp.itemfragmentations.length"
                    align="center"
                    class-name="small-padding"
                    fixed="right"
                    width="50px"
                  >
                    <template slot-scope="scope">
                      <el-tooltip class="item" content="Quitar de la lista" effect="dark">
                        <el-button
                          circle
                          icon="el-icon-delete"
                          size="mini"

                          @click="handleRemove(scope.$index, scope.row)"
                        />
                      </el-tooltip>
                    </template>
                  </el-table-column>
                </el-table>
                <br>
                <el-form-item>
                  <el-button @click="isEdit ? updateData() : createData()">
                    {{ $t('confirm') }}
                  </el-button>
                </el-form-item>
              </el-form>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import checkPermission from '@/utils/permission'
import Moment from 'moment'
import { extendMoment } from 'moment-range'
const moment = extendMoment(Moment)
import { graphqlRequest } from '@/api/graphql'
import extractions from '@/query/extraction'
import fragmentations from '@/query/fragmentation'
import typehemocomponents from '@/query/type-hemocomponent'
import { TYPE_PROCESS } from '@/utils/const'

const qualityBagOptions = [
  { key: 'AP', display_name: 'APTO' },
  { key: 'NA', display_name: 'NO APTO' }
]
export default {
  name: 'FragmentationForm',
  directives: {},
  props: {
    row: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      TYPE_PROCESS,
      pickerRangeOptions: {
        disabledDate: this.disabledDate
      },
      dateTimePickerOptions: {
        shortcuts: [{
          text: 'Hoy',
          onClick(picker) {
            picker.$emit('pick', new Date())
          }
        }, {
          text: 'Ayer',
          onClick(picker) {
            const date = new Date()
            date.setTime(date.getTime() - 3600 * 1000 * 24)
            picker.$emit('pick', date)
          }
        }, {
          text: 'Hace una semana',
          onClick(picker) {
            const date = new Date()
            date.setTime(date.getTime() - 3600 * 1000 * 24 * 7)
            picker.$emit('pick', date)
          }
        }]
      },
      isEdit: false,
      tableKey: 0,
      extractions: null,
      extraction: null,
      list: null,
      total: null,
      loading: false,
      listLoading: true,
      typeHemocomponentLoading: false,
      listExtractionQuery: {
        page: 1,
        limit: 20,
        search: '',
        offset: 0,
        ordering: '-id',
        from: 'FRA'
      },
      listTypeHemocomponentQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-name' },
      qualityBagOptions,
      listQuery: {
        page: 1,
        limit: 20,
        search: undefined,
        ordering: '-id'
      },
      temp: {
        id: undefined,
        employee: undefined,
        extraction: {
          hours_past: 1
        },
        itemfragmentations: [],
        total_hc: 0,
        quantity: 0,
        expiration_date: '',
        observations: '',
        quality_bag: '',
        register_at: new Date(),
        donor_code: undefined,
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Editando Fraccionamiento',
        create: 'Creando Fraccionamiento'
      },
      rules: {
        extraction_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        quality_bag: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        register_at: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        total_hc: [{ required: true, trigger: 'blur' }, { type: 'number', message: 'Debe ser número' }],
        observations: [{ trigger: 'blur' }],
      },
      itemLoading: false,
      listItemQuery: { page: 1, limit: 20, search: undefined, ordering: 'position, name', only_fragmentation: true },
      downloadLoading: false,
      totalHC: 0,
      items: [],
      innerVisible: false,
      action: '',
      isForApheresis: false,
      init_date: '',
      end_date: ''
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
    },
  },
  mounted() {
    this.determineAction()
  },
  methods: {
    checkPermission,
    determineAction() {
      if (this.row != null) {
        this.getFragmentation(this.row.id)
        this.extraction = this.row.extraction
        this.isEdit = true
      } else {
        this.handleCreate()
        this.isEdit = false
      }
    },
    validateTypeProcess(extraction) {
      if (extraction.donation && extraction.donation.type_process === 'NA') {
        this.isForApheresis = true
      } else {
        this.isForApheresis = false
      }
    },
    getFragmentation(id) {
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'fragmentations',
          query: fragmentations.get(id)
        }
      ).then(response => {
        const data = response.data
        this.handleUpdate(data.fragmentation)
      })
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        employee: undefined,
        quality_bag: '',
        extraction: {
          hours_past: 1
        },
        itemfragmentations: [],
        total_hc: 0,
        quantity: 0,
        observations: '',
        expiration_date: '',
        register_at: new Date(),
        donor_code: undefined,
      }
    },
    getExtraction(id) {
      const extraction = this.extractions.filter(function(item) {
        return item.id === id
      })
      this.extraction = extraction[0]
      this.buildItems()
      this.validateTypeProcess(extraction[0])
    },
    getListExtraction() {
      this.listLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          query: extractions.fragmentationExtractionSelect(this.listExtractionQuery)
        }
      ).then(response => {
        const data = response.data
        this.extractions = data.extractions.results
        const listFiltered = []
        for (const extraction of this.extractions) {
          const date1 = moment(extraction.register_at)
          const date2 = moment(new Date())
          extraction['hours_past'] = date2.diff(date1, 'hours')
          listFiltered.push(extraction)
        }
        this.extractions = listFiltered
        this.listLoading = false
      })
    },
    remoteMethod(query) {
      if (query !== '') {
        this.listExtractionQuery.search = query
      } else {
        this.listExtractionQuery.search = ''
      }
      this.getListExtraction()
    },
    handleCreate() {
      this.action = 'create'
      this.resetTemp()
      this.getListTypeHemocomponents()
      this.getListExtraction()

      const tempData = Object.assign({}, this.temp)
      tempData.employee_id = this.employee_id
      this.temp = tempData

      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      if (!this.validatorFragmentationItems() || !this.validatorSatelliteBag()) {
        return
      }
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.register_id = this.employee_id
          tempData.donor_code = this.extraction.donation.donor.code
          tempData.register_at = moment(tempData.register_at)
          this.verifyVoidBagData(tempData)
        }
      })
    },
    verifyVoidBagData(tempData) {
      const voidBag = tempData.itemfragmentations.filter(function(item) {
        return item.typehemocomponent_id === 16
      })
      if (voidBag[0]) {
        if (voidBag[0].observations === '') {
          this.$notify({
            title: 'Seleccionaste una Bolsa Vacia',
            message: 'Por favor llene el campo Observacion de la Bolsa Vacia',
            type: 'warning',
            duration: 4000
          })
        } else if (voidBag[0].typediscard_id === null) {
          this.$notify({
            title: 'Seleccionaste una Bolsa Vacia',
            message: 'Por favor selecciona un Tipo de Descarte de la Bolsa Vacia',
            type: 'warning',
            duration: 4000
          })
        } else {
          if (this.action === 'create') {
            this.createFragmentationData(tempData)
          } else {
            this.updateFragmentationData(tempData)
          }
        }
      } else {
        if (this.action === 'create') {
          this.createFragmentationData(tempData)
        } else {
          this.updateFragmentationData(tempData)
        }
      }
    },
    handleUpdate(row) {
      this.action = 'update'
      const tempData = Object.assign({}, row)
      tempData.extraction_id = tempData.extraction.id
      tempData.employee_id = tempData.employee.id
      tempData.register_at = new Date(tempData.register_at)
      this.temp = tempData
      this.checkQuantityBagsExtraction(tempData)
      this.getListTypeHemocomponents()
      this.validateTypeProcess(tempData.extraction)
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    checkQuantityBagsExtraction(tempData) {
      if (tempData.extraction.bags_quantity !== tempData.total_hc) {
        const quantity = tempData.extraction.bags_quantity - tempData.total_hc
        for (var i = 0; i < quantity; i++) {
          tempData.itemfragmentations.push({
            typehemocomponent_id: null,
            typediscard_id: null,
            typehemocomponent: {},
            is_satellite_bag: true,
            quantity: 1,
            expiration_date: '',
            is_max_expiration_days: false,
            weight: 0,
            observations: '',
            lot: '',
          })
        }
        if (tempData.itemfragmentations.length === tempData.total_hc) {
          tempData.total_hc = tempData.itemfragmentations.length
        } else {
          tempData.total_hc = tempData.extraction.bags_quantity
          this.temp = tempData
          if (quantity < 0) {
            this.$notify({
              title: 'Mensaje',
              message: 'Por favor actualice los hemocomponentes hubo cambios en la extraccion ha disminuido la cantidad de bolsas',
              type: 'warning',
              duration: 4000
            })
          } else {
            this.$notify({
              title: 'Mensaje',
              message: 'Por favor actualice los hemocomponentes hubo cambios en la extraccion ha aumentado la cantidad de bolsas',
              type: 'warning',
              duration: 4000
            })
          }
        }
      }
    },
    updateData() {
      if (!this.validatorFragmentationItems() || !this.validatorSatelliteBag()) {
        return
      }
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.register_id = this.employee_id
          tempData.donor_code = this.temp.extraction.donation.donor.code
          tempData.register_at = moment(tempData.register_at)
          this.verifyVoidBagData(tempData)
        }
      })
    },
    createFragmentationData(tempData) {
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'createFragmentation',
          query: fragmentations.createFragmentation(),
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
          this.resetTemp()
          this.$notify({
            title: 'Estado',
            message: 'Registro creado',
            type: 'success',
            duration: 2000
          })
          this.$emit('dialogStatus', false)
        }
      })
    },
    updateFragmentationData(tempData) {
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'updateFragmentation',
          query: fragmentations.updateFragmentation(),
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
          this.$notify({
            title: 'Estado',
            message: 'Registro actualizado',
            type: 'success',
            duration: 2000
          })
          this.$emit('dialogStatus', false)
        }
      })
    },
    validatorFragmentationItems() {
      if (this.temp.itemfragmentations.length === 0) {
        this.$notify({
          title: 'Estado',
          message: 'Necesitas agregar al menos un item',
          type: 'warning',
          duration: 2000
        })
        return false
      } else {
        let cont = 0
        this.temp.itemfragmentations.forEach(function(obj) {
          if (obj.typehemocomponent_id == null) {
            cont++
          }
        })
        if (cont > 0) {
          this.$notify({
            title: 'No ha seleccionado hemocomponentes',
            message: 'Por favor seleccione los hecomponentes',
            type: 'error',
            duration: 2000
          })
          return false
        } else {
          return true
        }
      }
    },
    validatorSatelliteBag() {
      if (!this.isForApheresis) {
        let cont = 0
        this.temp.itemfragmentations.forEach(function(obj) {
          if (obj.is_satellite_bag === false) {
            cont++
          }
        })
        if (cont === 0) {
          this.$notify({
            title: 'No ha seleccionado Bolsa Madre',
            message: 'Por favor seleccione un Hemocomponente como Bolsa Madre',
            type: 'error',
            duration: 2000
          })
          return false
        } else {
          return true
        }
      } else {
        var newList = []
        this.temp.itemfragmentations.forEach(function(obj) {
          obj.is_satellite_bag = null
          newList.push(obj)
        })
        this.temp.itemfragmentations = newList
        return true
      }
    },
    buildItems() {
      const tempData = Object.assign({}, this.temp)
      tempData.itemfragmentations = []
      if (this.extraction) {
        for (var i = 0; i < this.extraction.bags_quantity; i++) {
          const isb = i !== 0
          tempData.itemfragmentations.push({
            typehemocomponent_id: null,
            typediscard_id: null,
            typehemocomponent: {},
            is_satellite_bag: isb,
            quantity: 1,
            expiration_date: '',
            is_max_expiration_days: false,
            weight: 0,
            observations: '',
            lot: '',
          })
        }
      }

      tempData.total_hc = tempData.itemfragmentations.length
      this.temp = tempData
    },
    updateItemsFromBagsQuantity() {
      var tempData = Object.assign({}, this.temp)
      if (this.extraction && this.extraction.bags_quantity !== tempData.total_hc) {
        let quantity = tempData.total_hc - tempData.itemfragmentations.length
        if (tempData.itemfragmentations.length < tempData.total_hc) {
          for (let i = 0; i < quantity; i++) {
            tempData.itemfragmentations.push({
              typehemocomponent_id: null,
              typediscard_id: null,
              typehemocomponent: {},
              is_satellite_bag: true,
              quantity: 1,
              expiration_date: '',
              is_max_expiration_days: false,
              weight: 0,
              observations: '',
              lot: '',
            })
          }
        } else {
          quantity = -(quantity)
          for (let j = 0; j <= quantity; j++) {
            tempData.itemfragmentations.pop()
          }
        }
        this.temp = tempData
      }
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
    getListTypeHemocomponents() {
      this.typeHemocomponentLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'typehemocomponents',
          query: typehemocomponents.fragmentation_select(this.listTypeHemocomponentQuery)
        }
      ).then(response => {
        const data = response.data
        this.items = data.typehemocomponents.results
        this.typeHemocomponentLoading = false

        if (this.isEdit) {
          this.setTypeHemocomponents()
        }
      })
    },
    setTypeHemocomponents() {
      const tempData = Object.assign({}, this.temp)
      let index = 0
      for (const obj of tempData.itemfragmentations) {
        obj.typehemocomponent_id = obj.typehemocomponent.id
        obj.typediscards = this.setListTypeDiscard(obj)
        obj.typediscard_id = obj.typediscard ? obj.typediscard.id : undefined
        let expirationDate = null
        const register_at = moment(this.extraction.register_at)
        const date_now = moment(obj.expiration_date).format()
        expirationDate = moment(register_at.format()).add(obj.typehemocomponent.expiration_day, 'days')
        expirationDate = expirationDate.format()

        if (date_now.substring(0, 10) !== expirationDate.substring(0, 10)) {
          tempData.itemfragmentations[index]['expiration_date'] = expirationDate
          this.$notify({
            dangerouslyUseHTMLString: true,
            title: 'Mensaje',
            message: '<p>La fecha de expiración del hemocomponente ' + obj.typehemocomponent.name +
              ' no coincide con la fecha real de expiración adecuada de ' + obj.typehemocomponent.expiration_day +
              'días, por favor ' +
              'presiona en <b style="color:black">CONFIRMAR</b> para corregir</p>',
            type: 'error',
            duration: 6000
          })
        }
        index++
      }
      this.temp = tempData
    },
    setListTypeDiscard(obj) {
      const typeHemocomponent = this.items.filter(function(item) {
        return item.id === obj.typehemocomponent_id
      })
      let typediscards = []
      if (typeHemocomponent[0] && typeHemocomponent[0].typediscards) {
        typediscards = typeHemocomponent[0].typediscards
      }
      return typediscards
    },
    getTypeHemocomponent(id) {
      const hemocomponents = this.items.filter(function(item) {
        return item.id === id
      })
      return hemocomponents[0]
    },
    setTypeHemocomponent(scope) {
      const tempData = Object.assign({}, this.temp)

      let typehemocomponent_id = scope.row['typehemocomponent_id']
      if (scope.row['typehemocomponent_id'] === '') {
        typehemocomponent_id = null
        tempData.itemfragmentations[scope.$index]['typehemocomponent'] = {}
      } else {
        tempData.itemfragmentations[scope.$index]['typehemocomponent'] = this.getTypeHemocomponent(scope.row['typehemocomponent_id'])
      }

      tempData.itemfragmentations[scope.$index]['typediscard_id'] = ''
      tempData.itemfragmentations[scope.$index]['typehemocomponent_id'] = typehemocomponent_id

      this.setTypeDiscards(scope)
      this.setExpirationDate(scope)

      this.temp = tempData
    },
    setTypeDiscard(scope) {
      const tempData = Object.assign({}, this.temp)
      let type_discard_id = scope.row['typediscard_id']
      if (scope.row['typediscard_id'] === '') {
        type_discard_id = null
      }
      tempData.itemfragmentations[scope.$index]['typediscard_id'] = type_discard_id
      this.temp = tempData
    },
    setTypeDiscards(scope) {
      const tempData = Object.assign({}, this.temp)
      const typeHemocomponent = this.items.filter(function(item) {
        return item.id === scope.row['typehemocomponent_id']
      })

      if (typeHemocomponent[0].typediscards) {
        tempData.itemfragmentations[scope.$index]['typediscards'] = typeHemocomponent[0].typediscards
      } else {
        tempData.itemfragmentations[scope.$index]['typediscards'] = []
      }
    },
    disabledDate(date) {
      var range = moment().range(this.init_date, this.end_date)
      return !range.contains(date)
    },
    buildDateRange(scope) {
      const typeHemocomponent = this.items.filter(function(item) {
        return item.id === scope.row['typehemocomponent_id']
      })
      const register_at = moment(this.extraction.register_at)
      var init_date = moment(register_at.format()).add(typeHemocomponent[0].expiration_day, 'days')
      var end_date = moment(register_at.format()).add(typeHemocomponent[0].max_expiration_days, 'days')
      this.init_date = init_date.toDate()
      this.end_date = end_date.toDate()
    },
    setExpirationDate(scope) {
      const tempData = Object.assign({}, this.temp)
      const typeHemocomponent = this.items.filter(function(item) {
        return item.id === scope.row['typehemocomponent_id']
      })
      let expirationDate
      const register_at = moment(this.extraction.register_at)
      if (!scope.row.is_max_expiration_days) {
        expirationDate = moment(register_at.format()).add(typeHemocomponent[0].expiration_day, 'days')
        expirationDate = expirationDate.format()
        tempData.itemfragmentations[scope.$index]['expiration_date'] = expirationDate
        this.temp = tempData
      }
    }
  }
}
</script>
<style>
.demo-input-label {
  display: inline-block;
  width: 140px;
}
</style>

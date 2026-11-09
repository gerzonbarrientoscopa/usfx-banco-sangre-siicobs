<template>
  <div class="app-container">
    <div slot="footer" class="dialog-footer" style="text-align: right">
      <el-button v-if="checkPermission(['change_extraction']) && !isEditing" @click="isEditing=true">{{ $t('edit') }}</el-button>
    </div>
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
            <el-form-item
              :label="$t('models.extraction.type_place')"
              prop="type_place"
            >
              <el-radio-group v-model="temp.type_place">
                <el-radio-button v-for="tp in typePlaceOptions" :key="tp.key" :disabled="!isEditing" :label="tp.key">
                  {{ tp.display_name }}
                </el-radio-button>
              </el-radio-group>
            </el-form-item>
            <el-form-item :label="$t('models.extraction.donation')" prop="donation_id">
              <el-select
                v-if="dialogStatus === 'create'"
                v-model="temp.donation_id"
                :disabled="!isEditing"
                :loading="loadingDonation"
                :placeholder="$t('please_select')"
                :remote-method="remoteMethodDonation"
                automatic-dropdown
                class="filter-item"
                filterable
                remote
                @change="getDonation(temp.donation_id)"
              >
                <el-option
                  v-for="item in donations"
                  :key="item.id"
                  :label="item.donor | donorCodeFullName"
                  :value="item.id"
                >
                  <span style="float: left; margin-right: 10px"><strong>{{ item.donor.code }} </strong></span>
                  <span> {{ item.donor | fullName }}</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">{{ item.register_at| toHumanDateMonthLetter }}</span>
                </el-option>
              </el-select>
              <span v-if="dialogStatus === 'update'" class="text-text-turquoise" style="font-weight: bolder">
                {{ temp.donation.donor | donorCodeFullName }}
              </span>
            </el-form-item>
            <el-form-item :label="$t('models.extraction.register_at')" prop="register_at">
              <el-date-picker
                v-model="temp.register_at"
                :disabled="!isEditing"
                :placeholder="$t('models.extraction.register_at')"
                format="dd-MM-yyyy"
                type="date"
                value-format="yyyy-MM-dd"
              />
            </el-form-item>

            <el-form-item :label="$t('models.extraction.type_bag')" prop="bags_quantity">
              <el-radio-group v-model="temp.bags_quantity" :disabled="dialogStatus === 'update' && !checkPermission(['edit_type_bag_extraction'])">
                <el-radio-button v-for="item in typeBagOptions" :key="item.key" :disabled="!isEditing" :label="item.key">
                  {{ item.display_name }}
                </el-radio-button>
              </el-radio-group>
            </el-form-item>

            <el-form-item :label="$t('models.extraction.lot')" prop="lot">
              <el-input v-model="temp.lot" :disabled="!isEditing" @input.native="setUpperCase(temp, 'lot', $event)" />
            </el-form-item>

            <el-form-item
              v-if="!isForApheresis"
              :label="$t('models.extraction.tubing')"
              prop="tubing"
            >
              <el-input v-model="temp.tubing" :disabled="!isEditing" @input.native="setUpperCase(temp, 'tubing', $event)" />
            </el-form-item>

            <el-form-item
              v-if="isForApheresis"
              :label="$t('models.extraction.barcode')"
              prop="barcode"
            >
              <el-input v-model="temp.barcode" :disabled="!isEditing" />
            </el-form-item>
            <el-form-item v-if="!isForApheresis" :label="$t('models.fragmentation.weight')" prop="weight">
              <el-row class="row-bg" justify="space-between">
                <el-col :md="10" :sm="24">
                  <el-input-number v-model.number="temp.weight" :disabled="!isEditing" :min="0" :precision="2" :step="1" size="small" />
                </el-col>
              </el-row>
            </el-form-item>
            <el-form-item
              v-if="!isForApheresis"
              :label="$t('models.extraction.arm')"
              prop="arm"
            >
              <el-radio-group v-model="temp.arm">
                <el-radio-button v-for="arm in armOptions" :key="arm.key" :disabled="!isEditing" :label="arm.key">
                  {{ arm.display_name }}
                </el-radio-button>
              </el-radio-group>
            </el-form-item>

            <el-form-item :label="$t('models.extraction.initial_time')" prop="initial_time">
              <el-time-picker
                v-model="temp.initial_time"
                :disabled="!isEditing"
                :picker-options="{ selectableRange: '00:00:00 - 23:59:00' }"
                format="HH:mm"
                placeholder="Hora Inicial"
                @change="getTotalTime"
              />
            </el-form-item>

            <el-form-item :label="$t('models.extraction.end_time')" prop="end_time">
              <el-time-picker
                v-model="temp.end_time"
                :disabled="!isEditing"
                :picker-options="{ selectableRange: initTime + ' - 23:59:00' }"
                format="HH:mm"
                placeholder="End time"
                @change="getTotalTime"
              />
              <small>Deje en blanco si hay una reaccion adversa</small>
            </el-form-item>

            <el-form-item :label="$t('models.extraction.total_time')" prop="">
              <el-input v-model.number="temp.total_time" :disabled="!isEditing" type="number">
                <template slot="append">minutos</template>
              </el-input>
            </el-form-item>

            <el-form-item :label="$t('models.extraction.typeanticoagulant')" prop="typeanticoagulant_id">
              <el-select
                v-if="dialogStatus === 'create'"
                v-model="temp.typeanticoagulant_id"
                :disabled="!isEditing"
                :placeholder="$t('please_select')"
                automatic-dropdown
                class="filter-item"
                filterable
              >
                <el-option
                  v-for="item in typeAnticoagulants"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                >
                  {{ item.name }}
                </el-option>
              </el-select>
              <span v-if="dialogStatus === 'update'" class="text-text-turquoise" style="font-weight: bolder">
                <span v-if="temp.typeanticoagulant">{{ temp.typeanticoagulant.name }}</span>
              </span>
            </el-form-item>
            <el-form-item :label="$t('models.extraction.observations')" prop="observations">
              <el-input v-model="temp.observations" :disabled="!isEditing" :rows="2" type="textarea" @input.native="setUpperCase(temp, 'observations', $event)" />
            </el-form-item>

            <el-form-item :label="$t('models.extraction.employee')" prop="employee_id">
              <el-select
                v-model="temp.employee_id"
                :disabled="!isEditing"
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
            <el-form-item>
              <el-button v-if="isEditing" @click="isEdit ? updateData(): createData()">{{ $t('confirm') }}</el-button>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
    </el-form>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import { mapGetters } from 'vuex'
import moment from 'moment'
import { graphqlRequest } from '@/api/graphql'
import extractions from '@/query/extraction'
import donations from '@/query/donation'
import typeAnticoagulant from '@/query/type-anticoagulant'

const typeBagOptions = [
  { key: 1, display_name: 'SIMPLE' },
  { key: 2, display_name: 'DOBLE' },
  { key: 3, display_name: 'TRIPLE' },
  { key: 4, display_name: 'CUADRUPLE' },
  { key: 5, display_name: 'CUADRUPLE CON FILTRO' },
  { key: 6, display_name: 'SET DE AFERESIS' }
]

const armOptions = [
  { key: 'I', display_name: 'IZQUIERDO' },
  { key: 'D', display_name: 'DERECHA' }
]

const typePlaceOptions = [
  { key: 'PF', display_name: 'PUESTO FIJO' },
  { key: 'PM', display_name: 'PUESTO MOVIL' }
]

export default {
  name: 'Extraction',
  components: {},
  directives: {},
  filters: {},
  props: {
    row: {
      type: Object,
      default: null
    },
    isEditingParent: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      donations: null,
      loadingDonation: false,
      listDonationQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-register_at, donor__code', from: 'EXT' },
      typeBagOptions,
      armOptions,
      typePlaceOptions,
      temp: {
        id: undefined,
        donation_id: undefined,
        place_id: undefined,
        remark: '',
        timestamp: new Date(),
        title: '',
        type: '',
        status: 'published',
        age: '',
        degree_instruction: '',
        observations: '',
        lot: '',
        tubing: ''
      },
      dialogFormVisible: false,
      dialogStatus: '',
      rules: {
        type_place: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        register_at: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        donation_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        bags_quantity: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        lot: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        arm: [{ required: false, message: this.$t('is_required'), trigger: 'change' }],
        tubing: [{ required: false, message: this.$t('is_required'), trigger: 'blur' }],
        barcode: [{ required: false, message: this.$t('is_required'), trigger: 'blur' }],
        weight: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        initial_time: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        end_time: [{ required: false, message: this.$t('is_required'), trigger: 'blur' }],
        total_time: [{ trigger: 'blur' }, { type: 'number', message: 'Debe ser número' }],
        observations: [{ trigger: 'blur' }],
        employee_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        typeanticoagulant_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }]
      },
      initTime: '00:00:00',
      isEditing: this.isEditingParent,
      isEdit: false,
      isForApheresis: false,
      typeAnticoagulants: []
    }
  },
  computed: {
    ...mapGetters([
      'employees',
      'employee_id'
    ])
  },
  watch: {
    'temp.initial_time': function() {
      this.initTime = moment(this.temp.initial_time).format('HH:mm:ss')
    }
  },
  created() {
    this.getListTypeAnticoagulants()
    this.determineAction()
  },
  mounted() {
  },
  methods: {
    checkPermission,
    determineAction() {
      if (this.row != null) {
        this.isEdit = true
        this.handleUpdate(this.row)
      } else {
        this.isEditing = true
        this.isEdit = false
        this.handleCreate()
      }
    },
    getDonation(id) {
      const donation = this.donations.filter(function(item) {
        return item.id === id
      })
      this.validateTypeProcess(donation[0])
    },
    validateTypeProcess(donation) {
      if (donation && (donation.type_process === 'NA' || donation.type_process === 'CA')) {
        this.isForApheresis = true
        this.rules.barcode = [{ required: true, message: this.$t('is_required'), trigger: 'blur' }]
        this.rules.tubing = [{ required: false, message: this.$t('is_required'), trigger: 'blur' }]
        this.rules.arm = [{ required: false, message: this.$t('is_required'), trigger: 'blur' }]
      } else {
        this.isForApheresis = false
        this.rules.barcode = [{ required: false, message: this.$t('is_required'), trigger: 'blur' }]
        this.rules.tubing = [{ required: true, message: this.$t('is_required'), trigger: 'blur' }]
        this.rules.arm = [{ required: true, message: this.$t('is_required'), trigger: 'blur' }]
      }
    },
    getTotalTime() {
      let total = 0
      if (this.temp.initial_time && this.temp.end_time) {
        var end = moment(this.temp.end_time)
        var startTime = moment(this.temp.initial_time)
        var duration = moment.duration(end.diff(startTime))
        total = parseInt(duration.asMinutes())
        const tempData = Object.assign({}, this.temp)
        tempData.total_time = total
        this.temp = tempData
      }
    },
    getListDonations() {
      this.loadingDonation = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'donations',
          query: donations.extractionDonationSelect(this.listDonationQuery)
        }
      ).then(response => {
        const data = response.data
        this.donations = data.donations.results
        this.loadingDonation = false
      })
    },
    remoteMethodDonation(query) {
      if (query !== '') {
        this.listDonationQuery.search = query
      } else {
        this.listDonationQuery.search = ''
      }
      this.getListDonations()
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        type_place: 'PF',
        observations: '',
        lot: '',
        tubing: '',
        weight: undefined,
        register_at: moment().format('YYYY-MM-DD')
      }
    },
    handleCreate() {
      this.resetTemp()
      this.getListDonations()
      const tempData = Object.assign({}, this.temp)
      tempData.employee_id = this.employee_id
      // tempData.initial_time = new Date()
      this.temp = tempData

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
          tempData.register_id = this.employee_id
          tempData.initial_time = moment(this.temp.initial_time).format('HH:mm')
          if (this.temp.end_time) {
            tempData.end_time = moment(this.temp.end_time).format('HH:mm')
          }
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'createExtraction',
              query: extractions.createExtraction(),
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
      tempData.donation_id = tempData.donation.id
      tempData.employee_id = tempData.employee.id
      tempData.typeanticoagulant_id = tempData.typeanticoagulant.id
      tempData.initial_time = moment(tempData.initial_time, 'HH:mm')

      if (tempData.end_time) {
        tempData.end_time = moment(tempData.end_time, 'HH:mm')
      }
      this.temp = tempData
      this.validateTypeProcess(tempData.donation)

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
          tempData.register_id = this.temp.register.id
          tempData.initial_time = moment(this.temp.initial_time).format('HH:mm')

          if (this.temp.end_time) {
            tempData.end_time = moment(this.temp.end_time).format('HH:mm')
          }
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'updateExtraction',
              query: extractions.updateExtraction(),
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
              this.isEditing = false
              this.$emit('refreshExtraction', false)
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
    getListTypeAnticoagulants() {
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'anticoagulant',
          query: typeAnticoagulant.list(),
          variables: {}
        }
      ).then(response => {
        const data = response.data
        this.typeAnticoagulants = data.typeanticoagulants.results
      })
    }
  }
}
</script>
<style>
.fg-orange {
  color: #bd3739;
}
</style>

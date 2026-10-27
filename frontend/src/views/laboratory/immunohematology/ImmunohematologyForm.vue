<template>
  <div class="app-container">
    <el-form
      ref="dataForm"
      :model="temp"
      :rules="rules"
      label-position="right"
      label-width="100px"
      style="width: 100%;"
    >

      <div class="grid-content">
        <el-row :gutter="20">
          <el-col :md="8" :sm="24">
            <el-form-item :label="$t('models.immunohematology.donation')" prop="donation_id">
              <el-select
                v-if="dialogStatus === 'create' && !rowExtraction"
                v-model="temp.donation_id"
                :loading="loading"
                :placeholder="$t('please_select')"
                :remote-method="remoteMethod"
                automatic-dropdown
                class="filter-item"
                filterable
                remote
                @change="getDonation()"
              >
                <el-option
                  v-for="item in donations"
                  :key="item.id"
                  :label="item.donor.code"
                  :value="item.id"
                >
                  <span style="float: left"><strong>{{ item.donor.code }}</strong></span>
                  <span style="float: right; color: #8492a6; font-size: 13px">{{ item.register_at| toHumanDateMonthLetter }}</span>
                </el-option>
              </el-select>
              <strong v-if="dialogStatus === 'update'" class="text-text-green-sea">
                {{ temp.donation.donor.code }}
              </strong>
              <strong v-if="dialogStatus === 'create' && rowExtraction" class="text-text-green-sea">
                {{ rowExtraction.donation.donor.code }}
              </strong>
              <br>
              <el-tag v-if="donation && donation.exam.blood_group">
                Pre-Tamizaje: GRUPO ABO {{ donation.exam.blood_group }}
              </el-tag>
              <el-tag v-else>No existe registro de GRUPO ABO en Pre-Tamizaje</el-tag>
            </el-form-item>
            <el-form-item>
              <el-button v-if="donation" size="mini" @click="handleOpenForm">
                HISTORIAL DE IMMUNOHEMATOLOGIA
              </el-button>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item :label="$t('models.immunohematology.register_at')" prop="register_at">
              <el-date-picker
                v-model="temp.register_at"
                :placeholder="$t('models.immunohematology.register_at')"
                format="dd-MM-yyyy"
                type="date"
                value-format="yyyy-MM-dd"
              />
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
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
        <el-row :gutter="20">
          <el-col :md="8" :sm="24">
            <h3 class="text-center">GRUPO SANGUINEO ABO</h3>
            <el-form-item :label="$t('models.immunohematology.direct_abo')" prop="direct_abo">
              <el-radio-group v-model="temp.direct_abo" size="mini">
                <el-radio-button v-for="item in bloodGroupOptions" :key="item.key" :label="item.key">
                  <span v-html="item.display_name" />
                </el-radio-button>
              </el-radio-group>
            </el-form-item>

            <el-form-item :label="$t('models.immunohematology.inverse_abo')" prop="inverse_abo">
              <el-radio-group v-model="temp.inverse_abo" size="mini">
                <el-radio-button v-for="item in bloodGroupOptions" :key="item.key" :label="item.key">
                  <span v-html="item.display_name" />
                </el-radio-button>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <h3 class="text-center">FENOTIPO Rh</h3>
            <el-form-item :label="$t('models.immunohematology.phenotype')" prop="phenotype">
              <el-radio-group v-model="temp.phenotype" size="mini">
                <el-radio-button v-for="item in phenotypeOptions" :key="item.key" :label="item.key">
                  {{ item.display_name }}
                </el-radio-button>
              </el-radio-group>
            </el-form-item>
            <el-form-item :label="$t('models.immunohematology.factor_rh')" prop="factor_rh">
              <el-radio-group v-model="temp.factor_rh" size="mini">
                <el-radio-button v-for="item in rhOptions" :key="item.key" :label="item.key">
                  {{ item.display_name }}
                </el-radio-button>
              </el-radio-group>
            </el-form-item>
            <hr>
            <el-form-item :label="$t('models.immunohematology.antikell')" prop="antikell">
              <el-radio-group v-model="temp.antikell" size="mini">
                <el-radio-button v-for="item in kellOptions" :key="item.key" :label="item.key">
                  {{ item.display_name }}
                </el-radio-button>
              </el-radio-group>
            </el-form-item>
          </el-col>

          <el-col :md="8" :sm="24">
            <h3 class="text-center">
              ANTICUERPOS IRREGULARES
              <el-tooltip class="item" content="Poner en Negativo" effect="dark">
                <el-button circle icon="el-icon-check" size="mini" type="default" @click="setNegative($event)" />
              </el-tooltip>
            </h3>
            <h3 class="text-center">CELULA I</h3>

            <el-form-item :label="$t('models.immunohematology.fsi')" prop="fsi">
              <el-radio-group v-model="temp.fsi" size="mini" @change="handleChange">
                <el-radio-button v-for="item in crossesInverseOptions" :key="item.key" :label="item.key">
                  {{ item.display_name }}
                </el-radio-button>
              </el-radio-group>
            </el-form-item>
            <el-form-item :label="$t('models.immunohematology.liss')" prop="liss">
              <el-radio-group v-model="temp.liss" size="mini" @change="handleChange">
                <el-radio-button v-for="item in crossesInverseOptions" :key="item.key" :label="item.key">
                  {{ item.display_name }}
                </el-radio-button>
              </el-radio-group>
            </el-form-item>
            <el-form-item :label="$t('models.immunohematology.alb')" prop="alb">
              <el-radio-group v-model="temp.alb" size="mini" @change="handleChange">
                <el-radio-button v-for="item in crossesInverseOptions" :key="item.key" :label="item.key">
                  {{ item.display_name }}
                </el-radio-button>
              </el-radio-group>
            </el-form-item>
            <el-form-item :label="$t('models.immunohematology.coombs')" prop="coombs">
              <el-radio-group v-model="temp.coombs" size="mini" @change="handleChange">
                <el-radio-button v-for="item in crossesInverseOptions" :key="item.key" :label="item.key">
                  {{ item.display_name }}
                </el-radio-button>
              </el-radio-group>
            </el-form-item>
            <h3 class="text-center">CELULA II</h3>
            <el-form-item :label="$t('models.immunohematology.p2fsi')" prop="p2fsi">
              <el-radio-group v-model="temp.p2fsi" size="mini" @change="handleChange">
                <el-radio-button v-for="item in crossesInverseOptions" :key="item.key" :label="item.key">
                  {{ item.display_name }}
                </el-radio-button>
              </el-radio-group>
            </el-form-item>
            <el-form-item :label="$t('models.immunohematology.p2liss')" prop="p2liss">
              <el-radio-group v-model="temp.p2liss" size="mini" @change="handleChange">
                <el-radio-button v-for="item in crossesInverseOptions" :key="item.key" :label="item.key">
                  {{ item.display_name }}
                </el-radio-button>
              </el-radio-group>
            </el-form-item>
            <el-form-item :label="$t('models.immunohematology.p2alb')" prop="p2alb">
              <el-radio-group v-model="temp.p2alb" size="mini" @change="handleChange">
                <el-radio-button v-for="item in crossesInverseOptions" :key="item.key" :label="item.key">
                  {{ item.display_name }}
                </el-radio-button>
              </el-radio-group>
            </el-form-item>
            <el-form-item :label="$t('models.immunohematology.p2coombs')" prop="p2coombs">
              <el-radio-group v-model="temp.p2coombs" size="mini" @change="handleChange">
                <el-radio-button v-for="item in crossesInverseOptions" :key="item.key" :label="item.key">
                  {{ item.display_name }}
                </el-radio-button>
              </el-radio-group>
            </el-form-item>
            <h3 class="text-center">CELULA III</h3>
            <el-form-item :label="$t('models.immunohematology.p3fsi')" prop="p3fsi">
              <el-radio-group v-model="temp.p3fsi" size="mini" @change="handleChange">
                <el-radio-button v-for="item in crossesInverseOptions" :key="item.key" :label="item.key">
                  {{ item.display_name }}
                </el-radio-button>
              </el-radio-group>
            </el-form-item>
            <el-form-item :label="$t('models.immunohematology.p3liss')" prop="p3liss">
              <el-radio-group v-model="temp.p3liss" size="mini" @change="handleChange">
                <el-radio-button v-for="item in crossesInverseOptions" :key="item.key" :label="item.key">
                  {{ item.display_name }}
                </el-radio-button>
              </el-radio-group>
            </el-form-item>
            <el-form-item :label="$t('models.immunohematology.p3alb')" prop="p3alb">
              <el-radio-group v-model="temp.p3alb" size="mini" @change="handleChange">
                <el-radio-button v-for="item in crossesInverseOptions" :key="item.key" :label="item.key">
                  {{ item.display_name }}
                </el-radio-button>
              </el-radio-group>
            </el-form-item>
            <el-form-item :label="$t('models.immunohematology.p3coombs')" prop="p3coombs">
              <el-radio-group v-model="temp.p3coombs" size="mini" @change="handleChange">
                <el-radio-button v-for="item in crossesInverseOptions" :key="item.key" :label="item.key">
                  {{ item.display_name }}
                </el-radio-button>
              </el-radio-group>
            </el-form-item>

            <hr>
            <el-form-item :label="$t('models.immunohematology.observations')" prop="observations">
              <el-input v-model="temp.observations" :rows="2" type="textarea" @input.native="setUpperCase(temp, 'observations', $event)" />
            </el-form-item>
            <br>
            <el-alert v-if="donation && donation.extraction && donation.extraction.fragmentation" :closable="false">
              No existe registro de fraccionamiento
            </el-alert>
            <el-form-item
              v-show="enabledTypeIrregularAntiBodies"
              :label="$t('models.immunohematology.type_irregular_antibody')"
              prop="type_irregular_antibody_id"
            >
              <el-select
                v-model="temp.type_irregular_antibody_id"
                :loading="loadingTypeIrregularAntiBody"
                :placeholder="$t('please_select')"
                automatic-dropdown
                class="filter-item"
                clearable
                @change="getListTypeIrregularAntiBody()"
              >
                <el-option
                  v-for="item in typeIrregularAntiBodies"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
      </div>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="dialogStatus==='create'?createData():updateData()">{{ $t('confirm') }}
      </el-button>
    </div>

    <el-dialog
      :before-close="handleCloseForm"
      :visible.sync="dialogFormVisible"
      append-to-body
      title="Historial de Immunohematología del Donante"
      width="80%"
    >
      <history-immunohematology-donor :donation="donation" />
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { graphqlRequest } from '@/api/graphql'
import donations from '@/query/donation'
import typeIrregularAntiBodies from '@/query/typeIrregularAntiBody'
import moment from 'moment'
import { RH_OPTIONS, CROSSES_HEMOLISIS } from '@/utils/const'
import immunohematologies from '@/query/immunohematology'
import HistoryImmunohematologyDonor from './HistoryImmunohematologyDonor'

const crossesOptions = [
  { key: '+', display_name: '+' },
  { key: '++', display_name: '++' },
  { key: '+++', display_name: '+++' },
  { key: '++++', display_name: '++++' },
  { key: '-', display_name: 'Negativo' }
]
const crossesInverseOptions = [
  { key: '-', display_name: 'Negativo' },
  { key: '+', display_name: '+' },
  { key: '++', display_name: '++' },
  { key: '+++', display_name: '+++' },
  { key: '++++', display_name: '++++' }
]
const crossesInverseDOptions = [
  { key: '++++', display_name: '++++' },
  { key: '+++', display_name: '+++' },
  { key: '++', display_name: '++' },
  { key: '+', display_name: '+' },
  { key: '-', display_name: 'Negativo' }
]
const bloodGroupOptions = [
  { key: 'O', display_name: 'O' },
  { key: 'A1', display_name: 'A<sub>1</sub>' },
  { key: 'A2', display_name: 'A<sub>2</sub>' },
  { key: 'B', display_name: 'B' },
  { key: 'A1B', display_name: 'A<sub>1</sub>B' },
  { key: 'A2B', display_name: 'A<sub>2</sub>B' }
]
const kellOptions = [
  { key: '-', display_name: 'Negativo' },
  { key: '+', display_name: 'Positivo' }
]
const phenotypeOptions = [
  { key: 'C+ ĉ+ E+ ê+', display_name: 'C+ ĉ+ E+ ê+' },
  { key: 'C- c+ E+ ê-', display_name: 'C- c+ E+ ê-' },
  { key: 'C+ c- E- e+', display_name: 'C+ c- E- e+' },
  { key: 'C+ c- E+ e-', display_name: 'C+ c- E+ e-' },
  { key: 'C- c+ E- e+', display_name: 'C- c+ E- e+' },
  { key: 'C+ c- E+ e+', display_name: 'C+ c- E+ e+' },
  { key: 'C(-) c+ E+ e+', display_name: 'C(-) c+ E+ e+' },
  { key: 'C+ ĉ+ E+ e-', display_name: 'C+ ĉ+ E+ e-' },
  { key: 'C+ c+ E- e+', display_name: 'C+ c+ E- e+' }
]
const rhOptions = RH_OPTIONS
const crossesHemolisisOptions = CROSSES_HEMOLISIS

export default {
  name: 'ImmunohematologyForm',
  components: { HistoryImmunohematologyDonor },
  props: {
    row: {
      type: Object,
      default: null
    },
    rowExtraction: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      loading: false,
      donations: null,
      total: null,
      donation: null,
      listDonationQuery: { page: 1, limit: 20, search: '', offset: 0, ordering: '-id', from: 'HEM' },
      crossesOptions,
      crossesInverseOptions,
      crossesInverseDOptions,
      crossesHemolisisOptions,
      bloodGroupOptions,
      rhOptions,
      phenotypeOptions,
      kellOptions,
      listQuery: { page: 1, limit: 20, search: '', ordering: '-id' },
      temp: {
        id: undefined,
        employee_id: undefined,
        donation_id: undefined,
        direct_abo: null,
        inverse_abo: null,
        factor_rh: null,
        phenotype: null,
        antikell: null,
        alb: null,
        fsi: null,
        liss: null,
        coombs: null,
        p2alb: null,
        p2fsi: null,
        p2liss: null,
        p2coombs: null,
        p3alb: null,
        p3fsi: null,
        p3liss: null,
        p3coombs: null,
        observations: '',
        register_at: moment().format('YYYY-MM-DD'),
        type_irregular_antibody_id: undefined
      },
      rules: {
        donation_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        employee_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        direct_abo: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        inverse_abo: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        factor_rh: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        phenotype: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        antikell: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        alb: [{ required: false, message: this.$t('is_required'), trigger: 'change' }],
        fsi: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        liss: [{ required: false, message: this.$t('is_required'), trigger: 'change' }],
        coombs: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        p2alb: [{ required: false, message: this.$t('is_required'), trigger: 'change' }],
        p2fsi: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        p2liss: [{ required: false, message: this.$t('is_required'), trigger: 'change' }],
        p2coombs: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        p3alb: [{ required: false, message: this.$t('is_required'), trigger: 'change' }],
        p3fsi: [{ required: false, message: this.$t('is_required'), trigger: 'change' }],
        p3liss: [{ required: false, message: this.$t('is_required'), trigger: 'change' }],
        p3coombs: [{ required: false, message: this.$t('is_required'), trigger: 'change' }],
        observations: [{ trigger: 'blur' }],
        register_at: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }]
      },
      dialogStatus: '',
      typeIrregularAntiBodies: [],
      enabledTypeIrregularAntiBodies: false,
      loadingTypeIrregularAntiBody: false,
      listTypeIrregularAntiBodyQuery: { page: 1, limit: 50, offset: 0, search: '', ordering: 'name' },
      dialogFormVisible: false,
      errorMessage: ''
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
    rowExtraction: function() {
      this.determineAction()
    },
    'temp.factor_rh': function(value) {
      if (value !== null && !this.isEdit) {
        this.isSameBloodGroup()
      }
    }
  },
  mounted() {
    this.determineAction()
  },
  methods: {
    determineAction() {
      if (this.row) {
        this.handleUpdate(this.row)
        this.isEdit = true
      } else {
        this.handleCreate()
        this.donation = null
        this.isEdit = false
      }
      this.getListTypeIrregularAntiBody()
    },
    isSameBloodGroup() {
      const blood_group = this.donation ? this.donation.exam.blood_group : ''
      var isEqualGroupABO = false
      this.errorMessage = ''

      if (blood_group !== '') {
        const factor_rh = blood_group[blood_group.length - 1]
        const factor_rh_current = this.temp.factor_rh !== null ? this.temp.factor_rh[this.temp.factor_rh.length - 1] : ''
        const blood = blood_group.split(factor_rh)

        if (factor_rh_current !== factor_rh) {
          this.errorMessage = 'Factor RH, No es igual resultado en Pre-tamizaje'
          this.$message({
            title: 'Error Factor RH,',
            message: this.errorMessage,
            type: 'error'
          })
        }

        let withNoDigits = ''

        if (this.temp.direct_abo) {
          withNoDigits = this.temp.direct_abo.replace(/[0-9]/g, '')
        }

        if (withNoDigits === blood[0]) {
          isEqualGroupABO = true
        } else {
          this.errorMessage = 'Grupo Sanguíneo, No es igual resultado en Pre-tamizaje'

          this.$message({
            title: 'Error Grupo Sanguíneo,',
            message: this.errorMessage,
            type: 'error'
          })
        }

        if (this.temp.direct_abo !== this.temp.inverse_abo) {
          isEqualGroupABO = false
          this.errorMessage = 'Directa ABO, No es igual a Inversa ABO'
          this.$message({
            title: 'Error Factor RH,',
            message: this.errorMessage,
            type: 'error'
          })
        }
      } else {
        this.errorMessage = 'Grupo Sanguíneo, No existe resultado en Pre-tamizaje'
        this.$notify({
          title: 'Advertencia Grupo Sanguíneo,',
          message: this.errorMessage,
          type: 'warning'
        })
      }

      return isEqualGroupABO
    },
    handleOpenForm() {
      this.dialogFormVisible = true
    },
    handleCloseForm() {
      this.dialogFormVisible = false
    },
    handleChange() {
      const state = (this.temp.alb && this.temp.alb.indexOf('+') !== -1) ||
        (this.temp.fsi && this.temp.fsi.indexOf('+') !== -1) ||
        (this.temp.liss && this.temp.liss.indexOf('+') !== -1) ||
        (this.temp.coombs && this.temp.coombs.indexOf('+') !== -1) ||

        (this.temp.p2alb && this.temp.p2alb.indexOf('+') !== -1) ||
        (this.temp.p2fsi && this.temp.p2fsi.indexOf('+') !== -1) ||
        (this.temp.p2liss && this.temp.p2liss.indexOf('+') !== -1) ||
        (this.temp.p2coombs && this.temp.p2coombs.indexOf('+') !== -1) ||

        (this.temp.p3alb && this.temp.p3alb.indexOf('+') !== -1) ||
        (this.temp.p3fsi && this.temp.p3fsi.indexOf('+') !== -1) ||
        (this.temp.p3liss && this.temp.p3liss.indexOf('+') !== -1) ||
        (this.temp.p3coombs && this.temp.p3coombs.indexOf('+') !== -1)
      if (state == null || state === false) {
        this.temp.type_irregular_antibody_id = undefined
        this.enabledTypeIrregularAntiBodies = false
      } else {
        this.enabledTypeIrregularAntiBodies = true
      }
    },
    setNegative(event) {
      event.preventDefault()
      event.stopPropagation()
      const tempData = Object.assign({}, this.temp)
      tempData.fsi = '-'
      tempData.liss = '-'
      tempData.alb = '-'
      tempData.coombs = '-'
      tempData.p2fsi = '-'
      tempData.p2liss = '-'
      tempData.p2alb = '-'
      tempData.p2coombs = '-'
      tempData.p3fsi = '-'
      tempData.p3liss = '-'
      tempData.p3alb = '-'
      tempData.p3coombs = '-'
      tempData.type_irregular_antibody_id = undefined
      this.temp = tempData
      this.enabledTypeIrregularAntiBodies = false
    },
    getListDonation() {
      this.loading = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'donations',
          query: donations.immunohematologySelect(this.listDonationQuery)
        }
      ).then(response => {
        const data = response.data
        this.donations = data.donations.results
        this.total = data.donations.totalCount
        this.loading = false
      })
    },
    remoteMethod(query) {
      if (query !== '') {
        this.listDonationQuery.search = query
      } else {
        this.listDonationQuery.search = ''
      }
      this.getListDonation()
    },
    getListTypeIrregularAntiBody() {
      this.loadingTypeIrregularAntiBody = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'type_irregular_antibodies',
          query: typeIrregularAntiBodies.list(this.listTypeIrregularAntiBodyQuery)
        }
      ).then(response => {
        const data = response.data
        this.typeIrregularAntiBodies = data.type_irregular_antibodies.results
        this.loadingTypeIrregularAntiBody = false
      })
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        employee_id: undefined,
        donation_id: undefined,
        direct_abo: null,
        inverse_abo: null,
        factor_rh: null,
        phenotype: null,
        antikell: null,
        alb: null,
        fsi: null,
        liss: null,
        coombs: null,
        p2alb: null,
        p2fsi: null,
        p2liss: null,
        p2coombs: null,
        p3alb: null,
        p3fsi: null,
        p3liss: null,
        p3coombs: null,
        observations: '',
        register_at: moment().format('YYYY-MM-DD'),
        type_irregular_antibody_id: undefined
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      if (this.rowExtraction) {
        this.temp.donation_id = this.rowExtraction.donation.id
        this.getDonation()
      } else {
        this.getListDonation()
      }
      this.enabledTypeIrregularAntiBodies = false
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
          if (!this.isSameBloodGroup()) {
            return
          }

          const tempData = Object.assign({}, this.temp)
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'createImmnunohematology',
              query: immunohematologies.createImmunohematology(),
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
              // this.resetTemp()
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
    getDonation() {
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'donation',
          query: donations.getDonationEdit(this.temp.donation_id)
        }
      ).then(response => {
        const data = response.data
        this.donation = data.donation
      })
    },
    handleUpdate(row) {
      this.dialogStatus = 'update'

      const tempData = Object.assign({}, row)
      tempData.donation_id = tempData.donation.id
      tempData.employee_id = tempData.employee.id
      if (tempData.type_irregular_antibody) {
        tempData.type_irregular_antibody_id = tempData.type_irregular_antibody.id
        this.enabledTypeIrregularAntiBodies = true
      }
      this.temp = tempData
      this.getDonation()
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
              service: 'updateImmunohematology',
              query: immunohematologies.updateImmunohematology(),
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
                message: 'Se ha actualizado',
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


<style type="text/scss">
  .el-input--medium {
    text-transform: uppercase;
  }
</style>
<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model.lazy="listQuery.search"
        :placeholder="$t('models.donor.search')"
        :autofocus="'autofocus'"
        prefix-icon="el-icon-search"
        clearable
        class="filter-item"
        @input="handleFilter"
      />
      <el-button
        v-if="checkPermission(['add_donor'])"
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
      :default-sort="{prop: 'code', order: 'descending'}"
      border
      fit
      stripe
      highlight-current-row
      style="width: 100%;"
      @sort-change="handleOrderChange"
      @selection-change="handleSelectionChange"
    >
      <el-table-column
        :label="$t('models.donor.code')"
        fixed
        width="100px"
        align="center"
        prop="code"
        sortable="custom"
      >
        <template slot-scope="scope">
          <span>
            {{ scope.row.code }}
            <el-tooltip content="CODIGO ALTERNATIVO" placement="top">
              <small v-if="scope.row.code_other"><br>{{ scope.row.code_other }}</small>
            </el-tooltip>
          </span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.patient.first_name')" width="170px">
        <template slot-scope="scope">
          <span>{{ scope.row.first_name }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.patient.middle_name')" width="170px">
        <template slot-scope="scope">
          <span>{{ scope.row.middle_name }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.patient.last_name')" width="170px">
        <template slot-scope="scope">
          <span>{{ scope.row.last_name }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.donor.age')" width="80px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.age }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.donor.gender')" width="80px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.gender }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.donor.last_donation_at')" width="150px" align="center">
        <template slot-scope="scope">
          <span v-if="scope.row.last_effective_donation_at">
            {{ scope.row.last_effective_donation_at | toHumanDate() }}
            <br>
            <vue-moments-ago :date="scope.row.last_effective_donation_at" prefix="hace" suffix="aprox." lang="es" />
          </span>
        </template>
      </el-table-column>

      <el-table-column
        :label="$t('actions')"
        fixed="right"
        align="center"
        width="230"
        class-name="small-padding"
      >
        <template slot-scope="scope">
          <router-link v-if="$route.name !== 'registry-fast'" :to="'/registry/donors/'+scope.row.id">
            <el-tooltip :enterable="false" :content="$t('details')" class="item" effect="dark">
              <el-button v-if="checkPermission(['view_donor'])" size="mini"><font-awesome-icon icon="align-justify" /></el-button>
            </el-tooltip>
          </router-link>
          <el-tooltip :enterable="false" :content="$t('edit')" class="item" effect="dark">
            <el-button v-if="checkPermission(['change_donor'])" size="mini" @click.stop.prevent="handleUpdate(scope.row)">
              <font-awesome-icon icon="edit" />
            </el-button>
          </el-tooltip>
          <el-button v-if="$route.name === 'registry-fast' && checkPermission(['change_donor'])" size="mini" @click.stop.prevent="handleSelected(scope.row)">
            Seleccionar
          </el-button>
          <el-tooltip v-if="isAreaPromotion" class="item" effect="dark" content="Ficha de Donante Voluntario" placement="top-start">
            <el-button
              class="filter-item"
              type="default"
              size="mini"
              @click.stop.prevent="handlePrintDonorVolunteer(scope.row)"
            >
              <font-awesome-icon icon="book" />
            </el-button>
          </el-tooltip>
          <el-tooltip v-if="!scope.row.can_donate && $route.name === 'donor'" class="item" effect="dark" content="Habilitar Donante" placement="top-start">
            <el-button
              v-if="checkPermission(['enable_rejected_donor'])"
              class="filter-item"
              type="success"
              size="mini"
              @click.stop.prevent="enableDonor(scope.row)"
            >
              <font-awesome-icon icon="check" />
            </el-button>
          </el-tooltip>
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

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible" width="95%" destroy-on-close>
      <el-form
        ref="dataForm"
        :rules="rules"
        :model="temp"
        label-position="right"
        label-width="160px"
        style="width: 100%;"
      >
        <el-row :gutter="20">
          <el-col :sm="24" :md="24">
            <h3>Datos Personales</h3>
          </el-col>
          <el-col :sm="24" :md="8">

            <el-form-item :label="'Numero Indeficado'" prop="code">
              <el-input v-model.number="temp.code" type="number" />
            </el-form-item>
            <el-form-item :label="$t('models.donor.civil_status')" prop="civil_status">
              <el-select v-model="temp.civil_status" :placeholder="$t('please_select')" class="filter-item" automatic-dropdown>
                <el-option
                  v-for="item in maritalOptions"
                  :key="item.key"
                  :label="item.display_name"
                  :value="item.key"
                />
              </el-select>
            </el-form-item>
            <el-form-item :label="$t('models.donor.country')" prop="country">
              <el-select v-model="temp.country" :placeholder="$t('please_select')" class="filter-item" automatic-dropdown filterable>
                <el-option
                  v-for="item in countryOptions"
                  :key="item.key"
                  :label="item.display_name"
                  :value="item.key"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :sm="24" :md="8">
            <el-form-item :label="$t('models.donor.ci')" prop="ci">
              <el-input v-model="temp.ci" class="input-with-select customize-ci">
                <el-select slot="append" v-model="temp.ci_extension" placeholder="Depto.">
                  <el-option
                    v-for="item in departamentOptions"
                    :key="item.key"
                    :label="item.key"
                    :value="item.key"
                  />
                </el-select>
              </el-input>
            </el-form-item>
            <el-form-item :label="$t('models.donor.first_name')" prop="first_name">
              <el-input v-model="temp.first_name" @input.native="setUpperCase(temp, 'first_name', $event)" />
            </el-form-item>
            <el-form-item :label="$t('models.donor.middle_name')" prop="middle_name">
              <el-input v-model="temp.middle_name" @input.native="setUpperCase(temp, 'middle_name', $event)" />
            </el-form-item>
            <el-form-item :label="$t('models.donor.last_name')" prop="last_name">
              <el-input v-model="temp.last_name" @input.native="setUpperCase(temp, 'last_name', $event)" />
            </el-form-item>
          </el-col>
          <el-col :sm="24" :md="8">
            <el-form-item :label="$t('models.donor.birth_date')" prop="birth_date">
              <el-date-picker
                v-model="temp.birth_date"
                placeholder="dd-mm-YYYY"
                :picker-options="pickerOptionsBirthDate"
                type="date"
                format="dd-MM-yyyy"
                value-format="yyyy-MM-dd"
              />
            </el-form-item>
            <el-form-item :label="$t('models.donor.age')" prop="age">
              <el-input v-model="age" :disabled="true">
                <template slot="append">años</template>
              </el-input>
            </el-form-item>
            <el-form-item :label="$t('models.donor.gender')" prop="gender">
              <el-radio-group v-model="temp.gender">
                <el-radio-button label="F">F</el-radio-button>
                <el-radio-button label="M">M</el-radio-button>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :sm="24" :md="24">
            <h3>Procedencia</h3>
          </el-col>
          <el-col :sm="24" :md="8">
            <el-form-item :label="$t('models.donor.residence')" prop="residence">
              <el-input v-model="temp.residence" @input.native="setUpperCase(temp, 'residence', $event)" />
            </el-form-item>
            <el-form-item :label="$t('models.donor.zone')" prop="zone">
              <el-input v-model="temp.zone" @input.native="setUpperCase(temp, 'zone', $event)" />
            </el-form-item>
            <el-form-item :label="$t('models.donor.province')" prop="province">
              <el-input v-model="temp.province" @input.native="setUpperCase(temp, 'province', $event)" />
            </el-form-item>
          </el-col>
          <el-col :sm="24" :md="7">
            <el-form-item :label="$t('models.donor.department')" prop="department">
              <el-select v-model="temp.department" :placeholder="$t('please_select')" class="filter-item" automatic-dropdown>
                <el-option
                  v-for="item in departamentOptions"
                  :key="item.key"
                  :label="item.display_name"
                  :value="item.key"
                />
              </el-select>
            </el-form-item>
            <el-form-item :label="$t('models.donor.phone')" prop="phone">
              <el-input v-model="temp.phone" type="number" />
            </el-form-item>
            <el-form-item :label="$t('models.donor.mobile_phone')" prop="mobile_phone">
              <el-input v-model="temp.mobile_phone" type="number" />
            </el-form-item>
          </el-col>
          <el-col :sm="24" :md="9">
            <el-form-item :label="$t('models.donor.family_phone')" label-width="180px" prop="family_phone">
              <el-input v-model="temp.family_phone" type="number" />
            </el-form-item>
            <el-form-item :label="$t('models.donor.profession')" label-width="180px" prop="profession">
              <el-input v-model="temp.profession" @input.native="setUpperCase(temp, 'profession', $event)" />
            </el-form-item>
            <el-form-item :label="$t('models.donor.degree_instruction')" label-width="180px" prop="degree_instruction">
              <el-select v-model="temp.degree_instruction" :placeholder="$t('please_select')" class="filter-item" automatic-dropdown>
                <el-option v-for="item in gradeOptions" :key="item.key" :label="item.display_name" :value="item.key" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :sm="24" :md="24">
            <h3>Lugar de Trabajo</h3>
          </el-col>
          <el-col :sm="24" :md="8">
            <el-form-item :label="$t('models.donor.job')" prop="job">
              <el-input v-model="temp.job" @input.native="setUpperCase(temp, 'job', $event)" />
            </el-form-item>
          </el-col>
          <el-col :sm="24" :md="8">
            <el-form-item :label="$t('models.donor.job_address')" prop="job_address">
              <el-input v-model="temp.job_address" @input.native="setUpperCase(temp, 'job_address', $event)" />
            </el-form-item>
          </el-col>
          <el-col :sm="24" :md="8">
            <el-form-item :label="$t('models.donor.email')" prop="email">
              <el-input v-model="temp.email" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">{{ $t('cancel') }}</el-button>
        <el-button @click="dialogStatus==='create'?createData():updateData()">
          <span v-if="$route.name !== 'registry-fast'">{{ $t('confirm') }}</span>
          <span v-if="$route.name === 'registry-fast'">Guardar y continuar</span>
        </el-button>
      </div>
    </el-dialog>

    <el-dialog
      :visible.sync="reportDialogVisible"
      title="FICHA DEL DONANTE VOLUNTARIO"
      width="100%"
      top="10px"
      center
    >
      <report-dialog v-if="!reportDialogLoading" :row="pdf" />
      <div v-if="reportDialogLoading" class="loading-report">
        <i class="el-icon-loading" style="font-size: 80px" />
      </div>
    </el-dialog>

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormEnableDonorVisible" :before-close="handleCloseForm" :width="widthDialog" destroy-on-close>
      <el-row :gutter="20">
        <el-col :md="24">
          <div class="grid-content">
            <enable-donor v-if="dialogStatus === 'enable'" :row="row" @dialogStatus="handleCloseForm" />
            <donor-join v-if="dialogStatus === 'join'" ref="Receptor" :row="multipleSelection" @dialogStatus="handleCloseForm" />
          </div>
        </el-col>
      </el-row>
    </el-dialog>

    <el-dialog
      :visible.sync="dialogCannotDonation"
      width="60%"
      destroy-on-close
    >
      <el-row>
        <el-col :span="12">
          <h1 class="text-red">
            Oops!
          </h1>
          <h2 class="text-red">El donante selecionado no puede donar en este momento, por favor consulte con el personal del Banco de Sangre</h2>
        </el-col>
        <el-col :span="12">
          <img :src="errGif" width="313" height="428" alt="">
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
import errGif from '@/assets/401_images/401.gif'
import checkPermission from '@/utils/permission'
import { printDonorVolunteer } from '@/api/donor'
import ReportDialog from '../report-dialog/ReportDialog'
import EnableDonor from '../registry/components/enableDonor'
import DonorJoin from './join'
import Cookies from 'js-cookie'
import VueMomentsAgo from 'vue-moments-ago'
import { graphqlRequest } from '@/api/graphql'
import donors from '@/query/donor'
import { debounce } from 'debounce'
import moment from 'moment'
import { COUNTRIES, DEPARTMENT_OPTIONS } from '@/utils/const'


const maritalOptions = [
  { key: 'SO', display_name: 'SOLTERO/A' },
  { key: 'CO', display_name: 'COMPROMETIDO/A' },
  { key: 'CON', display_name: 'CONCUBINO/A' },
  { key: 'CA', display_name: 'CASADO/A' },
  { key: 'DI', display_name: 'DIVORCIADO/A' },
  { key: 'VI', display_name: 'VIUDO/A' }
]

const gradeOptions = [
  { key: 'SIN_EST', display_name: 'SIN ESTUDIOS' },
  { key: 'PRI', display_name: 'PRIMARIA' },
  { key: 'SEC', display_name: 'SECUNDARIA' },
  { key: 'BAC', display_name: 'BACHILLER' },
  { key: 'UNIV', display_name: 'UNIVERSITARIA' },
  { key: 'PROF', display_name: 'PROFESIONAL' }
]

export default {
  name: 'DonorList',
  components: { ReportDialog, VueMomentsAgo, EnableDonor, DonorJoin },
  directives: {},
  filters: {},
  data() {
    return {
      errGif: errGif + '?' + +new Date(),
      pdf: null,
      dialogFormEnableDonorVisible: false,
      reportDialogVisible: false,
      reportDialogLoading: false,
      dialogCannotDonation: false,
      tableKey: 0,
      list: null,
      total: null,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        offset: 0,
        importance: '',
        title: '',
        search: '',
        ordering: '-code'
      },
      importanceOptions: [1, 2, 3],
      countryOptions: COUNTRIES,
      maritalOptions,
      departamentOptions: DEPARTMENT_OPTIONS,
      gradeOptions,
      sortOptions: [{ label: 'ID Ascending', key: '+id' }, { label: 'ID Descending', key: '-id' }],
      statusOptions: ['published', 'draft', 'deleted'],
      temp: {
        id: undefined,
        code: '',
        civil_status: '',
        first_name: '',
        last_name: '',
        birth_date: '',
        gender: '',
        country: '',
        residence: '',
        zone: '',
        department: '',
        phone: undefined,
        mobile_phone: undefined,
        family_phone: undefined,
        profession: '',
        degree_instruction: '',
        job: '',
        job_address: '',
        email: ''
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Editando Donante',
        create: 'Creando Donante',
        join: 'Unir Donantes',
        enable: 'Hablitar Donante'
      },
      rules: {
        code: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }, { type: 'number', message: 'Debe ser número', trigger: 'blur' }],
        civil_status: [{ required: false, message: this.$t('is_required'), trigger: 'change' }],
        first_name: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        ci: [{ required: false, message: this.$t('is_required'), trigger: 'blur' }],
        middle_name: [{ required: false, message: this.$t('is_required'), trigger: 'blur' }],
        last_name: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        birth_date: [{ type: 'string', required: true, message: this.$t('is_required'), trigger: 'change' }],
        // age: [{ required: true, message: this.$t('is_required') }, { type: 'number', message: 'Debe ser número', trigger: 'blur' }],
        gender: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        country: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],

        residence: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        zone: [{ required: false, message: this.$t('is_required'), trigger: 'blur' }],
        department: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        phone: [],
        mobile_phone: [],
        family_phone: [],
        profession: [{ required: false, message: this.$t('is_required'), trigger: 'blur' }],
        degree_instruction: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        job: [{ required: false, message: this.$t('is_required'), trigger: 'blur' }],
        job_address: [{ required: false, message: this.$t('is_required'), trigger: 'blur' }],
        email: [{ type: 'email', message: 'Introduzca un correo válido', trigger: ['blur', 'change'] }]
      },
      isAreaPromotion: false,
      row: null,
      pickerOptionsBirthDate: {
        disabledDate(time) {
          const date = new Date()
          return time.getTime() > (date.getTime() - 3600 * 1000 * 24 * 365 * 15)
        }
      },
      widthDialog: null,
      multipleSelection: [],
      buttonJoin: true,
      dynamicTags: [],
      inputVisible: false,
      inputValue: ''
    }
  },
  computed: {
    age: function() {
      var age = 0
      if (this.temp.birth_date) {
        age = moment().diff(this.temp.birth_date, 'years')
      }
      return age
    }
  },
  watch: {
    multipleSelection: function(value) {
      this.buttonJoin = value.length <= 1
    },
    'temp.phone': function() {
      if (this.temp.phone === '') {
        this.temp.phone = null
      }
    },
    'temp.mobile_phone': function() {
      if (this.temp.mobile_phone === '') {
        this.temp.mobile_phone = null
      }
    },
    'temp.family_phone': function() {
      if (this.temp.family_phone === '') {
        this.temp.family_phone = null
      }
    }
  },
  created() {
    if (this.$route.name === 'promotions-donor') {
      this.isAreaPromotion = true
    }
    this.getList()
  },
  methods: {
    checkPermission,
    handleSelected(row, actionNew = false) {
      if (!row.is_available_for_new_donation) {
        const maxMonths = (row.gender === 'M') ? 3 : 4
        var lastEffectiveDonation = moment(row.last_effective_donation_at)
        var lastDonation = moment(row.last_effective_donation_at)
        var nextDonation = lastDonation.add(maxMonths, 'month').add(1, 'days')

        this.$notify({
          title: 'El donante no puede donar',
          message: 'Aún no pasaron ' + maxMonths +
            ' meses desde su ultima donación que fué el ' + lastEffectiveDonation.format('DD-MM-YYYY') + ', puede donar a partir del ' + nextDonation.format('DD-MM-YYYY'),
          type: 'warning',
          duration: 5000
        })
        return
      }

      if (row.can_donate) {
        if (!actionNew) {
          this.handleUpdate(row)
        }
        Cookies.set('donationDonor', {
          id: row.id,
          code: row.code,
          first_name: row.first_name,
          middle_name: row.middle_name,
          last_name: row.last_name,
          last_donation_at: row.last_effective_donation_at
        })
        this.$notify({
          title: 'Donante Seleccionado',
          message: 'Se ha seleccionado al donante: ' + row.code + ' ' + row.first_name + ' ' + row.middle_name + ' ' + row.last_name + ', Ahora presione siguiente ',
          type: 'success',
          duration: 2000
        })
        this.$emit('selectedDonor', false)
      } else {
        this.dialogCannotDonation = true
        setTimeout(() => {
          this.dialogCannotDonation = false
        }, 4000)
      }
    },
    getList() {
      this.listLoading = true

      let query = donors.list_small(this.listQuery)

      if (this.isAreaPromotion) {
        query = donors.list_volunteers(this.listQuery)
      }
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'donors',
          query: query
        }
      ).then(response => {
        const data = response.data
        this.list = data.donors.results
        this.total = data.donors.totalCount
        this.listLoading = false
      })
    },
    handleFilter: debounce(function() {
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
    handleOrderChange(val) {
      if (val['prop']) {
        this.listQuery.ordering = (val['order'] === 'descending' ? '-' : '') + val['prop']
        this.getList()
      }
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
        ci: '',
        ci_extension: '',
        code: '',
        code_other: '',
        civil_status: '',
        first_name: '',
        last_name: '',
        birth_date: '',
        gender: '',
        country: '',
        residence: '',
        zone: '',
        department: '',
        phone: undefined,
        mobile_phone: undefined,
        family_phone: undefined,
        profession: '',
        degree_instruction: '',
        job: '',
        job_address: '',
        email: ''
      }
    },
    handleNextCode() {
      graphqlRequest(
        {
          from: this.$route.name,
          query: donors.getNextCode()
        }
      ).then(response => {
        this.temp.code = response.data['next_donor_code']
      })
    },
    handleCreate() {
      this.resetTemp()
      this.dynamicTags = this.temp.code_other ? this.temp.code_other.split(',') : []
      this.handleNextCode()

      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    getDonor(id) {
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'donors',
          query: donors.showDonor(id)
        }
      ).then(response => {
        this.handleSelected(response.data.donor, true)
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.age = this.age
          tempData.code_other = this.dynamicTags.join(',')
          tempData.code = this.temp.code + ''
          tempData.family_phone = +this.temp.family_phone
          tempData.mobile_phone = +this.temp.mobile_phone
          tempData.phone = +this.temp.phone

          if (tempData.ci === '') {
            tempData.ci = undefined
          }

          graphqlRequest(
            {
              from: this.$route.name,
              service: 'createDonor',
              query: donors.createDonor(),
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
              if (this.$route.name === 'registry-fast') {
                this.getDonor(response.data.create_donor.donor.id)
              }
              this.dialogFormVisible = false
              this.$notify({
                title: 'Mensaje',
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
      const id = row.id
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'donors',
          query: donors.showDonor(id)
        }
      ).then(response => {
        const data = response.data
        this.temp = data.donor
        this.dynamicTags = this.temp.code_other ? this.temp.code_other.split(',') : []
        this.dialogStatus = 'update'
        this.dialogFormVisible = true
        this.$nextTick(() => {
          this.$refs['dataForm'].clearValidate()
        })
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.age = this.age
          tempData.code_other = this.dynamicTags.join(',')
          tempData.code = this.temp.code + ''
          tempData.family_phone = +this.temp.family_phone
          tempData.mobile_phone = +this.temp.mobile_phone
          tempData.phone = +this.temp.phone

          delete tempData['image']
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'updateDonor',
              query: donors.updateDonor(),
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
                title: 'Mensaje',
                message: 'Registro actualizado',
                type: 'success',
                duration: 2000
              })
            }
          })
        }
      })
    },
    handlePrintDonorVolunteer(row) {
      this.reportDialogVisible = true
      this.reportDialogLoading = true
      const tempData = Object.assign({}, row)
      printDonorVolunteer(tempData.id).then(
        response => {
          this.pdf = response
          this.reportDialogLoading = false
        }
      )
    },
    enableDonor(row) {
      this.dialogStatus = 'enable'
      this.widthDialog = '60%'
      this.dialogFormEnableDonorVisible = true
      this.row = row
    },
    handleCloseForm() {
      if (this.dialogStatus === 'join') {
        this.$refs.Receptor.buttonJoin = true
      }
      this.getList()
      this.dialogFormEnableDonorVisible = false
    },
    handleJoin() {
      this.dialogStatus = 'join'
      this.widthDialog = '85%'
      this.dialogFormEnableDonorVisible = true
    },
    handleSelectionChange(val) {
      this.multipleSelection = val
    },
    handleClose(tag) {
      this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1)
    },
    showInput() {
      this.inputVisible = true
      this.$nextTick(_ => {
        this.$refs.saveTagInput.$refs.input.focus()
      })
    },

    handleInputConfirm() {
      const inputValue = this.inputValue
      if (inputValue) {
        this.dynamicTags.push(inputValue)
      }
      this.inputVisible = false
      this.inputValue = ''
    }
  }
}
</script>
<style>
  .customize-ci .el-select .el-input {
    width: 80px;
  }
  .text-red {
    color: red;
  }
</style>

<template>
  <div class="createPost-container">
    <el-form ref="dataForm" :model="temp" :rules="rules" label-position="left" label-width="120px" style="width: 100%;">
      <el-row :gutter="20">
        <el-col :md="14" :sm="24">
          <div class="grid-content">

            <el-form-item :label="$t('models.extractionRefreshment.extraction')" prop="extraction_id">
              <el-select
                v-if="dialogStatus === 'create' && !rowExtraction"
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
                  <span style="float: right; color: #8492a6; font-size: 13px">
                    {{ item.donation.register_at| toHumanDateMonthLetter }}
                  </span>
                </el-option>
              </el-select>
              <strong v-if="dialogStatus === 'update'" class="text-text-green-sea">
                {{ temp.extraction.donation.donor.code }}
              </strong>
              <strong v-if="dialogStatus === 'create' && rowExtraction" class="text-text-green-sea">
                {{ rowExtraction.donation.donor.code }}
              </strong>
            </el-form-item>

            <el-form-item :label="$t('models.extractionRefreshment.menu')" prop="menu_id">
              <el-select v-model="temp.menu_id" automatic-dropdown class="filter-item" filterable>
                <el-option-group v-for="group in list_menu" :key="group.label" :label="group.label">
                  <el-option v-for="item in group.options" :key="item.value" :label="item.label" :value="item.value">
                    <span style="float: left">{{ item.label }}</span>
                    <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
                  </el-option>
                </el-option-group>
              </el-select>
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
          </div>
        </el-col>
      </el-row>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="dialogStatus==='create'?createData():updateData()">{{ $t('confirm') }}
      </el-button>
    </div>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import { graphqlRequest } from '@/api/graphql'
import extractions from '@/query/extraction'
import menus from '@/query/menu'
import { mapGetters } from 'vuex'
import extractionRefreshments from '@/query/extractionRefreshment'
import moment from 'moment'

export default {
  name: 'ExtractionRefreshmentForm',
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
      extractions: null,
      loadingMenu: false,
      loadingExtraction: false,
      listExtractionQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-id' },
      listExtractionRefreshmentQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-id' },
      temp: {
        id: undefined,
        extraction_id: undefined,
        menu_id: undefined,
        register_at: moment().format('YYYY-MM-DD')
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Editando Asignacion de Refrigerio',
        create: 'Creando Asignacion de  Refrigerio'
      },
      rules: {
        extraction_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        menu_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }]
      },
      downloadLoading: false,
      list_menu: [],
      generalList: [],
      volunteerList: [],
      isEdit: false
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
    'temp.extraction_id': function(value) {
      if (this.dialogStatus === 'create' && this.rowExtraction === null) {
        if (value !== undefined) {
          this.getExtraction(value)
        }
      }
    }
  },
  mounted() {
    this.determineAction()
  },
  methods: {
    checkPermission,
    determineAction() {
      if (this.row != null) {
        this.handleUpdate(this.row)
        this.isEdit = true
      } else {
        this.handleCreate()
        this.isEdit = false
      }
    },
    getExtraction(id) {
      const extraction = this.extractions.filter(function(item) {
        return item.id === id
      })
      this.setMenuList(extraction[0])
    },
    getListMenus() {
      this.loadingMenu = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'menus',
          query: menus.list(this.listExtractionRefreshmentQuery)
        }
      ).then(response => {
        const data = response.data
        this.groupedMenuListMethod(data.menus.results)
        this.loadingMenu = false
      })
    },
    groupedMenuListMethod(menus) {
      var volunteerList = [{ label: 'VOLUNTARIOS', options: [] }, { label: 'GENERAL', options: [] }]
      var generalList = [{ label: 'GENERAL', options: [] }, { label: 'VOLUNTARIOS', options: [] }]

      for (const tar of menus) {
        switch (tar.only_volunteer) {
          case true:
            volunteerList[0].options.push({ label: tar.name, value: tar.id })
            generalList[1].options.push({ label: tar.name, value: tar.id })
            break
          case false:
            volunteerList[1].options.push({ label: tar.name, value: tar.id })
            generalList[0].options.push({ label: tar.name, value: tar.id })
            break
        }
      }

      this.volunteerList = volunteerList
      this.generalList = generalList

      if (this.rowExtraction) {
        this.setMenuList(this.rowExtraction)
      }
    },
    setMenuList(extraction) {
      if (extraction && extraction.donation.type_donation === 'VA') {
        this.list_menu = this.volunteerList
      } else {
        this.list_menu = this.generalList
      }
    },
    getListExtractions() {
      this.loadingExtraction = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'extractions',
          query: extractions.refreshmentExtractionSelect(this.listExtractionQuery)
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
    resetTemp() {
      this.temp = {
        id: undefined,
        extraction_id: undefined,
        menu_id: undefined,
        register_at: moment().format('YYYY-MM-DD')
      }
    },
    handleCreate() {
      this.getListMenus()
      this.getListExtractions()
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      if (this.rowExtraction) {
        this.temp.extraction_id = this.rowExtraction.id
      }
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
              service: 'createExtractionRefreshment',
              query: extractionRefreshments.createExtractionRefreshment(),
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
              this.resetTemp()
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
      this.getListMenus()
      const tempData = Object.assign({}, row)
      tempData.extraction_id = tempData.extraction.id
      tempData.menu_id = tempData.menu.id
      tempData.employee_id = tempData.employee.id
      this.temp = tempData
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.setMenuList(row.extraction)
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
              service: 'updateExtractionRefreshment',
              query: extractionRefreshments.updateExtractionRefreshment(),
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

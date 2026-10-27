<template>
  <div class="app-container">
    <div class="filter-container">
      <el-row :gutter="20" style="width: 100%">
        <el-col :md="8">
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
        <el-col :md="12">
          <div class="block">
            <span class="demonstration">Hemocomponente</span>
            <el-select v-model="listQuery.typehemocomponent_id" clearable filterable placeholder="Select" @change="handleFilter">
              <el-option
                v-for="item in typeHemocomponents"
                :key="item.id"
                :label="item.name"
                :value="item.id"
              >
                <span style="float: left">{{ item.name }}</span>
                <span style="float: right; color: #8492a6; font-size: 13px">{{ item.acronym }}</span>
              </el-option>
            </el-select>
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
      <el-badge v-if="massiveDiscardItemsCount > 0" :value="massiveDiscardItemsCount" class="item">
        <el-button
          v-if="checkPermission(['add_discard'])"
          class="filter-item"

          style="margin-left: 10px;"
          @click="handleOpenDialog({}, 'DM')"
        >Descartar
        </el-button>
      </el-badge>
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      :default-sort="{prop: 'register_at', order: 'descending'}"
      border
      fit
      highlight-current-row
      style="width: 100%;"
    >
      <el-table-column :label="$t('models.release.register_at')" align="center" fixed prop="register_at" sortable="custom" width="100px">
        <template slot-scope="scope">
          <span>{{ scope.row.register_at | toHumanDate }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.release.code')" align="center" width="100px">
        <template slot-scope="scope">
          <span>
            <strong>{{ scope.row.itemfragmentation.donor_code }}</strong>
          </span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.release.hemocomponent')" width="350px">
        <template slot-scope="scope">
          <span>{{ scope.row.itemfragmentation.typehemocomponent.name }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.release.extraction_date')" align="center" width="180px">
        <template slot-scope="scope">
          <span>{{ scope.row.itemfragmentation.fragmentation.extraction.register_at | toHumanDate }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.release.expiration_date')" align="center" width="160px">
        <template slot-scope="scope">
          <span>{{ scope.row.itemfragmentation.expiration_date | toHumanDate }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.release.observations')" align="center" width="155px">
        <template slot-scope="scope">
          <span>{{ scope.row.observations }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.release.employee')" align="center" min-width="200">
        <template slot-scope="scope">
          <span>{{ scope.row.employee | fullName }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('actions')" align="center" class-name="small-padding" fixed="right" width="200">
        <template slot-scope="scope">
          <el-button
            v-if="checkPermission(['change_release'])"
            size="mini"
            type="primary"
            @click="handleOpenDialog(scope.row, 'L')"
          >{{ 'Modificar' }}
          </el-button>
          <el-tooltip class="item" content="Etiqueta de Bolsa" effect="dark">
            <el-button
              class="filter-item"
              size="mini"
              style="margin-left: 10px;"
              type="info"
              @click="handlePrintBloodBag(scope.row.itemfragmentation.id)"
            >
              <font-awesome-icon icon="file-medical" />
            </el-button>
          </el-tooltip>
          <el-tooltip
            v-if="isExpirationDate(scope.row.itemfragmentation)"
            class="item"
            content="Marcar para Descarte"
            effect="dark"
          >
            <el-button
              :disabled="massiveDiscardItems.hasOwnProperty(scope.row.itemfragmentation.id)"
              size="mini"
              @click="addDiscardMassiveItem(scope.row.itemfragmentation)"
            >
              <font-awesome-icon icon="check" />
            </el-button>
          </el-tooltip>
          <el-tooltip class="item" content="Eliminar" effect="dark">
            <el-popconfirm
              v-if="scope.row.itemfragmentation.distributionitemfragmentations.length === 0 && checkPermission(['delete_release'])"
              cancel-button-text="No, Gracias"
              confirm-button-text="Si, estoy seguro"
              icon="el-icon-info"
              icon-color="red"
              title="Esta seguro de eliminar? No habrá forma de revertir esta acción"
              @onConfirm="deleteData(scope.row)"
            >
              <el-button slot="reference" size="mini" style="margin-left: 10px;" >
                <font-awesome-icon icon="times" />
              </el-button>
            </el-popconfirm>
          </el-tooltip>
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
    <el-dialog :title="titleReport" :visible.sync="reportDialogVisible" center top="10px" width="100%">
      <report-dialog v-if="!reportDialogLoading" :row="pdf" />
      <div v-if="reportDialogLoading" class="loading-report">
        <i class="el-icon-loading" style="font-size: 80px" />
      </div>
    </el-dialog>
    <el-dialog :before-close="handleCloseForm" :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible" destroy-on-close width="90%">
      <release-form v-if="dialogStatus!=='discard_massive'" :row="temp" @dialogStatus="handleCloseForm" />
      <discard-massive-form
        v-if="dialogStatus==='discard_massive'"
        :row="massiveDiscardItems"
        @clearItems="clearDiscardItems"
        @dialogStatus="handleCloseForm"
        @list-added="removeDiscardItem($event)"
      />
    </el-dialog>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import { graphqlRequest } from '@/api/graphql'
import releases from '@/query/release'
import ReleaseForm from './ReleaseForm'
import DiscardMassiveForm from '../DiscardMassiveForm'
import { printBloodBag } from '@/api/itemFragmentation'
import ReportDialog from '../../report-dialog/ReportDialog'
import { debounce } from 'debounce'
import { defaultshorcouts } from '@/utils/date-utils'
import moment from 'moment'
import typehemocomponents from '@/query/type-hemocomponent'

export default {
  name: 'ReleaseList',
  components: { ReportDialog, ReleaseForm, DiscardMassiveForm },
  data() {
    return {
      pickerRangeOptions: {
        disabledDate(time) {
          return time.getTime() > Date.now()
        },
        shortcuts: defaultshorcouts()
      },
      tableKey: 0,
      list: null,
      total: null,
      loading: false,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        offset: 0,
        search: '',
        ordering: '-id',
        typehemocomponent_id: '',
        date_range: [moment().startOf('month').format('YYYY-MM-DD'), moment().format('YYYY-MM-DD')]
      },
      listTypeHemocomponentQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: 'name' },
      pdf: null,
      temp: {},
      reportDialogVisible: false,
      reportDialogLoading: false,
      titleReport: '',
      dialogStatus: '',
      dialogFormVisible: false,
      dateNow: moment(new Date()),
      massiveDiscardItems: {},
      massiveDiscardItemsCount: 0,
      typeHemocomponents: [],
      typeHemocomponentLoading: false,
      textMap: {
        release: 'Modificando Liberación',
        discard_massive: 'Creando Descarte Masivo'
      }
    }
  },
  computed: {},
  watch: {},
  created() {
    this.getList()
    this.getListTypeHemocomponents()
  },
  methods: {
    checkPermission,
    isExpirationDate(row) {
      return moment(row.expiration_date).isBefore(this.dateNow)
    },
    addDiscardMassiveItem(row) {
      this.massiveDiscardItems[row.id] = row
      this.massiveDiscardItemsCount = Object.keys(this.massiveDiscardItems).length
    },
    clearDiscardItems() {
      this.massiveDiscardItems = {}
      this.massiveDiscardItemsCount = Object.keys(this.massiveDiscardItems).length
    },
    removeDiscardItem(row) {
      delete this.massiveDiscardItems[row.id]
      this.massiveDiscardItemsCount = Object.keys(this.massiveDiscardItems).length
    },
    getList() {
      this.listLoading = true

      graphqlRequest(
        {
          from: this.$route.name,
          query: releases.listRelease(this.listQuery),
          variables: this.listQuery
        }
      ).then(response => {
        const data = response.data
        this.list = data.releases.results
        this.total = data.releases.totalCount
        this.listLoading = false
      })
    },
    handlePrintBloodBag(id) {
      this.reportDialogVisible = true
      this.reportDialogLoading = true
      this.titleReport = 'BOLSA DE SANGRE'
      printBloodBag(id).then(
        response => {
          this.pdf = response
          this.reportDialogLoading = false
        }
      )
    },
    handleCloseForm() {
      this.dialogFormVisible = false
      this.getList()
    },
    handleOpenDialog(row, x) {
      this.dialogFormVisible = true
      switch (x) {
        case 'L':
          row.release = 1
          this.dialogStatus = 'release'
          break
        case 'DM':
          this.dialogStatus = 'discard_massive'
          row = null
          this.massiveDiscardItems = Object.assign({}, this.massiveDiscardItems)
          break
        default:
          break
      }
      this.temp = row
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
    deleteData(row) {
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'deleteRelease',
          query: releases.deleteRelease(),
          variables: { id: row.id }
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
            message: 'Registro eliminado',
            type: 'success',
            duration: 2000
          })
          this.getList()
        }
      })
    }
  }
}
</script>

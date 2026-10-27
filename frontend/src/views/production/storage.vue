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
              range-separator="A"
              start-placeholder="Fecha Inicial"
              format="dd-MM-yyyy"
              type="daterange"
              value-format="yyyy-MM-dd"
              unlink-panels
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
        :placeholder="$t('donors.search')"
        :autofocus="'autofocus'"
        class="filter-item"
        clearable
        prefix-icon="el-icon-search"
        @input="handleFilter"
      />
      <el-badge v-if="massiveReleaseItemsCount > 0" :value="massiveReleaseItemsCount" class="item">
        <el-button
          v-if="checkPermission(['add_release'])"
          class="filter-item"
          style="margin-left: 10px;"
          type="primary"

          @click="handleOpenDialog({}, 'LM')"
        >Liberar
        </el-button>
      </el-badge>
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
      :row-class-name="tableRowClassName"
      border
      fit
      highlight-current-row
      style="width: 100%;"
      @sort-change="handleOrderChange"
    >
      <el-table-column :label="$t('models.storage.register_at')" align="center" fixed prop="register_at" sortable="custom" width="100px">
        <template slot-scope="scope">
          <span>{{ scope.row.fragmentation.extraction.register_at | toHumanDate }}</span>
        </template>
      </el-table-column>
      <el-table-column
        :label="$t('models.storage.code')"
        width="100px"
        align="center"
        prop="donor_code"
        sortable="custom"
      >
        <template slot-scope="scope">
          <span v-if="scope.row.fragmentation">
            <strong>{{ scope.row.donor_code }}</strong>
          </span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.storage.name')" align="center" width="255px">
        <template slot-scope="scope">
          <span>
            {{ scope.row.typehemocomponent.name }}
          </span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.extraction.status')" align="center" width="100px">
        <template slot-scope="scope">
          <el-tag
            v-if="scope.row.fragmentation.extraction.donation.immunohematology || scope.row.fragmentation.extraction.donation.immunoserology"
            :type="scope.row.adversereaction? 'danger': ''"
          >
            <el-tooltip v-if="scope.row.fragmentation.extraction.donation.immunohematology" content="Inmunohematologia" effect="dark" placement="top">
              <font-awesome-icon icon="dna" />
            </el-tooltip>
            <el-tooltip v-if="scope.row.fragmentation.extraction.donation.immunoserology" content="Inmunoserología" effect="dark" placement="top">
              <font-awesome-icon icon="biohazard" />
            </el-tooltip>
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.storage.type_irregular_antibody')" align="center" width="255px">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.type_irregular_antibody" >{{ scope.row.type_irregular_antibody.name }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.storage.weight')" align="right" width="80px">
        <template slot-scope="scope">
          <span>{{ scope.row.weight }} ml.</span>
        </template>
      </el-table-column>
      <el-table-column
        :label="$t('models.storage.expiration_date')"
        width="190px"
        align="center"
        prop="expiration_date"
        sortable="custom"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.expiration_date | toHumanDate }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.storage.pre_discard')" align="center" width="155px">
        <template slot-scope="scope">
          <span>{{ scope.row.typediscard ? 'SI' : 'NO' }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.storage.status')" align="center" width="185px">
        <template slot-scope="scope">
          <el-tag>
            <span>{{ getStatus(scope.row) }}</span>
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.storage.employee')" align="center" width="255px">
        <template slot-scope="scope">
          <span>{{ scope.row.fragmentation.employee | fullName }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('actions')" align="center" class-name="small-padding" fixed="right" width="320">
        <template slot-scope="scope">
          <el-button
            v-if="checkPermission(['add_discard'])"
            :disabled="scope.row.release!==null || scope.row.discard!==null"
            size="mini"
            type="primary"
            @click="handleOpenDialog(scope.row, 'D')"
          >{{ 'Descartar' }}
          </el-button>
          <el-button
            v-if="checkPermission(['add_release'])"
            :disabled="isRelease(scope.row)"
            size="mini"
            type="primary"
            @click="handleOpenDialog(scope.row, 'L')"
          >{{ 'Liberar' }}
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
    <el-dialog :visible.sync="reportDialogVisible" center title="Reporte" top="10px" width="100%">
      <report-dialog v-if="!reportDialogLoading" :row="pdf" />
      <div v-if="reportDialogLoading" class="loading-report">
        <i class="el-icon-loading" style="font-size: 80px" />
      </div>
    </el-dialog>

    <el-dialog :before-close="handleCloseForm" :visible.sync="dialogFormVisible" width="98%">
      <span v-if="dialogStatus==='discard' || dialogStatus==='release'" slot="title" class="dialog-footer">
        {{ textMap[dialogStatus] }} <el-tag>{{ temp.donor_code }}</el-tag>
        <h3 v-if="temp.typehemocomponent">{{ temp.typehemocomponent.name }}</h3>
      </span>
      <span v-else slot="title" class="dialog-footer">{{ textMap[dialogStatus] }}</span>
      <discard-form v-if="dialogStatus==='discard'" :row="temp" @dialogStatus="handleCloseForm" />
      <release-form v-if="dialogStatus==='release'" :row="temp" @dialogStatus="handleCloseForm" />
      <release-massive-form
        v-if="dialogStatus==='release_massive'"
        :row="massiveReleaseItems"
        @clearItems="clearReleaseItems"
        @dialogStatus="handleCloseForm"
        @list-added="removeReleaseItem($event)"
      />
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
import ReportDialog from '../report-dialog/ReportDialog'
import DiscardForm from './discard/DiscardForm'
import ReleaseForm from './release/ReleaseForm'
import ReleaseMassiveForm from './ReleaseMassiveForm'
import DiscardMassiveForm from './DiscardMassiveForm'
import { graphqlRequest } from '@/api/graphql'
import itemFragmentations from '@/query/itemFragmentation'
import { debounce } from 'debounce'
import { defaultshorcouts } from '@/utils/date-utils'
import moment from 'moment'
import typehemocomponents from '@/query/type-hemocomponent'
import { PROCESS_AFERESIS } from '@/utils/const'
import {buildBarcodeFilter, buildRegisterAtFilter} from "@/utils/general";

export default {
  name: 'Storage',
  components: { ReportDialog, DiscardForm, ReleaseForm, ReleaseMassiveForm, DiscardMassiveForm },
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
      tableKey: 0,
      list: [],
      total: null,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        offset: 0,
        search: '',
        ordering: '-register_at',
        typehemocomponent_id: '',
        date_range: [moment().startOf('month').format('YYYY-MM-DD'), moment().format('YYYY-MM-DD')]
      },
      listTypeHemocomponentQuery: { page: 1, limit: 50, offset: 0, search: '', ordering: 'name' },
      temp: { id: undefined },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        discard: 'Creando Descarte',
        release: 'Creando Liberación',
        discard_massive: 'Creando Descarte Masivo',
        release_massive: 'Creando Liberación Masiva'
      },
      massiveReleaseItems: {},
      massiveReleaseItemsCount: 0,
      massiveDiscardItems: {},
      massiveDiscardItemsCount: 0,
      typeHemocomponents: [],
      typeHemocomponentLoading: false
    }
  },
  computed: {},
  watch: {
    'temp.fragmentation_id': function() {
      this.getFragmentation(this.temp.fragmentation_id)
    }
  },
  created() {
    this.getList()
    this.getListTypeHemocomponents()
  },
  methods: {
    checkPermission,
    getStatus(row) {
      if (row && row.distributionitemfragmentations && row.distributionitemfragmentations.length > 0) {
        return 'DISTRIBUIDO'
      } else if (row.discard) {
        return 'DESCARTADO'
      } else if (row.release) {
        return 'LIBERADO'
      } else if (row.fragmentation.extraction.donation.immunohematology || row.fragmentation.extraction.donation.immunoserology) {
        return 'EN LABORATORIO'
      } else {
        return 'EN FRACCIONAMIENTO'
      }
    },
    tableRowClassName({ row, rowIndex }) {
      const isReactiveInmunoserologia = this.isReactiveInmunoserology(row.fragmentation.extraction.donation.immunoserology)

      if (isReactiveInmunoserologia) {
        return 'error-row'
      } else if (row.typediscard !== null) {
        return 'warning-row'
      }
      return ''
    },
    isRelease(row) {
      if (row !== null) {
        return row.release !== null || row.discard !== null || row.typediscard !== null || this.isReactiveInmunoserology(row.fragmentation.extraction.donation.immunoserology)
      }
      return false
    },
    isReactiveInmunoserology(immunoserology) {
      if (immunoserology === null) {
        return false
      } else {
        return (immunoserology.is_reactive)
      }
    },
    getList() {
      this.listLoading = true
      let tempListQuery = Object.assign({}, this.listQuery)

      tempListQuery = buildBarcodeFilter(tempListQuery, 'fragmentation__extraction__donation__id')
      tempListQuery = buildRegisterAtFilter(tempListQuery)

      if (tempListQuery.typehemocomponent_id === '') {
        tempListQuery.typehemocomponent_id = null
      }

      graphqlRequest(
        {
          from: this.$route.name,
          service: 'itemFragmentations',
          query: itemFragmentations.listQuarantine(tempListQuery),
          variables: tempListQuery
        }
      ).then(response => {
        const data = response.data
        this.list = data.itemfragmentations.results
        this.total = data.itemfragmentations.totalCount
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
    handleOrderChange(val) {
      if (val['prop']) {
        this.listQuery.ordering = (val['order'] === 'descending' ? '-' : '') + val['prop']
        this.getList()
      }
    },
    handleOpenDialog(row, x) {
      this.dialogFormVisible = true
      switch (x) {
        case 'D':
          this.dialogStatus = 'discard'
          break
        case 'L':
          this.dialogStatus = 'release'
          break
        case 'LM':
          this.dialogStatus = 'release_massive'
          row = null
          this.massiveReleaseItems = Object.assign({}, this.massiveReleaseItems)
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
    handleCloseForm() {
      this.dialogFormVisible = false
      this.getList()
    },
    clearReleaseItems() {
      this.massiveReleaseItems = {}
      this.massiveReleaseItemsCount = Object.keys(this.massiveReleaseItems).length
    },
    clearDiscardItems() {
      this.massiveDiscardItems = {}
      this.massiveDiscardItemsCount = Object.keys(this.massiveDiscardItems).length
    },
    removeDiscardItem(row) {
      delete this.massiveDiscardItems[row.id]
      this.massiveDiscardItemsCount = Object.keys(this.massiveDiscardItems).length
    },
    removeReleaseItem(row) {
      delete this.massiveReleaseItems[row.id]
      this.massiveReleaseItemsCount = Object.keys(this.massiveReleaseItems).length
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
    addForReleaseOrDiscard(row) {
      let message = ''
      if (checkPermission(['add_release']) && !this.isRelease(row) && (row.fragmentation.extraction.donation.immunohematology && row.fragmentation.extraction.donation.immunoserology)) {
        this.massiveReleaseItems[row.id] = row
        this.massiveReleaseItemsCount = Object.keys(this.massiveReleaseItems).length
        message += 'Liberar'
      }
      if (checkPermission(['add_discard']) && row.release === null && row.discard === null) {
        this.massiveDiscardItems[row.id] = row
        this.massiveDiscardItemsCount = Object.keys(this.massiveDiscardItems).length
        message += message !== '' ? ' o Descartar' : 'Descartar'
      }

      this.$notify({
        title: 'Estado',
        message: `Hemocomponente Agregado para ${message}`,
        type: 'success',
        duration: 2000
      })
    }
  }
}
</script>
<style>
  .el-table .warning-row {
    background: oldlace;
  }

  .el-table .success-row {
    background: #f0f9eb;
  }

  .el-table .error-row {
    background: rgba(255, 0, 4, 0.22);
  }

  .el-table .warning-fg {
    color: #f79e1b;
  }

  .el-table .success-fg {
    color: #f0f9eb;
  }

  .el-table .error-fg {
    color: rgba(255, 21, 29, 0.98);
  }
</style>

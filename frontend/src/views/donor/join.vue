<template>
  <div class="app-container">
    <div class="filter-container">
      <el-tag>Seleccione la fila principal</el-tag>
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="row"
      border
      style="width: 100%;"
    >
      <el-table-column :label="$t('models.patient.code')" width="170px" align="center" prop="register_at">
        <template slot-scope="scope">
          <span>{{ scope.row.code }}
            <small v-if="scope.row.code_other"><br>{{ scope.row.code_other }}</small>
          </span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.patient.ci')" width="120px" prop="ci">
        <template slot-scope="scope">
          <span>{{ scope.row.ci }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.patient.first_name')" width="170px" prop="first_name">
        <template slot-scope="scope">
          <span>{{ scope.row.first_name }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.patient.middle_name')" width="170px" prop="middle_name">
        <template slot-scope="scope">
          <span>{{ scope.row.middle_name }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.patient.last_name')" width="170px" prop="last_name">
        <template slot-scope="scope">
          <span>{{ scope.row.last_name }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.patient.birth_date')" width="170px">
        <template slot-scope="scope">
          <span>{{ scope.row.birth_date | toHumanDate }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.patient.gender')" width="100px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.gender | genderFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column width="300px" align="center">
        <template slot-scope="scope">
          <el-button @click="handleSelected(scope.row)">Seleccionar como principal</el-button>
        </template>
      </el-table-column>
    </el-table>
    <br>
    <div slot="footer" class="dialog-footer" style="text-align: right">
      <el-button :disabled="buttonJoin" @click="handleUpdate()">{{ $t('confirm') }}</el-button>
    </div>
  </div>
</template>

<script>
import donors from '@/query/donor'
import { graphqlRequest } from '@/api/graphql'

const genderOptions = [
  { key: 'F', display_name: 'Femenino' },
  { key: 'M', display_name: 'Masculino' }
]

const genderTypeKeyValue = genderOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'DonorJoin',
  components: {},
  directives: {},
  filters: {
    genderFilter(type) {
      return genderTypeKeyValue[type]
    }
  },
  props: {
    row: {
      type: Array,
      default: null
    }
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: null,
      listLoading: false,
      listQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-register_at' },
      temp: { id: undefined, items: [] },
      buttonJoin: true
    }
  },
  mounted() {
    this.buttonJoin = true
  },
  methods: {
    handleUpdate() {
      this.$confirm(this.$t('messageConfirmJoin'), 'Mensaje', {
        confirmButtonText: this.$t('confirmButtonText'),
        cancelButtonText: this.$t('cancelButtonText'),
        type: 'warning'
      }).then(() => {
        this.updateData()
      }).catch(() => {
        // cancel
      })
    },
    updateData() {
      const tempData = Object.assign({}, this.temp)
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'joinDonor',
          query: donors.joinDonor(),
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
            title: 'Mensaje',
            message: 'Registro actualizados',
            type: 'success',
            duration: 2000
          })
        }
      })
    },
    handleSelected(row) {
      const tempData = Object.assign({}, row)
      tempData.items = []
      for (const l of this.row) {
        if (l.id !== row.id) {
          tempData.items.push({ id: l.id })
        }
      }
      this.temp = tempData
      this.buttonJoin = false
      this.$notify({
        title: 'Mensaje',
        message: 'Fila a mantener seleccionado, Ahora presione "Confirmar"',
        type: 'success',
        duration: 2000
      })
    }
  }
}
</script>

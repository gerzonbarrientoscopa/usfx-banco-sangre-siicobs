<template>
  <div class="app-container">
    <div class="filter-container">
      <el-tag>Seleccione la fila principal</el-tag>
    </div>

    <el-table :key="tableKey" v-loading="listLoading" :data="row" border style="width: 100%;">
      <el-table-column type="index" width="50" align="center" />
      <el-table-column :label="$t('models.institution.register_at')" width="170px" align="center" prop="register_at">
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.register_at | toHumanDate }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.institution.name')" width="120px" prop="name">
        <template slot-scope="scope">
          <span>{{ scope.row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.institution.address')" width="170px" prop="address">
        <template slot-scope="scope">
          <span>{{ scope.row.address }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.institution.phone')" width="170px" prop="phone">
        <template slot-scope="scope">
          <span>{{ scope.row.phone }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.institution.department')" width="170px" prop="department">
        <template slot-scope="scope">
          <span>{{ scope.row.department | departmentOptionsFilter }}</span>
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
import { graphqlRequest } from '@/api/graphql'
import institutions from '@/query/institution'
import { DEPARTMENT_OPTIONS } from '@/utils/const'

const departmentOptionsKeyValue = DEPARTMENT_OPTIONS.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'InstitutionJoin',
  components: {},
  directives: {},
  filters: {
    departmentOptionsFilter(type) {
      return departmentOptionsKeyValue[type]
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
      listLoading: false,
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
          service: 'joinInstitution',
          query: institutions.joinInstitution(),
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
            message: 'Registros actualizados',
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

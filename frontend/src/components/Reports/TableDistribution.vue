<template>
  <el-table :key="tableKey" v-loading="loading" :data="list" border fit highlight-current-row style="width: 100%;">
    <el-table-column fixed type="expand">
      <template slot-scope="props">
        <el-row>
          <el-col :md="24">
            <el-table :data="props.row.itemfragmentations" style="width: 100%">
              <el-table-column align="center" type="index" width="50"/>
              <el-table-column align="center" label="Código" width="120">
                <template slot-scope="scope">
                  <strong>{{ scope.row.itemfragmentation.donor_code }}</strong>
                </template>
              </el-table-column>
              <el-table-column label="Tipo de Hemocomponente" width="500">
                <template slot-scope="scope">
                  {{ scope.row.itemfragmentation.typehemocomponent.name }}
                </template>
              </el-table-column>
              <el-table-column label="Volumen" width="150">
                <template slot-scope="scope">
                  {{ scope.row.itemfragmentation.weight }} ml.
                </template>
              </el-table-column>
            </el-table>
          </el-col>
        </el-row>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.distribution.register_at')" align="center" width="150px">
      <template slot-scope="scope">
        <span>{{ scope.row.register_at | toHumanDatetime }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.distribution.uuid')" width="220px" align="center">
      <template slot-scope="scope">
        {{ scope.row.uuid }}
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.distribution.medical')" width="320px">
      <template slot-scope="scope">
        <span>{{ scope.row.medical | fullName }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.distribution.institution')" width="220px">
      <template slot-scope="scope">
        <span>{{ scope.row.institution.name }}</span><br>
        <small>{{ scope.row.institution.type | institutionTypeValue }}</small>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.distribution.patient')" width="320px">
      <template slot-scope="scope">
        <span>{{ scope.row.patient | fullName }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.distribution.gender')" width="90px" align="center">
      <template slot-scope="scope">
        <span v-if="scope.row.patient">{{ scope.row.patient.gender }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.distribution.age')" width="90px" align="center">
      <template slot-scope="scope">
        <span v-if="scope.row.patient">{{ scope.row.age_patient }} {{ scope.row.age_patient_type }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="'Cantidad'" align="center" width="90px">
      <template slot-scope="scope">
        <span> {{ scope.row.itemfragmentations.length }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.distribution.type_payment')" align="center" width="120px">
      <template slot-scope="scope">
        <span>{{ scope.row.type_payment | receiptOptionsFilter }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.distribution.is_delivered')" align="center" width="140px">
      <template slot-scope="scope">
        <el-tag v-if="!scope.row.is_delivered">EN PROCESO</el-tag>
        <el-tag v-if="scope.row.is_delivered" type="success">ENTREGADO</el-tag>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.distribution.employee')" align="center" width="320px">
      <template slot-scope="scope">
        <span>{{ scope.row.employee | fullName }}</span>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
import {TYPE_PAYMENT_OPTIONS} from '@/utils/const'

const receiptOptionsValue = TYPE_PAYMENT_OPTIONS.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'TableDistribution',
  filters: {
    receiptOptionsFilter(type) {
      return receiptOptionsValue[type]
    }
  },
  props: {
    list: {
      type: Array,
      default: null
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      tableKey: 0
    }
  }
}
</script>

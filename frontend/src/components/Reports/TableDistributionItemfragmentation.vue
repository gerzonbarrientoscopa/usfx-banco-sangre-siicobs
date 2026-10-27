<template>
  <el-table :key="tableKey" v-loading="loading" :data="list" border fit highlight-current-row style="width: 100%;">
    <el-table-column :label="$t('models.distributionitemfragmentation.register_at')" fixed align="center" width="150px">
      <template slot-scope="scope">
        <span>{{ scope.row.distribution.register_at | toHumanDatetime }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.distribution.uuid')" width="220px" align="center">
      <template slot-scope="scope">
        {{ scope.row.distribution.uuid }}
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.distributionitemfragmentation.code')" width="100px" align="center">
      <template slot-scope="scope">
        <span>{{ scope.row.itemfragmentation.donor_code }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.distributionitemfragmentation.hemocomponent')" width="300px">
      <template slot-scope="scope">
        <span>{{ scope.row.itemfragmentation.typehemocomponent.name }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.distributionitemfragmentation.blood_group')" align="center" width="80px">
      <template slot-scope="scope">
        <span :inner-html.prop="scope.row.itemfragmentation.fragmentation.extraction.donation.donor.group_abo | bloodGroupToHtml" />
        <span>{{ scope.row.itemfragmentation.fragmentation.extraction.donation.donor.factor_rh }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.distributionitemfragmentation.expired_date')" align="center" width="120px">
      <template slot-scope="scope">
        <span> {{ scope.row.itemfragmentation.expiration_date | toHumanDate }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.distributionitemfragmentation.type_payment')" align="center" width="150px">
      <template slot-scope="scope">
        <span>{{ scope.row.distribution.type_payment | receiptOptionsFilter }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.distributionitemfragmentation.status')" align="center" width="155px">
      <template slot-scope="scope">
        <el-tag v-if="!scope.row.distribution.is_delivered">EN PROCESO</el-tag>
        <el-tag v-if="scope.row.distribution.is_delivered" type="success">ENTREGADO</el-tag>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.distributionitemfragmentation.employee')" align="center" width="320px">
      <template slot-scope="scope">
        <span>{{ scope.row.distribution.employee | fullName }}</span>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
import { RECEIPT_OPTIONS } from '@/utils/const'

const receiptOptionsValue = RECEIPT_OPTIONS.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'TableDistributionItemFragmentation',
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

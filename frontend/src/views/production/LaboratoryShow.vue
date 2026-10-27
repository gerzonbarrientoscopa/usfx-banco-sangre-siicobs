<template>
  <div>
    <el-alert
      v-if="((aux && aux.fragmentation.extraction.donation.immunohematology==null) &&
        (aux && aux.fragmentation.extraction.donation.immunoserology==null))"
      :closable="false"
      title=""
      type="error"
    ><h1>FALTA LABORATORIO</h1></el-alert>
    <div v-else>
      <el-card shadow="always">
        <div slot="header" class="clearfix">
          INMUNOHEMATOLOGIA
        </div>
        <el-alert
          v-if="aux && !aux.fragmentation.extraction.donation.immunohematology"
          :closable="false"
          title="NO EXISTE REGISTRO INMUNOHEMATOLOGICO"
          type="error"
        />
        <table v-if="aux && aux.fragmentation.extraction.donation.immunohematology" width="100%">
          <tr>
            <td width="50%"><strong>ALB.: </strong></td>
            <td>{{ aux.fragmentation.extraction.donation.immunohematology.alb | crossesStatus }}</td>
          </tr>
          <tr>
            <td width="50%"><strong>FSI.: </strong></td>
            <td>{{ aux.fragmentation.extraction.donation.immunohematology.fsi | crossesStatus }}</td>
          </tr>
          <tr>
            <td width="50%"><strong>LISS.: </strong></td>
            <td>{{ aux.fragmentation.extraction.donation.immunohematology.liss | crossesStatus }}</td>
          </tr>
          <tr>
            <td width="50%"><strong>COOMBS: </strong></td>
            <td>{{ aux.fragmentation.extraction.donation.immunohematology.coombs | crossesStatus }}</td>
          </tr>
          <tr>
            <td width="50%"><strong>Anticuerpos Irregulares: </strong></td>
            <td>
              <span v-if="aux.fragmentation.extraction.donation.immunohematology.exist_irregular_antibody">
                <el-tag type="danger">POSITIVO</el-tag>
              </span>
              <span v-if="!aux.fragmentation.extraction.donation.immunohematology.exist_irregular_antibody">
                NEGATIVO
              </span>
            </td>
          </tr>
          <tr>
            <td width="50%"><strong>AntiKell: </strong></td>
            <td>{{ aux.fragmentation.extraction.donation.immunohematology.antikell | crossesStatus }}</td>
          </tr>
        </table>
      </el-card>
      <el-card shadow="always">
        <div slot="header" class="clearfix">
          INMUNOSEROLOGIA
        </div>
        <el-alert
          v-if="aux && !aux.fragmentation.extraction.donation.immunoserology"
          :closable="false"
          title="NO EXISTE REGISTRO INMUNOSEROLOGICO"
          type="error"
        />
        <table v-if="aux && aux.fragmentation.extraction.donation.immunoserology" width="100%">
          <tr>
            <td><strong>CHAGAS HAI: </strong></td>
            <td :class="getColor(aux.fragmentation.extraction.donation.immunoserology.chagas_hai)">
              {{ aux.fragmentation.extraction.donation.immunoserology.chagas_hai | reactiveStatus }}
            </td>
          </tr>
          <tr>
            <td><strong>HIV: </strong></td>
            <td :class="getColor(aux.fragmentation.extraction.donation.immunoserology.hiv)">
              {{ aux.fragmentation.extraction.donation.immunoserology.hiv | reactiveStatus }}
            </td>
          </tr>
          <tr>
            <td><strong>HBsAg: </strong></td>
            <td :class="getColor(aux.fragmentation.extraction.donation.immunoserology.hbsag)">
              {{ aux.fragmentation.extraction.donation.immunoserology.hbsag | reactiveStatus }}
            </td>
          </tr>
          <tr>
            <td><strong>HVC: </strong></td>
            <td :class="getColor(aux.fragmentation.extraction.donation.immunoserology.hvc)">
              {{ aux.fragmentation.extraction.donation.immunoserology.hvc | reactiveStatus }}
            </td>
          </tr>
          <tr>
            <td><strong>CHEIA: </strong></td>
            <td :class="getColor(aux.fragmentation.extraction.donation.immunoserology.cheia)">
              {{ aux.fragmentation.extraction.donation.immunoserology.cheia | reactiveStatus }}
            </td>
          </tr>
          <tr>
            <td><strong>RPR: </strong></td>
            <td :class="getColor(aux.fragmentation.extraction.donation.immunoserology.rpr)">
              {{ aux.fragmentation.extraction.donation.immunoserology.rpr | reactiveStatus }}
            </td>
          </tr>
        </table>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LaboratoryShow',
  filters: {
    reactiveStatus(data) {
      switch (data) {
        case 'R':
          return 'REACTIVO'
        case 'NR':
          return 'NO REACTIVO'
        case 'IN':
          return 'INDETERMINADO'
        default:
          return ''
      }
    },
    crossesStatus(data) {
      if (data === '-') {
        return 'NEGATIVO'
      } else {
        return data
      }
    }
  },
  props: {
    aux: {
      type: Object,
      default: null
    }
  },
  methods: {
    getColor(value) {
      switch (value) {
        case 'IN':
          return 'text-orange'
        case 'R':
          return 'text-red'
        default:
          return 'text-blue'
      }
    }
  }
}
</script>

<style scoped>
.text-red {
  color: red;
}

.text-orange {
  color: orange;
}

</style>

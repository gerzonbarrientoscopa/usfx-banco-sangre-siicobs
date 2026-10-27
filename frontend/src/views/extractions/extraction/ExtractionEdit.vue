<template>
  <div v-if="extraction" class="app-container">
    <el-row style="margin-top: 8px">
      <el-col :md="24">
        <el-tabs type="card" @tab-click="determineTab">
          <el-tab-pane>
            <span slot="label"><font-awesome-icon icon="user" /> Detalle</span>
            <extraction-form ref="extractionForm" :is-editing-parent="false" :row="extraction" @refreshExtraction="extractionGet" />
          </el-tab-pane>
        </el-tabs>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { graphqlRequest } from '@/api/graphql'
import extractions from '@/query/extraction'
import ExtractionForm from '@/views/extractions/extraction/tab/ExtractionForm'

export default {
  name: 'ExtractionEdit',
  components: { ExtractionForm },
  directives: {},
  filters: {},
  props: {},
  data() {
    return {
      loading: false,
      extraction: undefined
    }
  },
  computed: {},
  created() {
    this.extractionGet()
  },
  methods: {
    determineTab(ev) {
      switch (ev.paneName) {
        case '0':
          this.$refs.extractionForm.determineAction()
          break
        case '1':
          if (this.extraction.donation.type_process === 'NA' || this.extraction.donation.type_process === 'CA') {
            this.$refs.apheresisForm.determineAction()
          }
          break
        default:
          this.extractionGet()
          break
      }
    },
    extractionGet() {
      this.loading = true
      const id = this.$route.params && this.$route.params.id

      graphqlRequest(
        {
          from: this.$route.name,
          service: 'getExtraction',
          query: extractions.getExtraction(id),
          variables: { id: id }
        }
      ).then(response => {
        this.extraction = response.data.extraction
        this.setTagsViewTitle()
        this.loading = false
      })
    },
    setTagsViewTitle() {
      const title = 'Extracción'
      const route = Object.assign({}, this.$route, { title: `${title}-${this.extraction.id}` })
      this.$store.dispatch('tagsView/updateVisitedView', route)
    }
  }
}
</script>
<style type="text/scss">
.title {
  font-size: 15px;
  vertical-align: middle;
  text-transform: uppercase;
  font-weight: bold;
}
.bold {
  font-weight: bold;
}
.step {
  height: 300px;
  margin-top: 20px;
}
.text {
  padding-top: 5px;
  font-size: 12px;
}
.code {
  float: left;
  font-size: 15px;
  margin-right: 20px;
}
.font-120 {
  font-size: 120px;
}
.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}
.clearfix:after {
  clear: both
}
.mt-40 {
  margin-top: 40px;
}
.box-card {
  width: 100%;
  span {
    vertical-align: middle;
  }
  img {
    height:140px;
  }
}
.box-card {
  width: 100%;
  height: auto;
}
</style>

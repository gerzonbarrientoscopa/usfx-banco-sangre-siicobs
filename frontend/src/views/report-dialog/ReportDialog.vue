<template>
  <iframe id="toPrint" :src="temp" frameborder="0" allowfullscreen />
</template>

<script>
export default {
  name: 'ReportDialog',
  props: {
    row: {
      type: ArrayBuffer,
      default: null
    }
  },
  data() {
    return {
      temp: null
    }
  },
  mounted() {
    this.determineAction()
  },
  methods: {
    determineAction() {
      if (this.row != null) {
        const blob = new Blob([this.row], { type: 'application/pdf' })
        const link = document.createElement('a')
        link.href = window.URL.createObjectURL(blob)
        this.temp = link
        document.getElementById('toPrint').onload = function() {
          try {
            window.frames['toPrint'].print()
          } catch (e) {
            console.log(e)
            try {
              window.frames['toPrint'].contentWindow.print()
            } catch (e) {
              console.log(e)
            }
          }
        }
      }
    }
  }
}
</script>

<style scoped>
  iframe {
    height:calc(100vh - 125px);
    width:calc(100vw - 50px);
    box-sizing: border-box;
  }
</style>

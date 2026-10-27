<template>
  <iframe id="iframeElementId" frameborder="0" allowfullscreen />
</template>

<script>
export default {
  name: 'HtmlView',
  props: {
    html: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      link: null
    }
  },
  mounted() {
    this.determineAction()
  },
  methods: {
    determineAction() {
      if (this.html != null) {
        var iframedoc = document.getElementById('iframeElementId').contentDocument || document.getElementById('iframeElementId').contentWindow.document

        // iframedoc.head.innerHTML = this.html
        iframedoc.body.innerHTML = this.html
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

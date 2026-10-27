<template>
  <div class="app-container">
    <el-row>
      <el-col :md="12">
        <el-card>
          <video ref="video" playsinline autoplay class="camera-stream" />
        </el-card>
        <div class="camera-modal-container">
          <el-button type="success" icon="el-icon-upload" @click="capture">CAPTURAR</el-button>
        </div>
      </el-col>
      <el-col :md="12">
        <el-card>
          <img v-if="previewPhoto === null" src="@/assets/global_images/user.png" alt="">
          <img :src="previewPhoto" class="image" alt="">
        </el-card>
        <div class="camera-modal-container">
          <el-button :disabled="previewPhoto === null" icon="el-icon-save" @click="save">GUARDAR</el-button>
        </div>
      </el-col>
    </el-row>

  </div>
</template>

<script>
import { updateImageDonor } from '@/api/donor'
export default {
  name: 'Camera',
  props: {
    row: {
      type: Number,
      default: null
    }
  },
  data() {
    return {
      mediaStream: null,
      previewPhoto: null
    }
  },
  watch: {},
  mounted() {
    this.reset()
  },
  methods: {
    handleSuccess(stream) {
      this.mediaStream = stream
      this.$refs.video.srcObject = stream
    },
    async reset() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true })
        this.handleSuccess(stream)
      } catch (e) {
        console.error('getUserMedia() error:', e)
      }
    },
    capture() {
      const mediaStreamTrack = this.mediaStream.getVideoTracks()[0]
      const imageCapture = new window.ImageCapture(mediaStreamTrack)

      imageCapture.takePhoto().then(blob => {
        const reader = new FileReader()
        reader.readAsDataURL(blob)
        reader.onloadend = function() {
          window.blob = reader.result
        }
      })
      setTimeout(() => {
        this.previewPhoto = window.blob
      }, 1000)
    },
    closeWebCam() {
      this.mediaStream.getTracks().forEach(function(track) {
        if (track.readyState === 'live') {
          track.stop()
        }
      })

      this.mediaStream = null
      this.previewPhoto = null
      this.$refs.video.srcObject = null
    },
    save() {
      var tempData = { url: this.previewPhoto }
      updateImageDonor(this.row, tempData).then(response => {
        this.$emit('dialogStatus', false)
        this.$notify({
          title: 'Actualizado',
          message: 'Se ha actualizado el registro del donante',
          type: 'success',
          duration: 2000
        })
      })
    }
  }
}
</script>

<style scoped>
  .camera-stream {
    width: 100%;
    height: 100%;
  }
  .camera-modal-container {
    position: absolute;
    width: 100%;
    align-items: center;
    margin-bottom: 24px;
  }
</style>

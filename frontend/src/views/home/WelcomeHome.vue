<script lang="ts" setup>
import { ref } from 'vue'
import { useSubmit } from '@/utils'
import { getHomeData } from '@/api'

const msg = ref('欢迎使用域名管理平台!')
const { loading, submit } = useSubmit({
  post: getHomeData,
  hideSuccessDialog: true,
  callback: (data: string) => {
    msg.value = data
  }
})

submit()
</script>

<template>
  <div class="m_container_content" v-loading="loading">
    <el-empty :image-size="200" :description="msg" />
  </div>
</template>

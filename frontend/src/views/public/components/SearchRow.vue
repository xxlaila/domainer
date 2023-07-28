<script setup lang="ts">
import { ref } from 'vue'
import { Plus } from '@element-plus/icons-vue'

const props = defineProps<{ showAdd?: boolean }>()
const emit = defineEmits(['add', 'delete', 'submit', 'export'])
const name = ref('')

const submit = (name: string) => {
  emit('submit', props.showAdd ? { subdomain: name } : { domain_name: name })
}
</script>

<template>
  <el-row class="m_container_top">
    <el-button
      v-if="props.showAdd"
      type="primary"
      @click="emit('add')"
      :icon="Plus"
      style="margin-right: 16px"
    >
      新建
    </el-button>

    <el-input
      v-model="name"
      placeholder="搜索域名"
      clearable
      @keyup.enter="submit(name)"
      class="m_domain_input"
    />

    <el-button type="primary" @click="submit(name)">搜索</el-button>
    <el-button type="primary" v-if="props.showAdd" @click="emit('export')">导出</el-button>
  </el-row>
</template>

<style scoped>
.m_domain_input {
  width: 200px;
  margin-right: 16px;
}
</style>

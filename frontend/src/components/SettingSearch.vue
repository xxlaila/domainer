<script setup lang="ts">
import { Delete, Plus } from '@element-plus/icons-vue'

const props = defineProps<{ showDel: boolean }>()
const emit = defineEmits(['add', 'delete'])
</script>

<template>
  <el-row class="m_container_top" justify="space-between">
    <el-button type="primary" @click="emit('add')" :icon="Plus">新建</el-button>

    <el-button v-if="props.showDel" plain @click="emit('delete')" :icon="Delete">删除</el-button>
  </el-row>
</template>

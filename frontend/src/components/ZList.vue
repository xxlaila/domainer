<script setup lang="ts" generic="T">
import { computed } from 'vue'
import type { ColumnLists, ListReturn } from '@/types'

const props = defineProps<{
  search: ListReturn<T>
  columns: ColumnLists<T>
}>()
const emit = defineEmits(['click', 'selection-change'])

const { page, size, setPage, setSize, count, list, error, loading, retry } = computed(
  () => props.search
).value
</script>

<template>
  <div class="z_list_container">
    <el-table
      v-loading="loading"
      :data="list"
      stripe
      border
      highlight-current-row
      tooltip-effect="light"
      size="large"
      @selection-change="(rows) => emit('selection-change', rows)"
    >
      <el-table-column align="center" type="selection" width="58" />

      <el-table-column
        v-for="column in props.columns"
        :key="column.key"
        :prop="column.key"
        :label="column.label"
        :width="column.width"
        :min-width="column.minWidth"
        :fixed="column.fixed"
        :show-overflow-tooltip="column.ellipsis"
      >
        <template v-if="column.link" #default="{ row }">
          <span class="z_list_cell" @click="emit('click', row)">
            {{ row[column.key] }}
          </span>
        </template>

        <template v-else-if="column.slot" #default="{ row }">
          <slot :name="column.key" :row="row"></slot>
        </template>
      </el-table-column>

      <!-- 接口异常显示 -->
      <template v-if="error" #empty>
        <p>{{ error }}</p>
        <el-button type="primary" size="small" @click="retry()">重试</el-button>
      </template>
    </el-table>

    <!-- 分页 -->
    <el-pagination
      class="z_list_pagination"
      v-model:current-page="page"
      v-model:page-size="size"
      @current-change="setPage"
      @size-change="setSize"
      background
      layout="slot, total, prev, pager, next"
      :total="count"
    />
  </div>
</template>

<style style="scss">
.z_list_container {
  margin-top: 8px;
  background-color: var(--color-background);
  padding: var(--primary-padding);
}

.z_list_pagination {
  margin: 24px 0 14px;
  justify-content: end;
}

.z_list_cell {
  position: relative;
  text-decoration: none;
  outline: none;
  cursor: pointer;
  vertical-align: middle;
  padding: 0;
  font-weight: 500;
  color: rgb(79, 122, 253);
}
</style>

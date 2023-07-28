<script setup lang="ts">
import type { CloudSecretItem, ColumnLists, DetailType } from '@/types'
import { ref, shallowRef } from 'vue'
import { deleteSkeySetting, getSkeySettingLists } from '@/api'
import { useBatchDelete, usePagiLists, useToggle } from '@/utils'
import { usePermissionStore } from '@/stores/permission'
import ZList from '@/components/ZList.vue'
import SettingSearch from '@/components/SettingSearch.vue'
import EditForm from './components/EditForm.vue'

const columns: ColumnLists<CloudSecretItem> = [
  {
    key: 'name',
    label: '所属云',
    width: 130,
    link: true
  },
  {
    key: 'secretid',
    label: 'SecretId',
    minWidth: 210,
    ellipsis: true
  },
  {
    key: 'tags',
    label: '标签',
    minWidth: 150
  },
  {
    key: 'comment',
    label: '备注',
    width: 144
  },
  {
    key: 'created_by',
    label: '创建人',
    width: 150
  },

  {
    key: 'created_time',
    label: '创建时间',
    width: 180
  },
  {
    key: 'updated_time',
    label: '更新时间',
    width: 180
  },
  {
    key: 'action',
    label: '操作',
    width: 113,
    fixed: 'right',
    slot: true
  }
]

// 控制右侧面板显示
const [showEventDetail, toggleEventDetail] = useToggle(false)
const currentItem = shallowRef<CloudSecretItem>()
const detailType = ref<DetailType>('detail')
const onItemClick = (item, type: DetailType) => {
  currentItem.value = item

  detailType.value = type
  toggleEventDetail(true)
}

// 搜索条件相关
const search = usePagiLists<CloudSecretItem>({
  get: getSkeySettingLists
})

// 处理删除功能
const { hasGlobalDelPerm } = usePermissionStore()
const { selectedRows, onSelctionChange, onBatchDelete } = useBatchDelete<CloudSecretItem>({
  post: deleteSkeySetting,
  key: 'secretid',
  callback: search.retry
})
</script>
<template>
  <SettingSearch
    @add="onItemClick(undefined, 'add')"
    @delete="onBatchDelete(selectedRows)"
    :showDel="hasGlobalDelPerm"
  ></SettingSearch>

  <z-list
    :columns="columns"
    :search="search"
    @click="onItemClick"
    @selection-change="onSelctionChange"
  >
    <template #action="{ row }">
      <el-button link type="primary" @click="onItemClick(row, 'edit')">编辑</el-button>

      <el-button v-if="hasGlobalDelPerm" link type="danger" @click="onBatchDelete([row])">
        删除
      </el-button>
    </template>
  </z-list>

  <EditForm
    :show="showEventDetail"
    :type="detailType"
    :data="currentItem"
    @close="toggleEventDetail(false)"
    @success="search.retry"
  ></EditForm>
</template>

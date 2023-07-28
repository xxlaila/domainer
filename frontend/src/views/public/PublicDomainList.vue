<script setup lang="ts">
import { useRouter } from 'vue-router'
import { getDomainList } from '@/api'
import type { ColumnLists, DomainSearchProps, DomainItemType } from '@/types'
import { usePagiLists } from '@/utils'
import SearchRow from './components/SearchRow.vue'
import ZList from '@/components/ZList.vue'

const router = useRouter()
const columns: ColumnLists<DomainItemType> = [
  {
    key: 'name',
    label: '域名',
    link: true,
    width: 400
  },
  {
    key: 'status_label',
    label: '解析状态',
    width: 120
  },
  {
    key: 'recordCount',
    label: '记录数量',
    width: 110
  },
  {
    key: 'remark',
    label: '备注',
    width: 125
  },
  {
    key: 'createdon',
    label: '添加时间',
    minWidth: 120
  },
  {
    key: 'cloud_label',
    label: '归属云',
    minWidth: 90
  }
]

const { submit, ...search } = usePagiLists<DomainItemType, DomainSearchProps>({
  get: getDomainList,
  initParam: {
    domain_name: ''
  }
})

//  编辑
const onEditClick = ({ domainid, name, cloud }) =>
  router.push({
    path: `/public/${domainid}`,
    query: {
      name,
      cloud
    }
  })
</script>

<template>
  <search-row @submit="submit"></search-row>

  <z-list :columns="columns" :search="search" @click="onEditClick"></z-list>
</template>

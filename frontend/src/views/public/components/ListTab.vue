<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { useToggle, usePagiLists, useSubmit, getCurrentDateTime } from '@/utils'
import { getDomainDetailList, updateDomainInfo, exportDomain } from '@/api'
import type {
  ColumnLists,
  DetailType,
  CLOUD_TYPE_KEY,
  DomainDetailSearchProps,
  DomainDetailType
} from '@/types'
import ZList from '@/components/ZList.vue'
import EditDialog from './EditDialog.vue'
import SearchRow from './SearchRow.vue'
import IconCircle from '@/components/icons/IconCircle.vue'
import IconPause from '@/components/icons/IconPause.vue'
import { downloadFileFromBlob } from '@/utils'

const columns: ColumnLists<DomainDetailType> = [
  {
    key: 'subdomain',
    label: '主机记录',
    // link: true,
    slot: true,
    minWidth: 180,
    ellipsis: true,
    fixed: 'left'
  },
  {
    key: 'type',
    label: '记录类型',
    width: 90
  },
  {
    key: 'line',
    label: '线路类型',
    width: 90
  },
  {
    key: 'value',
    label: '记录值',
    width: 200,
    ellipsis: true
  },
  {
    key: 'mx',
    label: 'MX优先级',
    width: 100
  },
  {
    key: 'ttl',
    label: 'TTL(秒)',
    width: 82
  },
  {
    key: 'status_label',
    label: '状态',
    width: 82
  },
  {
    key: 'remark',
    label: '备注',
    width: 100,
    ellipsis: true
  },
  {
    key: 'created_time',
    label: '添加时间',
    width: 170
  },
  {
    key: 'action',
    label: '操作',
    width: 160,
    slot: true,
    fixed: 'right'
  }
]

const route = useRoute()

// 列表搜索
const { submit, setParams, ...search } = usePagiLists<DomainDetailType, DomainDetailSearchProps>({
  get: getDomainDetailList,
  pageSize: 10,
  initParam: {
    domain_name: '',
    domainid: route.params.id as string,
    name: route.query.name as string,
    cloud: route.query.cloud as CLOUD_TYPE_KEY
  }
})

watch(
  () => route.params.id,
  (id, oldid) => {
    if (id && oldid && id !== oldid) {
      setParams({
        domainid: id as string,
        name: route.query.name as string,
        cloud: route.query.cloud as CLOUD_TYPE_KEY
      })
    }
  },
  {
    immediate: true
  }
)

const detailType = ref<DetailType>('detail')
const [showEditDialog, onToggleEditDialog] = useToggle(false)
const currentItem = ref<DomainDetailType>()
const onItemClick = (item, type: DetailType) => {
  currentItem.value = item

  detailType.value = type
  onToggleEditDialog(true)
}

// 删除、启用、暂停 二次确认弹窗
const { submit: onSubmitUpdate } = useSubmit<DomainDetailType>({
  post: updateDomainInfo,
  msg: '删除成功！',
  callback: search.retry
})
const showConfirmDialog = async (row, action) => {
  const isActionStatus = action === 'status'
  const title = `${isActionStatus ? (row.status === 1 ? '暂停' : '启用') : '删除'}`

  try {
    await ElMessageBox.confirm(`确认${title}${row.subdomain}解析？`, title, {
      showCancelButton: false,
      confirmButtonText: '确定',
      async beforeClose(ac, instance, done) {
        if (ac === 'confirm') {
          instance.confirmButtonLoading = true
          instance.confirmButtonText = `${title}中...`

          const param = { ...row, action }
          if (isActionStatus) {
            param.status = row.status === 1 ? 0 : 1
          }

          await onSubmitUpdate({
            ...param,
            name: route.query.name as string,
            domainid: route.params.id as string,
            cloud: route.query.cloud as CLOUD_TYPE_KEY
          })

          instance.confirmButtonLoading = false
          done()
        } else {
          done()
        }
      }
    })
  } catch (error) {
    // empty
  }
}

const checkedOptions = ref<DomainDetailType[]>([])
const onSectionChange = (row) => {
  checkedOptions.value = row
}

const onExportClick = async () => {
  const { data } = await exportDomain({
    domain_name: route.query.name as string,
    domainid: route.params.id as string,
    cloud: route.query.cloud as CLOUD_TYPE_KEY,
    action: checkedOptions.value.length > 0 ? 'ids' : 'all',
    ids: checkedOptions.value.map((item) => item.id).join(',')
  })

  const fileName = `${route.query.name}_${getCurrentDateTime()}_域名列表.xlsx`

  downloadFileFromBlob(data, fileName)
}
</script>

<template>
  <!-- 搜索栏 -->
  <search-row
    @submit="submit"
    @add="onItemClick(undefined, 'add')"
    show-add
    @export="onExportClick"
  ></search-row>

  <z-list
    :columns="columns"
    :search="search"
    @click="onItemClick"
    @selection-change="onSectionChange"
  >
    <template #subdomain="{ row }">
      <span class="z_list_cell" @click="onItemClick(row, 'detail')">
        <el-icon class="z_cell_icon" v-if="row.status === 1" size="12px" color="#67c23a"
          ><IconCircle
        /></el-icon>
        <el-icon class="z_cell_icon" v-else size="12px" color="#e6a23c"><IconPause /></el-icon>
        <span style="padding-left: 8px">{{ row.subdomain }}</span>
      </span>
    </template>

    <template #action="{ row }">
      <el-button link type="primary" @click="onItemClick(row, 'edit')">修改</el-button>
      <el-button link type="primary" @click="showConfirmDialog(row, 'status')">
        {{ row.status === 1 ? '暂停' : '启用' }}
      </el-button>
      <el-button link type="danger" @click="showConfirmDialog(row, 'delete')"> 删除 </el-button>
    </template>
  </z-list>

  <!-- 编辑弹窗 -->
  <edit-dialog
    :show="showEditDialog"
    :type="detailType"
    :data="currentItem"
    @close="onToggleEditDialog(false)"
    @success="search.retry()"
  />
</template>

<style>
.z_cell_icon {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translate(-50%, -50%);
}
</style>

<script lang="ts" setup>
import { computed, shallowRef, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getDomainAuditList } from '@/api'
import { DomainAuditLogSearchProps, DomainAuditLogType } from '@/types'
import { usePagiLists } from '@/utils'
import SearchRow from './SearchRow.vue'

const route = useRoute()

const list = shallowRef<DomainAuditLogType[]>([])
const { page, count, setPage, error, loading, retry, submit } = usePagiLists<
  DomainAuditLogType,
  DomainAuditLogSearchProps
>({
  pageSize: 10,
  get: getDomainAuditList,
  initParam: {
    domain_name: '',
    domainid: route.params.id as string,
    name: route.query.name as string,
    cloud: route.query.cloud as string
  },

  callback: (data) => {
    if (page.value === 1) {
      list.value = data.results
    } else {
      list.value = list.value.concat(data.results)
    }
  }
})

watch(
  () => route.params.id,
  (id, oldid) => {
    if (id && oldid && id !== oldid) {
      submit({
        domain_name: '',
        domainid: id as string,
        name: route.query.name as string,
        cloud: route.query.cloud as string
      })
    }
  },
  {
    immediate: true
  }
)

const desc = computed(() =>
  error.value ? error.value.message || error.value.name || 'unknow error' : '暂无数据'
)

const hasMore = computed(() => list.value && list.value.length < count.value)
const disabled = computed(() => loading.value || !hasMore.value)
const load = () => {
  !disabled.value && setPage(page.value + 1)
}

const refresh = (data) => {
  list.value = []
  submit({ ...data })
}

const typeColor = {
  add: 'success',
  delete: 'danger',
  status: 'primary'
}
</script>

<template>
  <!-- 搜索栏 -->
  <search-row @submit="refresh"></search-row>

  <div class="m_container_content infinite-list-wrapper" style="overflow: auto">
    <el-timeline v-infinite-scroll="load" :infinite-scroll-disabled="disabled">
      <el-timeline-item
        v-for="item in list"
        :key="item.id"
        :timestamp="item.created_time"
        :type="typeColor[item.action] || 'primary'"
        placement="top"
      >
        <el-card>
          <h3>{{ item.action }} {{ item.name }}</h3>
          <p class="m_ope_content">更新后：{{ item.news_record }}</p>
          <p class="m_ope_content">更新前：{{ item.source_record || '-' }}</p>
          <p class="m_ope_content">更新人：{{ item.created_by || '-' }}</p>
        </el-card>
      </el-timeline-item>
    </el-timeline>

    <template v-if="error || count === 0">
      <el-empty :image-size="200" v-loading="loading" :description="desc">
        <el-button type="primary" size="small" @click="retry()">重试</el-button>
      </el-empty>
    </template>

    <template v-else>
      <p class="flex-center" v-if="loading">加载中...</p>
      <p class="flex-center" v-if="!hasMore">到底了</p>
    </template>
  </div>
</template>

<style scoped>
.infinite-list-wrapper {
  height: calc(100vh - 182px);
  font-size: 14px;
}

.m_ope_content {
  margin-top: 10px;
}

.m_ope_bottom {
  font-size: 12px;
}
</style>

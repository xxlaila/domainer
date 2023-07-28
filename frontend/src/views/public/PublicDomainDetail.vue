<script setup>
import { defineAsyncComponent, computed, ref, shallowRef } from 'vue'
const ListTab = defineAsyncComponent(() => import('./components/ListTab.vue'))
const AuditTab = defineAsyncComponent(() => import('./components/AuditTab.vue'))
const menus = shallowRef([
  {
    key: 'RecordManage',
    name: '记录管理',
    component: ListTab
  },
  {
    key: 'OperateLog',
    name: '操作记录',
    component: AuditTab
  }
])

const active = ref('RecordManage')
const activeTab = computed(() => {
  const item = menus.value.find((item) => item.key === active.value)

  return item.component
})
const setActive = (tab) => (active.value = tab)
</script>

<template>
  <div>
    <el-menu :default-active="active" mode="horizontal">
      <el-menu-item
        v-for="item in menus"
        :key="item.key"
        :index="item.key"
        @click="setActive(item.key)"
      >
        {{ item.name }}
      </el-menu-item>
    </el-menu>

    <keep-alive>
      <Suspense>
        <component :is="activeTab" />

        <!-- 加载中状态 -->
        <template #fallback>
          <div v-loading="true" style="width: 100%; height: 200px"></div>
        </template>
      </Suspense>
    </keep-alive>
  </div>
</template>

<script setup lang="ts">
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import ZMenu from '@/components/ZMenu.vue'
import ZHeader from '@/components/ZHeader.vue'
</script>

<template>
  <el-config-provider namespace="dns" :locale="zhCn">
    <el-container>
      <el-header>
        <ZHeader />
      </el-header>
      <el-container>
        <el-aside width="200px"><ZMenu /></el-aside>
        <el-main>
          <RouterView v-slot="{ Component }">
            <keep-alive include="PublicDomainList">
              <component :is="Component"></component>
            </keep-alive>
          </RouterView>
        </el-main>
      </el-container>
    </el-container>
  </el-config-provider>
</template>

<style scoped>
.dns-main {
  background: #f5f7fa;
  padding: 10px 16px;
}

.dns-aside {
  z-index: 1;
  box-shadow: rgba(0, 0, 0, 0.1) 1px 2px 5px 0;
}

.dns-menu {
  border-right: none;
}

.dns-header {
  z-index: 3;
  box-shadow: rgba(0, 0, 0, 0.1) 0px 1px 1px;
}

.dns-container {
  height: 100%;
}
</style>

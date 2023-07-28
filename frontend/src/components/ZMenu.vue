<script setup lang="ts">
import ZMenuItem from './ZMenuItem.tsx'
import { menus } from '@/router/menus'
</script>

<template>
  <el-menu router>
    <ZMenuItem v-for="item in menus" :key="item.name" :menu="item" />

    <!-- <template v-for="item in menus" :key="item.name">
      <el-sub-menu v-if="item.children">
        <template #title>
          <el-icon v-if="item.icon"><component :is="item.icon"></component></el-icon>
          <span>{{ item.title }}</span>
        </template>
        <el-menu-item :index="child.path" v-for="child in item.children" :key="child.name">
          <template #title>
            <el-icon v-if="child.icon"><component :is="child.icon"></component></el-icon>
            <span>{{ child.title }}</span>
          </template>
        </el-menu-item>
      </el-sub-menu>
      <el-menu-item v-else :index="item.path">
        <template #title>
          <el-icon v-if="item.icon"><component :is="item.icon"></component></el-icon>
          <span>{{ item.title }}</span>
        </template>
      </el-menu-item>
    </template> -->
  </el-menu>
</template>


<template>
  <el-row class="m_header" justify="space-between" align="middle">
    <el-row align="middle">
      <img
        class="m_header_logo"
        src="https://photo.zastatic.com/images/common-cms/it/20230727/1690453619746_286919_t.png"
        alt="头像"
      />

      <span>域名管理平台</span>
    </el-row>
    <el-row align="middle">
      <span style="font-size: 14px;">Admin，欢迎你</span>
      <img
        class="m_header_avatar"
        src="https://photo.zastatic.com/images/common-cms/it/20230106/1672993768874_958303_t.png"
        alt="头像"
      />
    </el-row>
  </el-row>
</template>

<style lang="scss" scoped>
.m_header {
  height: var(--dns-header-height);
}
.m_header_logo {
  height: 40px;
  max-width: 200px;
  margin-right: 10px;
  object-fit: contain;
}
.m_header_avatar {
  height: 30px;
  border-radius: 50%;
  vertical-align: middle;
  margin-left: 8px;
}
.el-header {
  line-height: var(--dns-header-height);
}
</style>

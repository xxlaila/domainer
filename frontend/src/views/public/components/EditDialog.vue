<script lang="ts" setup>
import { computed, reactive, watch } from 'vue'
import { FormRules } from 'element-plus'
import { CaretBottom } from '@element-plus/icons-vue'
import { RecordTypeDict, DomainDetailDict } from '@/utils'
import { convertDictStr, useForm, useSubmit, DetailTitle } from '@/utils'
import { updateDomainInfo } from '@/api'
import type { CLOUD_TYPE_KEY, DetailType, DomainActionType, DomainDetailType } from '@/types'
import { useRoute } from 'vue-router'

const emit = defineEmits(['close', 'success'])
const props = defineProps<{
  show: boolean
  type: DetailType
  data?: DomainDetailType
}>()
const title = computed(() => convertDictStr(DetailTitle, props.type))
const isAdd = computed(() => props.type === 'add')
const showEdit = computed(() => isAdd.value || props.type === 'edit')

const route = useRoute()
const initData = (): Partial<DomainDetailType> => ({
  subdomain: '',
  type: 'A',
  value: '',
  status: 1,
  ttl: 600,
  remark: ''
})

const editForm = reactive<Partial<DomainDetailType>>(initData())

watch([() => props.show, () => props.data], ([show, data]) => {
  if (show) {
    const detailData = data || initData()
    // 数据初始化
    for (const key of Object.keys(editForm)) {
      editForm[key] = detailData[key]
    }
  }
})

const isEdit = computed(() => props.data && props.data.secordid)

// 处理表单事件
const { formRef: editFormRef, resetForm, submitForm } = useForm()

// 处理提交事件
const { loading: btnLoading, submit } = useSubmit<DomainDetailType>({
  post: () => {
    const action: DomainActionType = isEdit.value ? 'modify' : 'add'
    const param = {
      ...editForm,
      name: route.query.name as string,
      domainid: route.params.id as string,
      line: 'default',
      cloud: route.query.cloud as CLOUD_TYPE_KEY,
      action
    }

    if (isEdit.value) {
      param.secordid = props.data?.secordid
    }

    return updateDomainInfo(param)
  },
  callback: () => {
    emit('close')
    emit('success')
  }
})

// 表单数据验证
const rules: FormRules = {
  subdomain: [{ required: true, message: '解析域名不能为空！', trigger: 'blur' }],
  type: [{ required: true, message: '记录类型不能为空！', trigger: 'change' }],
  status: [{ required: true, message: '状态不能为空！', trigger: 'change' }],
  value: [{ required: true, message: '记录值不能为空！', trigger: 'blur' }],
  ttl: [{ required: true, message: 'TTL不能为空！', trigger: 'blur' }],
  remark: [{ required: true, message: '备注不能为空！', trigger: 'change' }]
}
</script>

<template>
  <el-drawer
    :model-value="props.show"
    direction="rtl"
    @close="emit('close')"
    @closed="resetForm(editFormRef)"
    size="540"
  >
    <template #header>
      <div class="m_detail_header">{{ title }}</div>
    </template>

    <template #default>
      <!-- 编辑表单 -->
      <template v-if="showEdit">
        <el-form
          ref="editFormRef"
          :model="editForm"
          :rules="rules"
          label-width="83px"
          size="small"
          label-position="left"
          style="margin-top: 16px"
        >
          <el-form-item label="主机记录:" prop="subdomain">
            <el-input v-model="editForm.subdomain" placeholder="请输入主机记录" />
          </el-form-item>

          <el-form-item label="状态:" prop="status">
            <el-select
              v-model="editForm.status"
              :suffix-icon="CaretBottom"
              placeholder="请选择状态"
            >
              <el-option label="启用" :value="1" />
              <el-option label="禁用" :value="0" />
            </el-select>
          </el-form-item>

          <el-form-item label="记录类型:" prop="type">
            <el-select v-model="editForm.type" :suffix-icon="CaretBottom" placeholder="记录类型">
              <el-option
                v-for="(item, value) in RecordTypeDict"
                :key="value"
                :label="item.key"
                :value="item.key"
              >
                {{ item.key }} : {{ item.desc }}
              </el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="TTL:" prop="ttl">
            <el-input-number v-model="editForm.ttl" :min="1" placeholder="请输入TTL" />
          </el-form-item>

          <el-form-item label="记录值:" prop="value">
            <el-input
              v-model="editForm.value"
              :rows="4"
              type="textarea"
              placeholder="请输入记录值"
            />
          </el-form-item>

          <el-form-item label="备注:" prop="remark">
            <el-input
              v-model="editForm.remark"
              :rows="4"
              type="textarea"
              placeholder="请输入备注信息"
            />
          </el-form-item>
        </el-form>
      </template>

      <template v-else-if="data">
        <div class="m_setting_detail_list">
          <div class="m_event_detail" v-for="(item, index) in DomainDetailDict" :key="index">
            <template v-for="(value, key) in item" :key="key">
              <div class="m_event_detail_key">{{ value }}:</div>
              <div class="m_setting_detail_value">{{ data[key] }}</div>
            </template>
          </div>
        </div>
      </template>
    </template>

    <template #footer>
      <el-button
        type="primary"
        :loading="btnLoading"
        @click="submitForm(editFormRef, submit)"
        style="width: 96px"
      >
        保存
      </el-button>
    </template>
  </el-drawer>
</template>

<script lang="ts" setup>
import { computed, reactive, watch, toRaw } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormRules } from 'element-plus'
import {
  CLOUD_DICT,
  convertDictStr,
  DetailTitle,
  useForm,
  useSubmit,
  CloudSecretItemDetailDict
} from '@/utils'
import { addCloudSecretItem, updateCloudSecretItemById } from '@/api'
import type { CLOUD_TYPE_KEY, CloudSecretItem, DetailType } from '@/types'
import { CaretBottom } from '@element-plus/icons-vue'

const emit = defineEmits(['close', 'success'])
const onClose = () => emit('close')
const { formRef: editFormRef, resetForm, submitForm } = useForm()

const props = defineProps<{
  show: boolean
  type: DetailType
  data?: CloudSecretItem
}>()
const title = computed(() => convertDictStr(DetailTitle, props.type))
const isAdd = computed(() => props.type === 'add')
const showEdit = computed(() => isAdd.value || props.type === 'edit')

type editFormType = {
  name: CLOUD_TYPE_KEY
  secretid: string
  secretkey: string
  tags: string
  comment: string
}
const initData = (): editFormType => ({
  name: 'Tencent',
  secretid: '',
  secretkey: '',
  tags: '',
  comment: ''
})

const editForm = reactive<editFormType>(initData())
watch(
  () => props.data,
  (data) => {
    const currentData = data ? data : initData()

    // 数据初始化
    for (const key of Object.keys(editForm)) {
      editForm[key] = currentData[key] || ''
    }
  }
)

const rules = reactive<FormRules>({
  secretid: [{ required: true, message: '所属云不能为空！', trigger: 'blur' }],
  secretkey: [{ required: true, message: '名称不能为空！', trigger: 'blur' }],
  name: [
    {
      required: true,
      message: '请选择所属云',
      trigger: 'change'
    }
  ]
})

// 更新
const { loading: updateLoading, submit: submitUpdate } = useSubmit<CloudSecretItem, string>({
  post: (id) => updateCloudSecretItemById(id, toRaw(editForm)),
  callback: () => emit('success')
})
const updateItem = () => {
  if (!props.data) {
    return ElMessage.error('数据异常：获取不到ID！')
  }

  submitUpdate(props.data.id)
}

// 新增
const { loading: addLoading, submit: addItem } = useSubmit<CloudSecretItem>({
  post: () => addCloudSecretItem(toRaw(editForm)),
  msg: '新增成功！',
  callback: () => {
    onClose()
    emit('success')
  }
})

const btnLoading = computed(() => updateLoading.value && addLoading.value)
</script>

<template>
  <el-drawer
    :model-value="props.show"
    direction="rtl"
    @close="onClose"
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
          label-width="75px"
          size="small"
          label-position="left"
          style="margin-top: 16px"
        >
          <el-form-item label="所属云:" prop="name">
            <el-select
              v-model="editForm.name"
              :suffix-icon="CaretBottom"
              placeholder="请选择所属云"
              class="m_column_item"
            >
              <el-option
                v-for="(key, value) in CLOUD_DICT"
                :key="value"
                :label="key"
                :value="value"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="Secretid:" prop="secretid">
            <el-input v-model="editForm.secretid" placeholder="请输入Secretid" />
          </el-form-item>

          <el-form-item label="Secretkey:" prop="secretkey">
            <el-input v-model="editForm.secretkey" placeholder="请输入Secretkey" />
          </el-form-item>

          <el-form-item label="标签:" prop="tags">
            <el-input v-model="editForm.tags" placeholder="请输入标签" />
          </el-form-item>

          <el-form-item label="备注:" prop="comment">
            <el-input v-model="editForm.comment" placeholder="请输入备注" />
          </el-form-item>
        </el-form>
      </template>

      <!-- 详情显示 -->
      <template v-else-if="data">
        <div class="m_setting_detail_list">
          <div
            class="m_event_detail"
            v-for="(item, index) in CloudSecretItemDetailDict"
            :key="index"
          >
            <template v-for="(value, key) in item" :key="key">
              <div class="m_event_detail_key">{{ value }}:</div>
              <div class="m_setting_detail_value">{{ data[key] }}</div>
            </template>
          </div>
        </div>
      </template>
    </template>

    <template #footer>
      <template v-if="showEdit">
        <el-button
          type="primary"
          :loading="btnLoading"
          @click="submitForm(editFormRef, isAdd ? addItem : updateItem)"
          style="width: 96px"
        >
          {{ isAdd ? '新增' : '更新' }}
        </el-button>
      </template>
    </template>
  </el-drawer>
</template>

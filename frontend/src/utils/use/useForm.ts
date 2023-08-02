/*
 * @Author: cc2victoria@gmail.com
 * @Date: 2023-07-20 18:38:34
 * @Last Modified by:   cc2victoria@gmail.com
 * @Last Modified time: 2023-07-20 18:38:34
 */
import { ref } from 'vue'
import type { FormInstance } from 'element-plus'

export const useForm = () => {
  const formRef = ref<FormInstance>()
  // 重置表格
  const resetForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.resetFields()
  }

  // 清理表单验证信息
  const clearFormValidate = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.clearValidate()
  }

  const submitForm = async (formEl: FormInstance | undefined, callback: Function) => {
    if (!formEl) return
    await formEl.validate((valid, fields) => {
      if (valid) {
        callback()
      } else {
        console.log('error submit!', fields)
      }
    })
  }

  return { formRef, resetForm, clearFormValidate, submitForm }
}

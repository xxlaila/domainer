/*
 * @Author: cc2victoria@gmail.com
 * @Date: 2023-03-31 14:17:42
 * @Last Modified by: cc2victoria@gmail.com
 * @Last Modified time: 2023-07-20 16:26:16
 */
import { ref } from 'vue';
export const usePagination = (defautPage = 1, defautSize = 10) => {
  const page = ref(defautPage);
  const size = ref(defautSize);
  const setPage = (val: number) => (page.value = val);
  const setSize = (val: number) => (size.value = val);

  return { page, size, setPage, setSize };
};
